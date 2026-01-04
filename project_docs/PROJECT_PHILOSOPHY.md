# Project Philosophy: The Knowledge Base

This document captures the core principles of the String Theory Project. It is adapted from the "ChatToMap" philosophy but tailored for scientific research and formal verification.

## Core Principle: Nothing Is Ever Lost

**Every piece of information is captured, organized, and preserved.**

In scientific research, "failed" experiments are as valuable as successful ones. In formal verification, a failed proof attempt teaches us about the structure of the problem.

### How It Works

1.  **Additive-Only**: We never delete history. We only append.
2.  **Feedback & Research**: Raw notes go into `research/` or `feedback/`. They stay there forever.
3.  **Triage**: We synthesize raw notes into `prds/`, `project_docs/`, or `todo/`. The original source remains as the "raw data".

## Document-First Development

**Write it down before you build it.**

1.  **Hypothesis**: Captured in `research/`.
2.  **Plan**: Triage to `prds/` or `design/`.
3.  **Tasks**: Create `todo/` items.
4.  **Implement**: Code follows documentation.

## Component-Based TODOs

**Each component has its own TODO list. Items are checked off, never deleted.**

- `todo/cyrus/`: Tasks for the Rust toolkit.
- `todo/string_theory/`: Tasks for the Search logic.
- `todo/project/`: Internal tasks for this Knowledge Base.

## Separated but Linked

**Code lives in code repos. Knowledge lives here.**

- **Code Repos** (`cyrus`, `string_theory`): Focus on implementation, tests, and commit history of the *code*.
- **Project Repo** (This repo): Focus on PRDs, Research, TODOs, and Architecture.

We link them via symlinks (`project/` in code repos points here), so you can reference docs while coding, but they evolve in separate git histories.

## Strict Rigor (Non-Negotiable)

**In Physics and Formal Verification, "almost right" is wrong.**

- **No Shortcuts**: Do not use approximations without explicit justification.
- **Formal Proof**: If a property is critical, verify it with Aeneas.
- **Reproducibility**: Results must match published literature exactly.
- **Source Integrity**: Prefer `.tex` sources for papers. PDF-to-text conversion is a last resort, as it can corrupt mathematical formulas.

## Engineering Standards

### 1. Exactness at Decision Boundaries
**Floating point is forbidden for geometric decision making.**
- Orientation tests (sign of determinant), convex hull visibility, and triangulation flips must use **exact arithmetic** (Integers or Rationals).
- A wrong sign in a determinant doesn't just mean a small error; it changes the topology of the manifold.
- **Rule**: Heights and lattice points are Integers. Determinants are Integers.

### 2. The "No Cheating" Rule
We do not hardcode constants from papers unless they are universal constants (like $\pi$ or $\zeta(3)$). Every derived value (e.g., $W_0$, $g_s$) must be computed from first principles within the pipeline.
