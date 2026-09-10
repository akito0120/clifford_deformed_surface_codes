from codes.registry import registered_codes, build_code
from codes.builtin import *

def main() -> int:
    print(registered_codes())

    css = build_code("rotated_surface", distance=3)
    xzzx = build_code("xzzx", distance=3)
    print(css)
    print(xzzx)
    return 0
