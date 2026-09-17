from ..codes.definition import CodeDefinition
from ..circuit_builder.code_capacity import CodeCapacityBuilder
from pathlib import Path
from ..noise.builtin import depolarizing_noise


def render_diagrams(
    output_dir: Path,
    codes: list[CodeDefinition],
    code_ids: list[str]
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    for code, code_id in zip(codes, code_ids):
        circuit = CodeCapacityBuilder(code, depolarizing_noise(0.1, None)).build()
        detslice = circuit.diagram("detslice-svg")
        timeline = circuit.diagram("timeline-svg")

        detslice_path = output_dir / f"{code_id}_d{code.distance}_detslice.svg"
        timeline_path = output_dir / f"{code_id}_d{code.distance}_timeline.svg"

        detslice_path.write_text(str(detslice))
        timeline_path.write_text(str(timeline))
