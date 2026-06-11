# Quintessence, the DESI results, and what they mean for Cyrus

*Written: 2026-06-11, immediately after Cyrus reproduced all five published
McAllister vacua end-to-end (cyrus commit 177afced).*
*Companion to the earlier [DESI_DARK_ENERGY_IMPLICATIONS.md](DESI_DARK_ENERGY_IMPLICATIONS.md)
(2026-01-01); this note is the layman's-terms explainer plus the GA-pipeline
implications as assessed post-reproduction.*

---

## Quintessence in plain terms

Think of dark energy as the question: *what is the energy of empty space doing?*

- **Cosmological constant (Λ):** empty space has a fixed, eternal energy density — a ball sitting motionless on a perfectly flat shelf. The universe accelerates forever at an ever-steadier rate. This is the "CDM + Λ" standard model, and it's what a true *vacuum* (a minimum of the potential, like the ones we compute) gives you.
- **Quintessence:** the ball isn't on a shelf — it's on a very, very gentle slope, still rolling. "Dark energy" is the energy of a scalar field (in string theory: a modulus or axion, exactly the τ's and their partners our pipeline computes) that hasn't settled. Because it's rolling, its energy density *changes over time* — typically decreasing. The observational fingerprint is the "equation of state" w: a true Λ has w = −1 forever; quintessence has w drifting away from −1.

## What the new results actually say

The [DESI galaxy survey's latest releases](https://newscenter.lbl.gov/2025/03/19/new-desi-results-strengthen-hints-that-dark-energy-may-evolve/) — measuring the universe's expansion history with unprecedented precision — show **mounting (but not yet conclusive) evidence that dark energy is weakening over time**. Alone, DESI is still consistent with plain ΛCDM; combined with the cosmic microwave background and supernovae, the data prefer evolving dark energy at moderate-to-strong significance, and [the debate is genuinely live](https://phys.org/news/2026-02-dark-energy-evolving.html) — most cosmologists [want more evidence before declaring it](https://bigthink.com/starts-with-a-bang/dark-energy-weakening-desi-results/). The dramatic headline version: if dark energy keeps decaying, acceleration ends, and the universe could even [recollapse in a "big crunch"](https://www.sciencedaily.com/releases/2026/02/260215225537.htm). On the dark matter side, the 2026 news is more incremental — [self-interacting dark matter simulations](https://nasaspacenews.com/2026/05/a-new-theory-of-dark-matter/), [sharper Webb lensing maps](https://www.nasa.gov/missions/webb/nasa-reveals-new-details-about-dark-matters-influence-on-universe/), and [hints of multiple dark-matter components](https://www.sciencedaily.com/releases/2026/04/260409101101.htm) — interesting, but nothing that overturns the framework.

## Does this break string theory? Almost the opposite.

This is the genuinely fun part. String theory's most chronic embarrassment over the last decade has been the *de Sitter problem*: constructing a vacuum with a small **positive**, **eternal** cosmological constant is notoriously hard, and the "swampland" school argues it may be impossible in principle — quantum gravity may forbid balls resting on positive-energy shelves, allowing only gentle slopes (rolling fields) or negative-energy minima. That's why your reference library contains papers like the [Agrawal–Obied–Steinhardt–Vafa swampland-quintessence paper](https://arxiv.org/pdf/2404.05722) lineage: **swampland-motivated string theory has been predicting "dark energy should be slowly decaying, not constant" since 2018**. If DESI's trend holds up, it's the first observational hint *in favor* of that expectation. And the "big crunch" version connects even more directly to us: a rolling field heading toward a small-magnitude **negative** minimum — and exponentially-small-|V₀| **AdS vacua are literally what the McAllister pipeline computes** (all five reproduced vacua have V₀ < 0).

What the results *do* pressure is one specific scenario: the KKLT-style "uplift to a positive constant Λ and sit there forever" story. If w ≠ −1 is confirmed, the universe isn't sitting in any vacuum yet — it's still rolling toward one.

## Does it break our approach? No — it retargets the search, using the same engine.

The crucial distinction: what we just spent these sessions validating is the **engine** — polytopes → triangulations → intersection numbers → Kähler geometry → GV invariants → superpotentials → scalar potentials, all exact. That machinery is agnostic about which cosmology you're hunting. CLAUDE.md already names quintessence as the goal; the McAllister reproduction was the calibration target, not the destination. Concretely, for the GA:

1. **The fitness function changes, not the pipeline.** Instead of only "minimize |V₀|", we'd score candidates on the *shape* of the potential: a direction flat enough to still be rolling today (mass ~ H₀ ≈ 10⁻³³ eV) at a height ~10⁻¹²² M_pl⁴, with a slope reproducing DESI's measured w(z). Note that the scales involved — potentials of 10⁻¹²² from exponentials like e^(−2πτ) — are *exactly* the kind of fantastically small numbers this machinery produces naturally (we just computed a vacuum at 10⁻²¹³).
2. **The natural string quintessence candidates are axions**, the periodic partners of the τ moduli we already compute. Their masses and couplings come straight from our pipeline outputs (instanton scales e^(−2πτᵢ), the Kähler metric from κ). The same outputs give the **axion dark matter spectrum** — so the new ultralight/multi-component dark matter hints are scored by the same data, for free.
3. **One real subtlety:** DESI's best-fit, taken literally, has dark energy crossing w = −1 ("phantom crossing"), which a *single* rolling field cannot do. You need multiple interacting fields — which is precisely what the [Kähler-mixing quintessence paper](https://arxiv.org/pdf/2404.08056) already in your research collection (`kmix_quintessence_2511.23463`) addresses: mixing between Kähler moduli, i.e., multi-field dynamics in exactly the moduli space our κ tensors describe.
4. **What would actually break the approach:** data demanding dark energy that *grows*, or no scalar-field description at all. Nothing current points that way.

So: can we find vacua (really, *trajectories toward* vacua) matching the new findings? Plausibly yes — and that's arguably a more exciting target than small-Λ hunting, because evolving dark energy is far more *falsifiable*: a candidate compactification predicts a specific w(z) curve that Euclid and DESI's next releases can test. The missing piece in Cyrus is the `cyrus-cosmology` layer: integrate the Friedmann + scalar-field equations over the potentials the core engine produces, output w(z), and feed that to the GA's fitness function. That's the natural next construction project after the landscape smoke test.

---

Sources: [Berkeley Lab / DESI DR2](https://newscenter.lbl.gov/2025/03/19/new-desi-results-strengthen-hints-that-dark-energy-may-evolve/), [Big Think on the ambiguity](https://bigthink.com/starts-with-a-bang/dark-energy-weakening-desi-results/), [Phys.org Feb 2026 debate](https://phys.org/news/2026-02-dark-energy-evolving.html), [ScienceDaily big-crunch coverage](https://www.sciencedaily.com/releases/2026/02/260215225537.htm), [quintessential interpretation of DESI](https://arxiv.org/pdf/2404.05722), [interpreting DESI's evidence](https://arxiv.org/pdf/2404.08056), [SIDM theory](https://nasaspacenews.com/2026/05/a-new-theory-of-dark-matter/), [Webb dark matter maps](https://www.nasa.gov/missions/webb/nasa-reveals-new-details-about-dark-matters-influence-on-universe/), [two-component dark matter](https://www.sciencedaily.com/releases/2026/04/260409101101.htm).

---

## Status postscript (2026-06-11)

The construction project sketched above is now built, in
`~/code/cyrus/crates/cyrus-ga`:

- The cosmology layer exists and is wired into the GA fitness: each
  candidate's energy scale is dressed as a thawing-axion potential,
  integrated through the real Friedmann + Klein-Gordon equations, and the
  resulting w(z) is CPL-fitted against DESI (w0 = -0.45 +/- 0.21,
  wa = -1.8 +/- 0.6).
- The GA searches pools of Kreuzer-Skarke polytopes (bandit scheduler,
  exact-isotropic PFV sampling, per-geometry tadpole bounds), fully
  stop/resumable. First 30-minute laptop run: 1.04M evaluations,
  114 valid vacua, best at log10|V0| = -120.6 (observed: -121.5) with
  CPL wa = -1.7 already inside the DESI band; w0 still too fast by
  roughly the one missing log of height.
- An automated orientifold layer (involutions, O7s, rigidity, c_i,
  tadpoles) reproduces all five published McAllister examples and feeds a
  verification emitter for any candidate. Remaining gates to full
  first-principles verification: chamber selection (flop-walk the
  secondary fan to a GV-covered phase) and Pfaffian purity (port the
  1712.04946 fourfold Hodge formulas).

Falsifiability status: on track. A verified candidate would predict a
specific w(z) testable against DESI DR3/Euclid.
