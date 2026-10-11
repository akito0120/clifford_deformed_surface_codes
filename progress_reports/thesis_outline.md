# Background Outline

## Qubits and Quantum Circuits

### Qubits

- Qubit state is in Hilbert space $\mathbb{C}^2$
- Superposition
- $n$ qubit register live in a space of dimension $2^n$
- Entanglement (those states that do not factor)

### Quantum Circuits

- Gates are unitary and reversible
- Measurement is the only irreversible element; return a random outcome and collapse the state
- One qubit takes part in at most one gate in each time step

---

## The Paulis and Clifford Groups

### Pauli Groups

- 1-qubit Pauli group: I, X, Y, Z and their products
- Any two Paulis either commute or anticommute
- n-qubit Pauli Group: tensor products of Pauli operators with phase
- Two n-qubit Pauli operators anticommute when they anticommute on an odd number of qubits
- The weight of an operator: the number of qubits on which a Pauli operator acts non-trivially

### Clifford Groups

- The Clifford group is the normalizer of the Pauli group: conjugation maps Paulis to Paulis
- A single-qubit Clifford permutes the operators X, Y, Z
- H, S and CNOT generate the whole Clifford group
- Gottesman–Knill theorem: Clifford circuits are efficiently simulable classically, which is what makes the simulation possible at all

---

## Noise in Quantum Systems

### Error Sources and Their Discretization

- Decoherence, imperfect gates, faulty readout, and error accumulated while a qubit idles
- Physical errors are continuous, yet correction must be a discrete choice
- Any single-qubit error expands in the Pauli basis, and measuring the checks of a code projects it onto one Pauli error
- Consequence: it suffices to study Pauli noise

### Pauli Channels

- A Pauli channel applies X, Y or Z with fixed probabilities; the total rate is p
- Two-qubit gates need a two-qubit channel over the fifteen non-identity Pauli pairs, because a gate correlates the errors on its operands
- Bit-flip and phase-flip channels as the two one-parameter special cases
- The depolarizing channel: X, Y and Z each with probability p/3
- Biased noise: in many devices dephasing dominates relaxation, so Z errors are far more likely than X or Y

---

## Stabilizer Codes

### Fundamental Idea

- 3 Challenges: No-cloning forbids keeping copies, measurement collapses the state, errors are continuous
- Encode a logical qubit in a subspace of a larger register
- Syndrome measurement: measure parities that reveal whether an error occurred, and where, but nothing about the encoded state
- Measuring the syndrome discretize the continuous error
- Decoding: correction is then a classical inference problem: from the syndrome, decide what to apply

### Stabilizer Formalism

- Stabilizer group: an abelian subgroup of the Pauli group not containing −I
- Stabilizer generators: an independent set whose products give the whole stabilizer group
- The generators are exactly the checks that will be measured in syndrome measurement
- The code space is the simultaneous +1 eigenspace of all generators
- An error anticommuting with a generator flips that generator's outcome → Error detected

### The Three-Qubit Repetition Code

- Encoding $\ket0$ and $\ket1$ as three-qubit strings, with two parity checks ZZI and IZZ
- The syndrome table and the corresponding correction

---

## The Surface Code

### The Rotated Surface Code

- d × d data qubits on a square lattice, one check per plaquette in a checkerboard of X and Z type. Checks have weight four; neighbouring X and Z plaquettes share two qubits and commute
- Open boundaries with weight-two checks: Z-type along the top and bottom, X-type along the left and right
- A logical operator is a string spanning the lattice between two boundaries of the same type
- Logical X and logical Z run perpendicular and cross an odd number of times, hence anticommute
- The distance equals the length of the shortest such string, and therefore the lattice size

### Syndrome Extraction

- The ancilla is prepared in the X basis; the controlled-Pauli gates write the eigenvalue of the generator onto its phase, and measuring the ancilla in the X basis reads that phase back out
- The outcome is the eigenvalue of the stabilizer generator and nothing more, so the encoded state survives
- The order of those controlled gates is a scheduling choice, constrained by the rule that a qubit takes part in one gate per time step
- The measurement is itself noisy, so a single round of outcomes cannot be trusted → Multiple rounds of syndrome extraction is needed
- Two-qubit gates let a single ancilla fault spread into a two-qubit hook error; a poor schedule aligns hooks with the logical operator and roughly halves the circuit-level distance.

---

## Decoding

### The Decoding Problem

- Input: the set of detection events. Output: a guess at the logical class of the error
- Many distinct errors give the same detection events, and they fall into classes differing by a stabilizer; the target is the most likely class, not the most likely individual error
- If the measurement is noisy, we have multiple rounds of syndrome extraction. Data error is an edge in the space direction, and the measurement error is an edge in the time direction

### Error Chains

- Closed chain: acts trivially on the code space; cannot be detected, but harmless
- Open chain: Two endpoints of the chain appears as detection events; detectable error
- Spanning chain: A chain spanning from one boundary to the other of the lattice; undetectable, but harmful → Logical error

### Decoders

- Different decoders have different accuracy and speed
- MWPM decoder: pair up detection events at minimal total weight. Exact minimum-weight solution in polynomial time, the standard baseline for the surface code
- Union-find decoder: grows clusters until they resolve locally. Near-linear time, at some cost in accuracy
- Belief matching decoder: reweights the graph using the full error model first. More accurate, considerably slower

---

## Clifford Deformed Surface Codes

### Definition

- Apply a single-qubit Clifford to a subset of data qubits, relabeling the Paulis on that qubit, and conjugate every check by that relabeling
- The preparation and measurement basis of each data qubit transforms along with them, and with it the choice of time-boundary detectors
- The controlled gate on each leg follows the new Pauli (CX, CY or CZ); the ancillas and their basis are unchanged
- The lattice, the qubit count and the schedule are untouched, and deformations

### Biased Noise and Necessity of Clifford Deformation

- The standard surface code treats X and Z symmetrically, so it does not exploit the error bias
- Clifford deformed surface codes might exploit the error bias
- e.g. XZZX code: H on one checkerboard sublattice of data qubits, so every check reads XZZX. A Z error then flips checks along one diagonal only, and under pure dephasing the code decouples into independent repetition codes. Its threshold grows with bias
- e.g. XY code: $\sqrt{X}$ on every data qubit turns the Z checks into Y checks. XY code under Z-biased noise is the CSS code under Y-biased noise
- Deforming each of the n data qubits by one of six single-qubit Cliffords gives a family of 6ⁿ codes. Symmetries of the noise make many of them equivalent: 3ⁿ classes remain under Z-biased noise with $p_X = p_Y$, and a single class under depolarizing noise. Which deformation performs best can depend on the bias, as well as on the figure of merit and the decoder

---

## Memory Experiment and Quantifying Results

### Memory Experiment

- The experiment that measures how well a code stores a qubit
- Prepare the logical state, repeat syndrome extraction for a number of rounds, read out the data, then decode → Success or failure
- X memory and Z memory: preparing and reading in one basis tests protection against the complementary error type, and the two can behave very differently for the same code
- Round count is conventionally proportional to the distance, balancing space and time protection

### Logical Error Rate

- Each shot is a Bernoulli trial, so $p_L$ is estimated as failures/shots
- The Wilson interval behaves well near zero
- Per shot ( $p_L$ ) and per round ( $\epsilon$ ) differ: The per-round rate is needed whenever runs of different R = d are compared

### Threshold

- The threshold is the physical error rate below which increasing d decreases $p_L$; curves for different d cross there
- Threshold can be mapped to the phase transitions in statistical mechanics
- Finite-size scaling: near the crossing $p_L$ is a function of $x = (p − p_{th}) d^{(1/ν)}$.
- A threshold belongs to the code, the circuit model, the noise parameters and the decoder jointly

### Suppression and Teraquop Footprint

- Below threshold $\epsilon \propto \Lambda^{(−(d+1)/2)}$, and $\Lambda = \epsilon(d)/\epsilon(d+2)$ is the return on adding qubits.
- It is read off as the slope of $\log \epsilon$ against $(d+1)/2$, which for odd d is the same as a fit against d
- The teraquop footprint is the number of qubits needed for an error rate of $10^{-12}$ over a d-round memory: extrapolate the fit to the d at which it reaches the target and round up to an odd d