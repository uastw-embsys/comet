<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# Documentation Index

Welcome to the COMET documentation! This documentation will guide you through the processes of preparing, printing, assembling, setting up the electronics, configuring, and safely operating the drone.

<div align="center">
    <img src="./assets/renders/comet_rotating.gif" width="50%" float="left">
</div>

Quick Links:
  - Bill of Materials: [docs/bill_of_materials.ods](./bill_of_materials.ods)
  - Printing guide: [docs/printing.md](./printing.md)
  - Build manual: [docs/build.md](./build.md)
  - FCU and ESC configuration: [docs/config.md](./config.md)
  - Safety instructions: [docs/safety.md](./safety.md)

## Software

The following is a list of the software used to create, 3D print, and operate COMET:
- [FreeCAD 1.1.0](https://github.com/FreeCAD/FreeCAD/releases/tag/1.1.0) and [A2plus Workbench 0.4.68](https://github.com/kbwbe/A2plus)
- [Python 3.12.3](https://www.python.org/downloads/release/python-3123/)
- [PrusaSlicer 2.9.4](https://github.com/prusa3d/PrusaSlicer/releases/tag/version_2.9.4)
- [INAV Configurator 8.0.1](https://github.com/iNavFlight/inav-configurator/releases/tag/8.0.1)

[Back to the top &#8593;](#documentation-index)

## Tools

The following is a list of the tools needed to build COMET:
- length ruler (from the 3D-printed frame parts)
- side cutter
- nose plier
- soldering iron, solder, and flux
- 1.5mm allen key
- 2.5mm allen key
- 5.5mm open-jaw wrench
- tweezers
- zip ties (different sizes)
- shrinking tube (different sizes)
- (optional) cable striper
- (optional) threaded inserts melting [aid set](https://www.3djake.com/ruthex/soldering-tips-melting-aid-set?similar_products_d_a=30899)

[Back to the top &#8593;](#documentation-index)

## Quick Start

The following steps will guide you through the process of building your very own COMET drone.

### 1) Get the files

- Download one of the [release ZIPs](https://github.com/uastw-embsys/comet/releases)
- OR clone the repository:
```bash
git clone https://github.com/uastw-embsys/comet.git
```

### 2) Order the non-printable parts

- Refer to the "bill of materials" sheet in [`docs/bill_of_materials.ods`](./bill_of_materials.ods). It contains a detailed list of parts grouped by subassemblies from the build manual.
- Use the "order list" sheet for recommended parts, including filament spools for multiple drones. Don't order filament spools if they're already available.

### 3) 3D print the frame

- Make sure the 3D printer is properly calibrated (e.g., [elephant footing](https://store.anycubic.com/blogs/3d-printing-guides/how-to-fine-tune-z-offset) and [over- or under-extrusion](https://help.prusa3d.com/article/.extrusion-multiplier-calibration_2257)).
- Print the gauge with the frame part filament and update parts based on clearances.
- 3D print the frame and color-code parts:
  - Use 3MF projects in [`mechanical/prints/`](./../mechanical/prints/) that match your slicer and 3D printer
  - OR set up your own slicer project and use the provided projects as a reference.
- Install heat-set inserts where specified.
- For more detailed instructions, refer to the printing guide in [`docs/printing.md`](./printing.md).

### 4) Assemble COMET

- Begin by assembling the individual COMET subassemblies.
- Assemble all subassemblies and finish the wiring.
- Perform final checks to ensure that the build is correct.
- Enjoy your self-built drone!
- For more detailed instructions, refer to the build manual in [`docs/build.md`](./build.md).

### 5) Flash and configure the FCU and ESCs

- Flash the official INAV 8.0.1 to the FCU, then apply the settings in the INAV CLI.
- Calibrate the accelerometer, magnetometer, and radio.
- Use the ESC Configurator to flash the Bluejay firmware onto the ESCs and apply the parameters.
- Verify the failsafes, motor order, and spin directions.
- For more detailed instructions, refer to the FCU and ESC configuration in [`docs/config.md`](./config.md).

### 6) First test flight!

- Perform all checks according to the safety instructions found in the [`docs/safety.md`](./safety.md) file.
- Share your experience and first flight with us!

[Back to the top &#8593;](#documentation-index)
