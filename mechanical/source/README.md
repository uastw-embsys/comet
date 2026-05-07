<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->
# Source README

This directory contains the “Source” for the hardware design — the preferred form for making modifications — as required by the CERN Open Hardware License v2 (CERN‑OHL‑W).

What this means
- The FreeCAD `*.FCStd` files here are editable project sources.
- Generated artifacts (STL/STEP/3MF) live under `../exports/` and are not the canonical editing form.
- If you redistribute Products based on this design, you must provide a notice pointing to this Source and license.

## Contents and conventions

- parts/
  - One manufacturable part per `*.FCStd`
  - Each file has a top‑level Body with a stable Label (e.g., `mounting_plate`, `rotor_arm`)
  - Parameters stored in a Spreadsheet object (Label: `params`), referenced by aliases (e.g., `'m3_hole_diameter_clearance`, `'threaded_insert_outer_diameter`)
- assemblies/
  - Assembly files (e.g., Assembly3) linking parts via `App::Link`
  - Local Coordinate Systems (LCS) used for constraints
- params/
  - YAML parameter sets (e.g., `default.yaml`, variant files)

FreeCAD version
- Designed and tested with 1.1.0.44227 +568 (Git) Snap 2266. Other versions may work but are not guaranteed.

## Editing guidelines

- Avoid attaching sketches/features to generated faces (topological naming issue). Use Datum planes/axes and LCS.
- Keep a “master sketch” per part for core layout; parameterize via the `params` Spreadsheet.
- Apply fillets/chamfers late in the feature tree.
- Name key features (e.g., `Sketch_Master`, `Pad_Main`, `Hole_M3_Insert`) for clarity.
- Update revision numbers (R#) in file names and meta when geometry changes.

## Parameters and variants

- Default parameters are stored in each part’s `params` Spreadsheet.
- Variant sets live under `params/variants/`. Load them before recompute/export (see scripts).
- Typical aliases:
  - `m3_hole_diameter_clearance`, `threaded_insert_outer_diameter`, etc.

## Assemblies

- Use stable Labels in parts so assembly links don’t break.
- Constrain via LCS‑to‑LCS where possible.
- Keep sub‑assemblies (e.g., `motor_block`) separate and link into the main assembly.

## Exporting

- Exports are generated headless via `freecad.cmd` using `scripts/export_freecad.py`.
- STL/STEP/3MF are written to `../exports/`.
- Do not hand‑edit exports; modify the `*.FCStd` source and re‑export.

## Licensing

- SPDX for source files: `CERN-OHL-W-2.0`
- Include license and source URL in FreeCAD document metadata:
  - Document → Properties → Meta → `License = CERN-OHL-W-2.0`
  - `Comment = Source: https://github.com/uastw-embsys/comet`
- Full license text: `LICENSES/LICENSE.CERN-OHL-W-2.0.txt`

Third‑party models

- External CAD (e.g., GrabCAD) must be segregated under `third-party/` with clear attribution and original license. These files are not covered by CERN‑OHL‑W unless explicitly stated.
- See `LICENSES/THIRD-PARTY-NOTICES.md` for details.

## Contributing

- Edit `*.FCStd` in `parts/` or `assemblies/` only; keep exports in sync via scripts.
- Add/maintain parameter aliases for new features.
- Run validation scripts (dimension/mesh checks) before submitting PRs.
- Use SPDX headers in text files and keep meta info updated in `*.FCStd`.