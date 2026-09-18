#!/usr/bin/env bash
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>

# Update FreeCAD parts based on part_parameters.yaml and export into 3D formats.

. docker/run_container_ci_mode.sh scripts/apply_parameters.py scripts/export_source.py