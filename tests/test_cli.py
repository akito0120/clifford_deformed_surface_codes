import pytest
import yaml
from cdsc import cli


CONFIG = {
    "experiment": {"name": "test"},
    "codes": ["rotated_surface"],
    "noise": {"model": "code_capacity", "definition": "depolarizing", "p_meas": "same_as_p"},
    "sweeps": [{"id": "sweep", "distances": [3, 5], "basis": ["X"], "p": {"mode": "list", "values": [0.05]}}],
    "sampling": {"decoder": "mwpm", "max_shots": 100, "max_errors": 10, "max_batch_size": 100, "workers": 1},
    "threshold": {"source_sweep": "sweep", "distances": [3, 5], "x_window": 0.1, "nu_0": 1.1},
    "suppression": {"source_sweep": "sweep", "target_pl": 1e-12},
    "output": {"dir": "unused"},
}


# run-all runs every step in order on one loaded config, and stops at the first step that fails
@pytest.mark.parametrize("failing", [None, "validate", "analyze"])
def test_run_all_runs_the_steps_in_order_and_stops_at_the_first_failure(tmp_path, monkeypatch, failing):
    path = tmp_path / "config.yaml"
    path.write_text(yaml.safe_dump(CONFIG))

    calls = []

    def fake(step):
        def handler(config, args):
            calls.append((step, config))
            return cli.EXIT_FAILED if step == failing else cli.EXIT_OK
        return handler

    # The fakes stand in for the real steps, so nothing is sampled or written
    for step in cli.RUN_ALL_STEPS:
        monkeypatch.setitem(cli.HANDLERS, step, fake(step))

    exit_code = cli.main(["run-all", str(path)])

    steps = list(cli.RUN_ALL_STEPS)
    expected = steps if failing is None else steps[: steps.index(failing) + 1]
    assert exit_code == (cli.EXIT_OK if failing is None else cli.EXIT_FAILED)
    assert [step for step, _ in calls] == expected
    assert all(config is calls[0][1] for _, config in calls)
