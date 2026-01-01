# Cyrus Tasks

## Formal Verification
- [ ] **Intersection Tensor** (`intersection.rs`)
    - [ ] Prove `canonical_key` is idempotent and symmetric.
    - [ ] Prove `symmetry_multiplicity` counts permutations correctly.
    - [ ] Prove `contract_triple` sum correctness.
- [ ] **Divisor Volumes** (`divisor.rs`)
    - [ ] Prove gradients match Jacobian.
- [ ] **Flat Direction** (`flat_direction.rs`)
    - [ ] Prove linear system solution correctness.

## Core Features
- [ ] Optimize `contract_triple` for sparse intersection tensors.
- [ ] Implement self-optimizing cache tiers in `cyrus-cache`.
- [ ] **Port CYTools Logic**:
    - [ ] Implement FRST triangulation (or integrate a Rust library).
    - [ ] Implement intersection number computation ($\kappa_{ijk}$).
    - [ ] Implement Kähler cone determination.
- [ ] **Port Physics Logic**:
    - [ ] Implement RG flow for gauge couplings (`GaugeCouplingComputer`).
    - [ ] Implement full KKLT potential with uplift (`ModuliStabilizer`).

## Validation
- [ ] Validate 5-81-3213 example against McAllister data.
- [ ] Validate 5-113-4627 example.
