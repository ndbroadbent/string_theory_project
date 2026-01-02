# ScalPy Clean-Room Implementation Specifications

This document provides high-level mathematical and algorithmic descriptions of the functionality provided by the `scalpy` library (https://github.com/sum33it/scalpy). These descriptions are derived from general cosmological principles and inspection of the public codebase to serve as a specification for a clean-room implementation in Rust.

## 1. Scalar Field Dynamics

The core functionality is solving the background cosmological evolution of a scalar field $\phi$ coupled to gravity (Friedmann equations).

### dynamical System
The universe is modeled as containing:
1.  **Matter** ($\rho_m \propto a^{-3}$)
2.  **Radiation** ($\rho_r \propto a^{-4}$)
3.  **Scalar Field** ($\rho_\phi, p_\phi$)

The evolution is often solved using $N = \ln a$ as the time variable.

#### Quintessence (Minimally Coupled Scalar Field)
*   **Lagrangian**: $\mathcal{L} = -\frac{1}{2} \partial_\mu \phi \partial^\mu \phi - V(\phi)$
*   **Density**: $\rho_\phi = \frac{1}{2}\dot{\phi}^2 + V(\phi)$
*   **Pressure**: $p_\phi = \frac{1}{2}\dot{\phi}^2 - V(\phi)$
*   **Equation of State**: $w_\phi = \frac{p_\phi}{\rho_\phi} = \frac{\frac{1}{2}\dot{\phi}^2 - V}{\frac{1}{2}\dot{\phi}^2 + V}$

**Equation of Motion (Klein-Gordon)**:
$$ \ddot{\phi} + 3H\dot{\phi} + V'(\phi) = 0 $$

**Friedmann Equation**:
$$ H^2 = \frac{1}{3 M_{pl}^2} (\rho_m + \rho_r + \rho_\phi) $$

### Potentials Supported
1.  **Power Law**: $V(\phi) = \phi^n$
2.  **Exponential**: $V(\phi) = \exp(K\phi)$

### Other Models
*   **Tachyon Field**: Non-canonical kinetic term. $\mathcal{L} = -V(\phi)\sqrt{1 - \partial_\mu \phi \partial^\mu \phi}$.
*   **Galileon Field**: Includes higher-derivative terms (cubic Galileon) preserving second-order equations of motion.

## 2. Cosmological Observables

Once $H(z)$ and $w(z)$ are computed, derived observables are calculated via standard integrals.

### Distance Measures
*   **Hubble Distance**: $D_H = c / H_0$
*   **Normalized Hubble**: $E(z) = H(z)/H_0$
*   **Comoving Distance**:
    $$ D_C(z) = D_H \int_0^z \frac{dz'}{E(z')} $$
*   **Angular Diameter Distance**: $D_A(z) = D_C(z) / (1+z)$
*   **Luminosity Distance**: $D_L(z) = (1+z) D_C(z)$

### Growth of Structure
Linear perturbation theory for matter density contrast $\delta_m$.
**Growth Equation**:
$$ \ddot{\delta} + 2H\dot{\delta} - 4\pi G \rho_m \delta = 0 $$
Converted to $N = \ln a$ derivatives:
$$ \delta'' + \left(2 + \frac{H'}{H}\right)\delta' - \frac{3}{2} \Omega_m(a) \delta = 0 $$
where primes denote $d/dN$.

*   **Growth Rate**: $f = d\ln\delta / d\ln a \approx \Omega_m(z)^\gamma$
*   **fσ8**: $f(z) \sigma_8(z) = f(z) \sigma_8(0) \frac{D_+(z)}{D_+(0)}$

## 3. Parametrized Dark Energy Models

Standard fluid models implemented for comparison:

*   **LCDM**: $w = -1$ (const)
*   **wCDM**: $w = w_0$ (const)
*   **CPL (w0waCDM)**: Chevallier-Polarski-Linder parameterization
    $$ w(a) = w_0 + w_a (1 - a) = w_0 + w_a \frac{z}{1+z} $$
    Dark energy density evolution:
    $$ \rho_{DE}(a) = \rho_{DE,0} \exp\left( 3 \int_a^1 \frac{1+w(a')}{a'} da' \right) $$
    $$ \rho_{DE}(a) = \rho_{DE,0} a^{-3(1+w_0+w_a)} \exp(3 w_a (a-1)) $$

## 4. Initial Condition Solver

To match present-day observations ($\Omega_{\phi,0}, w_0$), the system must solve a "shooting problem".
*   **Inputs**: Target $w_0$, Target $\Omega_{\phi,0}$.
*   **Variables**: Initial conditions at early times (e.g., $\phi_i$, $\lambda_i$).
*   **Method**: Numerical root finding (Newton-Raphson/Hybrd) to find inputs that evolve to the targets.

## 5. Transfer Functions

Analytic approximations for the matter power spectrum $P(k)$.
*   **BBKS**: Bardeen-Bond-Kaiser-Szalay. Suitable for general overview.
*   **Eisenstein-Hu**: Includes Baryon Acoustic Oscillations (BAO) wiggles.

## Rust Implementation Strategy

1.  **ODE Solver**: Use `diffsl` or `ode_solvers` crate.
2.  **Integration**: Use `quadrature` or `simpson` crate for distance integrals.
3.  **Root Finding**: Use `roots` crate or implement Newton-Raphson for the shooting problem.
4.  **Structure**:
    *   `Cosmology` trait defining `H(z)`, `w(z)`, `rho(z)`.
    *   Structs for `Quintessence`, `LCDM`, `CPL`.
    *   Methods for `luminosity_distance(z)`, `growth_factor(z)`.
