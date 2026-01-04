# Polytope Selection and Mirror Symmetry

## The h21 Constraint: Why McAllister Chose "Asymmetric" Polytopes

All examples in McAllister et al. (arXiv:2107.09064) have **small h21**:

| Polytope ID | h21 | h11 | Notes |
|-------------|-----|-----|-------|
| 4-214-647 | 4 | 214 | Primary example |
| 5-113-4627 | 5 | 113 | |
| 5-81-3213 | 5 | 81 | |
| 7-51-13590 | 7 | 51 | |

This is not a coincidence. **Small h21 is required for tractable computation.**

## Mirror Symmetry: Primal vs Dual

For a reflexive polytope, we get two Calabi-Yau manifolds related by mirror symmetry:

```
Primal CY (X):     h11 = 214,  h21 = 4
Mirror CY (X̃):    h11 = 4,    h21 = 214
```

Mirror symmetry exchanges:
- Kähler moduli (h11) ↔ Complex structure moduli (h21)
- Kähler cone ↔ Complex structure moduli space
- Intersection numbers κ_ijk ↔ Yukawa couplings

## Which Polytope for Which Computation?

Different pipeline stages require different sides of the mirror:

### PRIMAL (h11=214) - Kähler Geometry
Used for:
- **V_string** = (1/6) κ_ijk t^i t^j t^k - BBHL
- **Divisor volumes** τ_i = ∂V/∂t^i
- **Kähler cone** membership

Why: These involve Kähler moduli t^i, of which there are h11=214.

### DUAL/MIRROR (h11=4) - Complex Structure
Used for:
- **e^K₀** = (4/3) × (κ̃_abc p^a p^b p^c)^(-1)
- **Flat direction** p from flux (K, M)
- **Racetrack stabilization** for W₀

Why: These involve complex structure moduli, which on the mirror become Kähler moduli. Working on the mirror with h11=4 means only 4 moduli to handle.

## Why Small h21 is Essential

### 1. Flux Lattice Search (h21 dimensions)
The flux vectors K, M ∈ Z^{h21} must satisfy:
- Tadpole constraint: (1/2) K·M ≤ L (typically L ~ 500)
- Perturbative flatness conditions
- Small W₀ requirement

For h21=4, we search a 4-dimensional lattice.
For h21=100, we'd search a 100-dimensional lattice - intractable.

### 2. Mirror Intersection Numbers
The e^K₀ formula uses mirror intersection numbers κ̃_abc where a,b,c ∈ {0,...,h21-1}:
- h21=4: Only 4³ = 64 possible entries (sparse)
- h21=100: 100³ = 1,000,000 entries

### 3. Racetrack Complexity
The racetrack superpotential sums over curves:
```
W = W₀ + Σ A_q exp(-2πi q·T)
```
The number of relevant curves grows with h21.

## Polytope ID Convention

The naming "4-214-647" means:
- **4**: h21 = 4
- **214**: h11 = 214
- **647**: Index in Kreuzer-Skarke database for this (h21, h11) pair

## Computing the Dual Polytope

For a reflexive polytope Δ, the dual Δ° is defined by:
```
Δ° = { y ∈ M_R : ⟨x, y⟩ ≥ -1 for all x ∈ Δ }
```

The vertices of Δ° correspond to facets of Δ, and vice versa.

CYTools provides both:
```python
poly = Polytope([[1,0,0,0], [0,1,0,0], ...])  # primal points
dual_poly = poly.dual()  # automatically computed
```

In our fixtures:
- `polytope.json` contains both `primal_points` (294) and `dual_points` (12)
- The dual has fewer points because h21 < h11

## Implications for the GA Pipeline

### For General Search
When the GA explores random polytopes, we should:
1. **Filter by h21**: Only consider polytopes with h21 ≤ ~10 for tractability
2. **Precompute both sides**: Store primal AND dual intersection numbers
3. **Use appropriate side**: Route each computation to correct polytope

### For McAllister Validation
The fixture data includes:
- `points.dat` / `dual_points.dat`: Both polytopes
- `dual_simplices.dat`: Triangulation of the DUAL
- `basis.dat`: Divisor basis for the dual (dim=4)

We need to be careful about which intersection numbers we're using:
- `intersection.json` in our fixtures has dim=4 → this is the DUAL
- For V_string, we need primal intersection numbers (dim=214)

## The "Balanced" Polytope Problem

A polytope with h11 ≈ h21 ≈ 100 would be problematic:
- **Primal side**: 100 Kähler moduli - manageable
- **Dual side**: 100 complex structure moduli - manageable
- **Flux search**: 100-dimensional lattice - INTRACTABLE

The real bottleneck is the **discrete flux search**, not the continuous geometry.

This is why the landscape search focuses on "long thin" polytopes where one of h11 or h21 is small.

## Summary

| Computation | Uses | Why |
|-------------|------|-----|
| V_string, τ_i | Primal (h11=214) | Kähler moduli |
| e^K₀, p, W₀ | Dual (h11=4) | Complex structure → mirror Kähler |
| Flux search | N/A | Scales with h21, must be small |

**Key insight**: McAllister didn't choose these polytopes because they're special geometrically - he chose them because **small h21 makes the flux search tractable**.
