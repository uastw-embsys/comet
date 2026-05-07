DESCRIBE NAMING CONVENTION OF 3D PRINT FILES

# PrusaSlicer assets

This folder contains PrusaSlicer project files and presets for printing the drone parts reproducibly.

Use these assets to import a ready-to-print configuration bundle, or pick per-printer/per-material presets and 3MF projects with saved orientations, supports, and modifier meshes.

Build: PrusaSlicer-2.9.4+flathub.org

## Contents

- bundle: prusaslicer-bundle-v1.ini        # All-in-one bundle for quick import
- printers/, filaments/, print-profiles/
  - Individual presets (.ini) you can import selectively.
- projects/
  - Per-part PrusaSlicer projects (.3mf) with locked orientation, supports, and modifiers.
- plates/ (optional)
  - Multi-part plates for batch printing spares.
- gcode/ (optional)
  - Pre-sliced G-code for specific machines/profiles. See safety note.
- screenshots/
  - Reference images showing part orientation, supports, and modifiers.

Naming convention: PART__PRINTER__MATERIAL__LAYERHEIGHT__vREV.EXT
- Example: ARM-L__MK4__PETG__0p20__v1.3mf

## Requirements

- PrusaSlicer ≥ 2.6 (or SuperSlicer recent release)
- Nozzle size: 0.4 mm unless stated otherwise in filename or project notes
- Verified printers: list your tested machines here (e.g., Prusa MK4, MK3S+, Bambu X1C via generic profile)

## Quick start: Import the full config bundle

1) Open PrusaSlicer.
2) File → Import → Import Config Bundle…
3) Select bundles/OpenPrintDrone_bundle.ini.
4) In the top toolbar, choose:
   - Printer: pick the imported printer profile (e.g., Prusa MK4 0.4).
   - Filament: choose the intended filament (e.g., PETG Generic).
   - Print Settings: choose the matching quality (e.g., 0.20mm QUALITY).
5) File → Open Project… and pick a 3MF from projects/ (e.g., ARM-L__MK4__PETG__0p20__v1.3mf).
6) Confirm that:
   - The printer, filament, and print settings match the 3MF filename.
   - Nozzle size and layer height are correct.
   - Supports/modifiers are present as shown in screenshots/.

Then slice and review the preview (top layers, bridges, support interfaces) before exporting G-code.

## Alternative: Import individual presets

If you prefer not to import a full bundle:

- Import printer preset:
  - File → Import → Import Config… → select a .ini from printers/
- Import filament preset:
  - File → Import → Import Config… → select a .ini from filaments/
- Import print profile:
  - File → Import → Import Config… → select a .ini from print-profiles/
- Open a part project from projects/ and ensure the three selectors (Printer, Filament, Print Settings) are set to the intended presets.

## Material guidance (recommendations)

- Arms and structural parts: PETG or PA-CF/Nylon (for higher heat and stiffness). PA-CF requires a dry filament and preferably an enclosure.
- Camera/FPV damped parts: TPU (use dedicated flexible print profile).
- Plates/covers: PETG or PLA+ if thermals are low; prefer PETG for field durability.

Typical baseline settings (override as needed in your profiles):
- Perimeters: 4–6 on arms; 3–4 on covers.
- Infill: 20–35% grid/gyroid for covers; 40–60% for arms; increase sparse infill overlap to strengthen walls.
- Supports: Only where needed; interface layers enabled; avoid supports inside insert holes.
- Holes for M3: model nominal 3.0–3.1 mm, then drill/ream to 3.2 mm post-print for best fit.

## Orientation and supports

- Use the provided 3MF orientation; it is chosen to:
  - Align layer lines with load paths on arms.
  - Keep insert bosses vertical to reduce ovalization.
  - Minimize supports in critical surfaces.
- See screenshots/ for each part’s preview and support strategy.
- If you change orientation, review:
  - Bridge cooling, overhang quality, and strength along layer lines.

## Heat-set inserts and post-processing

- Heat-set inserts (e.g., M3):
  - Recommended tip temp: follow insert manufacturer (typically 250–280 °C for PETG, lower for PLA).
  - Use a printed alignment jig if included; press vertically without twisting.
- Hole finishing:
  - Clear pilot holes with a 3.0 mm drill; ream to 3.2 mm for M3 clearance if required.
- Threaded holes:
  - If tapping printed threads, reduce tapping torque and back off frequently to avoid delamination.

## Using optional G-code (if present)

- Provided G-code is for a specific machine and profile at the time of release.
- You MUST verify:
  - Bed and nozzle temperatures suit your filament brand.
  - Start/end G-code matches your printer (bed leveling, purge lines, flow calibration).
  - Fan, chamber, and accessory controls are correct for your hardware.
- If in doubt, re-slice from the 3MF using your known-safe profiles.

## Safety and liability notice

- 3D printers and UAVs can cause injury and property damage.
- Always:
  - Supervise prints; ensure proper ventilation for materials that emit fumes.
  - Validate temperatures, speeds, and adhesives on your hardware.
  - Inspect printed parts for defects, poor layer adhesion, or warping before flight.
  - Use threadlocker where indicated; torque fasteners per the build manual.
  - Follow local regulations for UAV operation; perform ground checks and a gentle maiden flight.
- Any G-code and settings are provided without warranty; you assume responsibility for safe operation.

## Versioning and compatibility

- 3MF and presets are versioned to match hardware releases (e.g., v1.0.0).
- If a part geometry or critical setting changes, the filename revision (vX) increases.
- Check CHANGELOG.md for notes affecting print settings or orientation.

## Troubleshooting

- Layers splitting or weak arms:
  - Dry filament thoroughly; increase nozzle temperature by 5–10 °C; add perimeters; consider higher enclosure temperature.
- Insert holes too tight/loose:
  - Ream to size after printing; adjust “hole_xy_compensation” in the print profile; use the tolerance test coupon if provided.
- Stringing or blobs:
  - Reduce nozzle temp slightly; tune retraction; enable wipe and coasting if compatible with your printer.
- Overly long print times:
  - Switch to SPEED profile or 0.28 mm layers where acceptable; maintain perimeters for strength.

## How to contribute

- For new printers/filaments:
  - Export your tuned presets (.ini) and a sample 3MF for one part.
  - Follow the naming convention and place files in the appropriate subfolders.
  - Add a short note to this README under “Verified printers” and open a pull request.
- Large binary files:
  - .3mf and .gcode should be tracked with Git LFS.
  - Example .gitattributes entries:
    ```
    *.3mf filter=lfs diff=lfs merge=lfs -text
    *.gcode filter=lfs diff=lfs merge=lfs -text
    ```

## Links

- Printing notes and per-part tips: link to docs/printing/part-notes.md
- Build manual: link to docs/build-manual/
- Issue tracker for print problems: link to repository issues
