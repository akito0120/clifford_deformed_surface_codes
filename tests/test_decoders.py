import pytest
import sinter
from cdsc.circuit_builder import build_circuit
from cdsc.codes.registry import build_code
from cdsc.decoder import resolve_decoder
from cdsc.noise.builtin import depolarizing_noise


SHOTS = 2000


@pytest.fixture(scope="module")
def sampled():
    circuit = build_circuit(
        "circuit_level", build_code("rotated_surface", distance=3), depolarizing_noise(0.002, None), "X"
    )
    dem = circuit.detector_error_model(decompose_errors=True, approximate_disjoint_errors=True)
    dets, obs = circuit.compile_detector_sampler(seed=1).sample(SHOTS, separate_observables=True)
    return dem, dets, obs


# Each decoder corrects most of the logical errors in a sampled memory experiment
@pytest.mark.parametrize("name", ["mwpm", "uf", "bp"])
def test_decoder_corrects_most_errors(sampled, name):
    dem, dets, obs = sampled
    decoder, custom_decoders = resolve_decoder(name)
    predictions = sinter.predict_observables(
        dem=dem, dets=dets, decoder=decoder, custom_decoders=custom_decoders
    )
    undecoded = obs.any(axis=1).mean()
    decoded = (predictions != obs).any(axis=1).mean()
    assert decoded < undecoded / 3
