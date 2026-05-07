<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 3D-Print Guide - NOTES

### 3) 3D print the frame

Use 3MF projects in hardware/mechanical/exports/3mf/ or follow manifest.csv.
STL/STEP are in hardware/mechanical/exports/{stl,step}/.
Follow docs/printing.md for materials, orientation, and post‑processing.

0) ensure that 3D printer calibration for elephant foot and over-/under-extrusion is done!
- See the section [Printed Parts](#printed-parts) for material and settings.
- Follow instructions
- STL and 3MF files are in hardware/exports/ and hardware/prints/3mf/.
- See mechanical/prints/README.md for recommended materials, orientations, and slicer profiles.
- Download STL/STEP: mechanical/exports/{stl,step}/
- Optional: use provided 3MF projects for a known-good profile.

- Verify printed parts match dimensions (critical hole diameters, arm thickness).

Printed parts
- See ../../hardware/mechanical/exports/stl/ and manifest.csv for settings
- Recommended materials: PC/CF (frame), and PETG (color-coding parts)
1) Print parts according to manifest and 3MF projects.
2) Install heat-set inserts (where specified).

## 3D printing guidance

- Use the 3MF projects to capture intended orientation, supports, and modifiers.
- Typical settings (starting point; see manifest.csv for part-specific):
  - Nozzle: 0.4 mm; Layer: 0.20 mm
  - Walls: 4; Top/Bottom: 6; Infill: 35-50% (gyroid) for arms
  - Material: PC/CF-Nylon
- Tolerances (rule of thumb):
  - Write values in params/default.yaml
- Test coupons: test/coupons/ includes hole ladders and insert gauges.

## Printed Parts

- Recommended materials:
  - PC-CF or ABS for the drone's frame (separte 3mf project file)
  - PETG for color-coding/cosmetic parts (separte 3mf project file)
- Baseline settings (see part notes and screenshots in docs/printing/):
  - Nozzle: 0.4 mm
  - Layer height: 0.2 mm (first layer 0.3mm)
  - Perimeters: 4
  - Top Solid layers: 6
  - Bottom Solid layers: 6
  - Infill: 20% Gyroid
  - Orientation: each STL is oriented “as printed”
- Slicer profiles:  
  Provided 3MF projects for [PrusaSlicer](https://github.com/prusa3d/prusaslicer) in hardware/prints/3mf/ with per‑category settings.
- Heat‑set inserts: sizes and temperatures in part notes (docs/printing/) - README.md
- Post‑processing in hardware/prints/README.md (threaded inserts); post‑processing (reaming, tapping, heat‑set insert temperatures); removal of support.

- Files:
  - Editable: hardware/freecad/parts/*.FCStd
  - Interchange: hardware/exports/step/*.step
  - Mesh: hardware/exports/stl/*.stl
  - Slicer projects: hardware/prints/3mf/


