from ..config import Config, WINDOW_MODE, LINSPACE_MODE, LIST_MODE
from itertools import product
from .points import build_p_linspace, build_p_window
from typing import Any
from dataclasses import dataclass
from ..noise.registry import build_noise
from ..codes.registry import build_code
from ..circuit_builder import build_circuit
import sinter


@dataclass(frozen=True)
class SweepPlan:
    sweep_id: str
    code_builder: str
    noise_model: str
    noise_definition: str
    params: dict[str, Any] | None
    basis: str
    distances: list[int]
    ps: list[float]

    def as_dict(self) -> dict[str, Any]:
        return {
            "sweep_id": self.sweep_id,
            "code_builder": self.code_builder,
            "noise_model": self.noise_model,
            "noise_definition": self.noise_definition,
            "noise_params": self.params,
            "basis": self.basis,
            "distances": self.distances,
            "ps": self.ps
        }


def build_sweep_plans(config: Config) -> list[SweepPlan]:
    # Noise parameters * basis * code_builders -> 1 Plan
    # 1 Plan generates 1 sweep figure
    plans = list()

    for sweep in config.sweeps:
        params = config.noise.params.copy() if config.noise.params is not None else dict()
        params["basis"] = sweep.basis
        params["code_builder"] = [code.builder for code in config.codes]
        keys = params.keys()
        values = params.values()
        combinations = [dict(zip(keys, combination)) for combination in product(*values)]

        ps: list[float] | None = None
        if sweep.p.mode == WINDOW_MODE:
            for center, combination in zip(sweep.p.centers, combinations):
                ps = build_p_window(center, sweep.p.half_width, sweep.p.step)
                basis = combination.pop("basis", None)
                code_builder = combination.pop("code_builder", None)
                plans.append(SweepPlan(
                    sweep_id=sweep.id,
                    code_builder=code_builder,
                    noise_model=config.noise.model,
                    noise_definition=config.noise.definition,
                    params=combination,
                    basis=basis,
                    distances=sweep.distances,
                    ps=ps
                ))

        elif sweep.p.mode == LINSPACE_MODE:
            for combination in combinations:
                ps = build_p_linspace(sweep.p.start, sweep.p.stop, sweep.p.num)
                basis = combination.pop("basis", None)
                code_builder = combination.pop("code_builder", None)
                plans.append(SweepPlan(
                    sweep_id=sweep.id,
                    code_builder=code_builder,
                    noise_model=config.noise.model,
                    noise_definition=config.noise.definition,
                    params=combination,
                    basis=basis,
                    distances=sweep.distances,
                    ps=ps
                ))

        elif  sweep.p.mode == LIST_MODE:
            for combination in combinations:
                ps = sweep.p.values
                basis = combination.pop("basis", None)
                code_builder = combination.pop("code_builder", None)
                plans.append(SweepPlan(
                    sweep_id=sweep.id,
                    code_builder=code_builder,
                    noise_model=config.noise.model,
                    noise_definition=config.noise.definition,
                    params=combination,
                    basis=basis,
                    distances=sweep.distances,
                    ps=ps
                ))

    return plans  

    
def plan_to_tasks(plan: SweepPlan) -> list[sinter.Task]:
    # Build sinter tasks from 1 sweep plan
    tasks = list()
    
    for distance in plan.distances:
        code = build_code(plan.code_builder, distance=distance)
        for p in plan.ps:
            noise = build_noise(plan.noise_channel, p, plan.params)
            circuit = build_circuit(
                builder=plan.noise_model,
                code=code,
                noise=noise,
                basis=plan.basis,
                rounds=None # TODO take this value from YAML connfig
            )

            dem = circuit.detector_error_model(
                decompose_errors=True,
                approximate_disjoint_errors=True
            )

            tasks.append(sinter.Task(
                circuit=circuit,
                detector_error_model=dem,
                json_metadata={
                    "d": distance,
                    "p": p,
                    "sweep_id": plan.sweep_id,
                    "code": plan.code_builder,
                    "basis": plan.basis,
                    "noise_model": plan.noise_model,
                    "noise_channel": plan.noise_channel,
                    **plan.params,
                },
            ))

    return tasks
