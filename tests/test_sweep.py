from itertools import product
from pytest import approx
from cdsc.circuit_builder import build_circuit
from cdsc.codes.registry import build_code
from cdsc.config import Config
from cdsc.noise.registry import build_noise
from cdsc.sweep.run import build_sweep_plans, plan_to_tasks


CENTERS = [0.006, 0.007, 0.008, 0.009]
HALF_WIDTH = 0.001


def _config() -> Config:
    return Config.model_validate({
        "experiment": {"name": "test"},
        "codes": ["rotated_surface", "xzzx"],
        "noise": {
            "model": "circuit_level",
            "definition": "biased",
            "params": {"eta": [0.5, 10]},
            "p_meas": "same_as_p",
        },
        "sweeps": [{
            "id": "window",
            "distances": [3, 5],
            "basis": ["X"],
            "p": {"mode": "window", "centers": CENTERS, "half_width": HALF_WIDTH, "step": 0.0005},
        }],
        "sampling": {"decoder": "mwpm", "max_shots": 100, "max_errors": 10, "max_batch_size": 100, "workers": 1},
        "threshold": {"source_sweep": "window", "distances": [3, 5], "x_window": 0.1, "nu_0": 1.1},
        "suppression": {"source_sweep": "window", "target_pl": 1e-12},
        "output": {"dir": "unused"},
    })


# Plans come out in the documented order, each sweeping the window around its own center
def test_plans_follow_the_documented_order_and_centers():
    # NOTE: params vary slowest, code fastest; centers are given in that order
    plans = build_sweep_plans(_config())
    assert [(plan.params["eta"], plan.code) for plan in plans] == [
        (0.5, "rotated_surface"),
        (0.5, "xzzx"),
        (10, "rotated_surface"),
        (10, "xzzx"),
    ]
    for plan, center in zip(plans, CENTERS):
        assert min(plan.ps) == approx(center - HALF_WIDTH)
        assert max(plan.ps) == approx(center + HALF_WIDTH)
        assert plan.basis == "X"
        assert plan.distances == [3, 5]


# Every task's metadata describes the circuit the task actually carries
def test_task_labels_match_the_circuit_they_carry():
    plan = build_sweep_plans(_config())[3]
    tasks = plan_to_tasks(plan)

    labels = [(task.json_metadata["d"], task.json_metadata["p"]) for task in tasks]
    assert sorted(labels) == sorted(product(plan.distances, plan.ps))

    for task in tasks:
        meta = task.json_metadata
        assert (meta["code"], meta["basis"], meta["eta"]) == ("xzzx", "X", 10)
        noise = build_noise("biased", meta["p"], {"eta": meta["eta"]})
        expected = build_circuit("circuit_level", build_code(meta["code"], distance=meta["d"]), noise, meta["basis"])
        assert task.circuit == expected
