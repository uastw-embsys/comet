<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 3D-Print Guide

This guide covers the calibration, materials and settings, file locations, printing steps, and post-processing of the COMET frame and its accessories.

Find the needed files here:
- Slicer projects (recommended to use): [mechanical/prints/](./../mechanical/prints/)
- Meshes (STL): [mechanical/exports/stl/](./../mechanical/exports/stl/)
- Interchange solids (STEP): [mechanical/exports/step/](./../mechanical/exports/step/)

Naming of the 3MF projects inside the slicer project folders:
- Clearance gauge for pre-print calibration: `clearance-gauge-*.3mf`
- A single print plate is used for all COMET frame parts: `frame-*.3mf`
- Non-functional colored parts: `color-coding-*.3mf`

## Table of Contents
- [Printer Calibration](#printer-calibration)
- [Clearance Gauge](#clearance-gauge)
- [3D Printing](#3d-printing)
- [Post-Processing](#post-processing)
- [Next Step](#next-step)

## Printer Calibration

First, we calibrate the printer with the intended filament to achieve reliable hole clearances, flat first layers, and accurate dimensions within acceptable tolerances. You can skip any steps for which your 3D printer is already calibrated.

### 1) Extrusion Multiplier

- Print a single-wall cube with 0% infill and no top or bottom, then measure the resulting wall thickness as described [here](https://help.prusa3d.com/article/.extrusion-multiplier-calibration_2257).
- Adjust the extrusion multiplier so that the measured wall thickness matches the width of the nozzle (e.g., 0.40 mm for a 0.4 mm nozzle).

### 2) First-layer and Elephant Foot

- Fine-tune the Z-offset to prevent squish ridges and reduce elephant footing while ensuring optimal adhesion. Refer to the provided [examples](https://store.anycubic.com/blogs/3d-printing-guides/how-to-fine-tune-z-offset) for guidance.
- If there is still some elephant footing remaining, set the `elephant_foot_chamfer` parameter in the [mechanical/source/part_parameters.yaml](./../mechanical/source/part_parameters.yaml) file to compensate for it in the CAD files themselves.


### 3) Bed leveling and Adhesion

- Use automatic bed leveling or a [test pattern](https://help.prusa3d.com/article/bed-level-correction_2267) to ensure an even print surface.
- Use a clean, appropriate surface for your material (e.g., the [Prusa Filament Material Guide](https://help.prusa3d.com/filament-material-guide) specifies which print sheets to use).
- The heated bed temperature should be selected based on the type of filament being used. It should not be set too high, but high enough to ensure that the parts adhere to it.

[Back to the top &#8593;](#table-of-contents)

## Clearance Gauge

Recommended for frame, optional for color-coding parts.

Measure your threaded inserts (outer diameter, length, recommended pilot hole) from the datasheet or with calipers, then enter these values into the project’s parameter file (e.g., params/default.yaml). Apply the updated parameters and export a small test coupon: either open the 3MF project that contains the clearance gauge and slice it, or export the relevant STL/3MF to print the test piece.

Print the clearance gauge and determine which categories produce proper fits for M3, M2, and the selected threaded inserts (aim for a smooth, non-loose fit for clearance holes and a firm, pressable fit for insert pilots). Use these results to refine the YAML values if needed. Once satisfied, apply the final parameters and export the full set of parts (3MF preferred to capture orientation and supports, or STL if you manage slicing separately). The parts are now ready to print with the validated clearances.


Dimensional accuracy and clearances

get threaded insert measures, enter them into yaml, then apply & export. 3mf or export to print the test piece

Determine in which clearance category M3, M2, and threaded inserts fit into the clearence gauge.

Input values and apply & export, parts are now ready to print

[Back to the top &#8593;](#table-of-contents)

## 3D Printing

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

Printed parts
- See ../../hardware/mechanical/exports/stl/ and manifest.csv for settings
- Recommended materials: PC/CF (frame), and PETG (color-coding parts)
1) Print parts according to manifest and 3MF projects.
2) Install heat-set inserts (where specified).

- Use the 3MF projects to capture intended orientation, supports, and modifiers.
- Typical settings (starting point; see manifest.csv for part-specific):
  - Nozzle: 0.4 mm; Layer: 0.20 mm
  - Walls: 4; Top/Bottom: 6; Infill: 35-50% (gyroid) for arms
  - Material: PC/CF-Nylon
- Tolerances (rule of thumb):
  - Write values in params/default.yaml
- Test coupons: test/coupons/ includes hole ladders and insert gauges.

<div align="center">
    <img src="./assets/images/finished_3D_print.jpg" width="60%">
    <p>Fig. 1. The finished 3D-printed frame parts were produced using our research group's Prusa CORE One 3D printers. This build plate contains all the parts needed to assemble COMET.</p>
</div>

[Back to the top &#8593;](#table-of-contents)

## Post-Processing

The 3D-printed frame requires the removal of support structures before proceeding. This concerns components battery holder (BH-01), XT30 connector mounts (YF-03), and ESC connector mount (YF-04). The figure below highlights these structures, which can be detached by applying a small amount of force with nose pliers.
<div align="center">
    <img src="./assets/images/supports_to_remove.jpg" width="60%">
    <p>Fig. 2. Spots where the supports need to be removed.</p>
</div>

ADD Threaded insert preperation!.

[Back to the top &#8593;](#table-of-contents)

## Next Step

Assemble COMET using the build manual in [`docs/build.md`](./build.md).

[Back to the top &#8593;](#table-of-contents)