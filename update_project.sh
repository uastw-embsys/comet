#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# Update FreeCAD parts based on part_parameters.yaml
# Export into 3D formats.
# Create build plates based on Layout
. docker/run_container_ci_mode.sh scripts/cad/apply_parameters.py \
                                  scripts/cad/export_source.py \
                                  'scripts/cad/generate_plates.py --pass mechanical/prints/layouts/frame.layout.json mechanical/prints/layouts/color-coding.layout.json mechanical/prints/layouts/clearance-gauge.layout.json'