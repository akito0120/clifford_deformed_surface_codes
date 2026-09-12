from .codes.registry import build_code
from .codes.builtin import *
from .noise import NoiseModel
from .circuit_builder.circuit_level import CircuitLevelBuilder
from .validation.validate import validate_codes, validation_report
import json
from .config import load_config

def main() -> int:
    css = build_code("rotated_surface", distance=3)
    xzzx = build_code("xzzx", distance=5)
    codes = [css, xzzx]

    # Validation
    result = validate_codes(codes)
    report = validation_report(result)
    print(json.dumps(report, indent=2))

    # Code definitions
    print(css)
    print(xzzx)

    # Circuit
    noise = NoiseModel(p=0.1, channel="biased", eta=10)
    circuit = CircuitLevelBuilder(code=xzzx, noise=noise, basis='X').build()
    print(str(circuit))

    config = load_config("configs/smoke.yaml")
    print(config)

    return 0
