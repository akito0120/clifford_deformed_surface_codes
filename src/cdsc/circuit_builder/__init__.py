from .code_capacity import CodeCapacityBuilder
from .phenomenological import PhenomenologicalBuilder
from .circuit_level import CircuitLevelBuilder
import stim
from ..codes.definition import CodeDefinition, Pauli
from ..noise.noise_model import NoiseModel


BUILDERS: dict[str, type] = {
    "code_capacity": CodeCapacityBuilder,
    "phenomenological": PhenomenologicalBuilder,
    "circuit_level": CircuitLevelBuilder,
}


CODE_CAPACITY = "code_capacity"
PHENOMENOLOGICAL = "phenomenological"
CIRCUIT_LEVEL = "circuit_level"


def build_circuit(
    builder: str,
    code: CodeDefinition, 
    noise: NoiseModel, 
    basis: Pauli,
    rounds: int | None = None,
) -> stim.Circuit:
    if builder == CODE_CAPACITY:
        return CodeCapacityBuilder(code, noise, basis).build()
    elif builder == PHENOMENOLOGICAL:
        return PhenomenologicalBuilder(code, noise, rounds, basis).build()
    elif builder == CIRCUIT_LEVEL:
        return CircuitLevelBuilder(code, noise, rounds, basis).build()
    
    raise ValueError("invalid circuit buillder specified")
