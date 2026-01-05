# Unit Specifications for Intersection Number Algorithm

These specifications break down the Intersection Number algorithm into atomic, testable units for clean-room implementation and debugging.

## Units
1.  [[project_docs/clean_room/specs/UNIT_LINEAR_RELATIONS.md|Linear Relations Matrix]]: Correct construction from GLSM charge matrix.
2.  [[project_docs/clean_room/specs/UNIT_KNOWN_INTERSECTIONS.md|Known Intersections]]: Fractional values from simplex determinants.
3.  [[project_docs/clean_room/specs/UNIT_VARIABLE_ENUMERATION.md|Variable Enumeration]]: Pruning strategy for self-intersections.
4.  [[project_docs/clean_room/specs/UNIT_EQUATION_CONSTRUCTION.md|Equation Construction]]: The exact linear system equations.
5.  [[project_docs/clean_room/specs/UNIT_ORIGIN_AND_BASIS.md|Origin & Basis]]: Post-processing steps.

## Debugging Guide
Use these specs to verify each step of the Rust implementation independently.
If the final result is wrong, check which unit fails its verification criteria.
