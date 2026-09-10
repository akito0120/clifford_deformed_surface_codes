from .codes.registry import registered_codes, build_code
from .codes.checks import run_checks
from .codes.builtin import *
from .noise import NoiseModel
from .circuit_builder.circuit_level import CircuitLevelBuilder 

def main() -> int:
    print(registered_codes())

    css = build_code("rotated_surface", distance=3)
    xzzx = build_code("xzzx", distance=3)
    print(css)
    print(xzzx)

    results = run_checks(xzzx)
    for result in results:
        print(result.as_json())

    noise = NoiseModel(p=0.1, channel="biased", eta=10)
    circuit = CircuitLevelBuilder(code=xzzx, noise=noise, basis='X').build()
    print(str(circuit))

    return 0
