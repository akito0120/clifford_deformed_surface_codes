from .code_capacity import CodeCapacityBuilder
from .phenomenological import PhenomenologicalBuilder
from .circuit_level import CircuitLevelBuilder


BUILDERS: dict[str, type] = {
    "code_capacity": CodeCapacityBuilder,
    "phenomenological": PhenomenologicalBuilder,
    "circuit_level": CircuitLevelBuilder,
}
