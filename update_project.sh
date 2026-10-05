#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

set -euo pipefail

# Resolve paths regardless of where the script is called from.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="${SCRIPT_DIR}"

# 1) Update the FreeCAD parts based on the part_parameters.yaml file.
# 2) Export to 3D formats.
# 3) Create build plates based on layouts.
# 4) Slice all build plates using all available slicers, printers, and materials.
${REPO_ROOT}/docker/run_ci.sh bash -lc '
    stdbuf -oL -eL FreeCADCmd scripts/cad/apply_parameters.py &&
    stdbuf -oL -eL FreeCADCmd scripts/cad/export_source.py &&
    stdbuf -oL -eL FreeCADCmd scripts/cad/generate_plates.py --pass \
        mechanical/prints/layouts/frame.layout.json \
        mechanical/prints/layouts/color-coding.layout.json \
        mechanical/prints/layouts/clearance-gauge.layout.json &&
    stdbuf -oL -eL python3 scripts/print/slice_plates.py --all-plates --all-slicers --all-printers
'
