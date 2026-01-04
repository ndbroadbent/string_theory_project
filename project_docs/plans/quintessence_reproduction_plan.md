# Plan: Reproduce "From Inflation to Quintessence" (Cicoli et al. 2024)

## Goal
Reproduce the quintessence cosmology results from [arXiv:2407.03405](https://arxiv.org/abs/2407.03405) to validate our pipeline against DESI observations.

**Target**: Match the numerical example in Section 4.5.
- **Model**: K3-fibred Calabi-Yau in LVS (Large Volume Scenario).
- **Moduli**:
  - $\tau_1 \approx 1.324$ (Fibre modulus)
  - $\tau_2 \approx 1122$ (Base modulus)
  - $\mathcal{V} \approx 900$
  - $g_s = 0.1$
  - $|W_0| = 1$
- **Observables**:
  - Dark Energy Scale: $\Lambda_1^4 \approx 10^{-120} M_p^4$
  - Decay Constant: $f_1 \approx 0.085 M_p$
  - Axion Mass: $m_1 \sim 10^{-32}$ eV

## Why This Paper?
Unlike McAllister (KKLT), which seeks a *static* de Sitter vacuum (disfavored by DESI), Cicoli constructs *dynamic* Dark Energy (Quintessence) using an ultralight axion rolling down a potential. This fits the $w(z) > -1$ hint from DESI.

## Implementation Steps

### Phase 1: LVS Potential Implementation
LVS differs from KKLT. We need to implement the LVS scalar potential:
$$V_{LVS} = \frac{3 \xi |W_0|^2}{4 g_s^{3/2} \mathcal{V}^3} + \text{soft terms} $$
This requires:
1.  **$\alpha'$ corrections ($\xi$)**: Computed from Euler characteristic $\chi$.
2.  **Volume $\mathcal{V}$**: Already implemented in `cyrus-core`.
3.  **Moduli Stabilization**: Find minimum for volume modulus $\mathcal{V}$, but leave axions light.

### Phase 2: Quintessence Potential
Implement the effective potential for the quintessence axion $\phi$:
$$V(\phi) = \Lambda^4 \left( 1 - \cos\left(\frac{\phi}{f}\right) \right) $$
1.  **Decay Constant $f$**: Derived from the CY metric (already in `cymyc` or computable via `cyrus-core` intersection numbers).
2.  **Scale $\Lambda^4$**: Derived from non-perturbative superpotential terms ($e^{-S}$).

### Phase 3: Cosmology Solver
Solve the Friedmann-Klein-Gordon equations to get $w(z)$:
$$\ddot{\phi} + 3H\dot{\phi} + V'(\phi) = 0 $$
$$H^2 = \frac{1}{3M_p^2} (\rho_m + \rho_\phi) $$
1.  Use `ode_solvers` (Rust) or `ScalPy` (Python bridge).
2.  Compute $w(z) = P_\phi / \rho_\phi$ and compare with DESI contours.

## Reusing Existing Work
- **`cyrus-core`**:
    - **Triangulation/Intersections**: CRITICAL. Used to compute $\mathcal{V}$ and kinetic terms $K_{i\bar{j}}$.
    - **Exact Arithmetic**: Essential for small numbers ($e^{-100}$). 
- **Deprecated**:
    - `compute_v0` (KKLT specific): Replace with `compute_v_lvs`.
    - `solve_racetrack` (KKLT specific): Replace with LVS stabilization + Axion dynamics.

## Next Immediate Task
Create `crates/cyrus-core/src/lvs.rs` to implement the LVS potential and stabilization logic.
