# PRD: String Theory Playground

## Overview
A web-based interactive dashboard for exploring Calabi-Yau compactifications. It allows researchers to manually tweak moduli, fluxes, and discrete choices to see immediate physics feedback.

## Goals
1.  **Interactive Debugging**: Manually step through the `physics_bridge` logic.
2.  **Education**: Visualize how changing a flux integer shifts the vacuum.
3.  **Validation**: compare our results against "Gold Standard" points (McAllister).

## Features
- **Polytope Selector**: Choose from KS database or upload vertices.
- **Moduli Sliders**: Tweak $t^i$ (Kähler) and $z^a$ (Complex).
- **Flux Input**: Matrix input for $F_3, H_3$.
- **Real-time Feedback**:
    - $V_{CY}$, $V_{divisor}$.
    - Gauge couplings $\alpha^{-1}$.
    - $W_{flux}$, $V_{scalar}$.
- **Visualization**: 2D projection of the Kähler cone and current ray.

## Technical Stack (Tentative)
- **Backend**: Rust (via `cyrus` crate, possibly WASM?).
- **Frontend**: React/Svelte.
- **Data**: SQLite for caching evaluations.
