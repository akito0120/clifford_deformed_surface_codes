# Introduction Outline

## Motivation
- Quantum computers promise speedups for some problems, but physical qubits fail far too often for
  long computations. Quantum error correction (QEC) encodes one logical qubit in many physical ones
  and corrects errors faster than they accumulate
- The surface code is the leading candidate: it needs only nearest-neighbour interactions on a
  two-dimensional grid and tolerates comparatively high error rates. Its cost is overhead: reaching
  the error rates useful algorithms need takes on the order of a thousand physical qubits per
  logical qubit
- In many hardware platforms errors are not symmetric. Dephasing (Z errors) dominates, and in cat
  qubits the bias is engineered on purpose. A code tailored to such noise could reach the same
  protection with fewer qubits
- Clifford deformations change which Pauli each check measures on each qubit while keeping the
  lattice, the qubit count and the measurement schedule. They are an inexpensive way to tailor the
  surface code to the noise

## Problem statement
- The family is large: $6^n$ deformations of a code with n data qubits, of which $3^n$ remain distinct
  under the usual Z-biased noise model. Only a few members, notably the XZZX and XY codes, have been
  studied in depth
- Published results for these codes were obtained under different boundary conditions, noise
  levels, noise conventions and decoders, so they cannot be compared directly
- Studying a new deformation at the circuit level means building a new syndrome-extraction circuit,
  deciding which detectors are valid at the time boundaries, checking that the schedule preserves
  the distance, and running a full sampling and analysis pipeline. Done by hand for each code, every
  step is a source of silent errors
- What is missing is a way to define an arbitrary deformation once, verify that its circuits are
  correct, and compare it with other codes under identical conditions

## Research questions
- RQ1 (Design): Can circuits for any Clifford deformation of the rotated surface code, at the
  code-capacity, phenomenological and circuit levels, be generated automatically from a definition
  in the stabilizer formalism?
- RQ2 (Correctness): Which checks are sufficient to guarantee that the generated circuits are
  correct, and do the circuits reproduce known results?
- RQ3 (Usefulness): Does the framework make it practical to add a new deformation and compare it
  with existing codes under identical conditions?

## Approach
- A code is declared by its stabilizer generators, logical operators, extraction schedule and
  per-qubit deformation. The framework validates the declaration, builds the memory-experiment
  circuits, samples and decodes them, and estimates the threshold, the suppression factor and the
  teraquop footprint. A single configuration describes, and reproduces, an entire study
- Figure: the pipeline from code definition to analysis results

## Contributions
- A framework that builds memory-experiment circuits at three noise levels for any Clifford
  deformation of surface codes, from a definition in the stabilizer formalism
- A validation method that combines algebraic checks on the code with circuit-level checks on
  detectors and distance
- A case study comparing CSS, XZZX, and partially deformed codes under identical conditions
- An open-source implementation that records configuration and environment for reproducibility

## Scope
- In scope: static codes, whose checks are the same in every round; one logical qubit; the
  two-dimensional lattice; single-qubit Clifford deformations of data qubits; Pauli noise;
  memory experiments; matching-based decoders
- Out of scope: Floquet and other dynamic codes, logical operations such as lattice surgery,
  optimal (maximum-likelihood) decoders, and non-Pauli (coherent) noise
- Give the reason for each limit in one clause, e.g. static checks are what allow detectors to be
  generated automatically, and one logical qubit keeps comparisons fair

## Thesis outline
- Chapter 2. Background: introduces the background: stabilizer codes, the surface code, noises, decoding,
  Clifford deformations and the measures of code performance
- Chapter 3. Related Work: reviews related work on surface codes and on simulation tools (could be merged into chapter 2)
- Chapter 4. Design: presents the design of the framework and its validation method
- Chapter 5. Implementation: describes the implementation
- Chapter 6. Evaluation: evaluates correctness, extensibility and a case study, answering RQ1–RQ3
- Chapter 7. Discussion: discusses the results and their limitations
- Chapter 8. Conclusion and Future Work: concludes and outlines future work
