#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>
"""
Common code snippets and variables across scripts.

Usage:
    freecad.cmd -c scripts/apply_parameters.py

License: LGPL-3.0-or-later
See the LICENSE file (or https://www.gnu.org/licenses/lgpl-3.0.txt).
"""

__version__ = "1.0.0"
__author__ = "Christoph Böhm"
__contact__ = "christoph.boehm@ieee.org"
__copyright__ = "2026 Christoph Böhm"
__license__ = "LGPL-3.0-or-later"


# Define which parts to apply the parameters to
PARTS = [
    {
        "fcstd": "mechanical/source/tools/clearance_gauge.FCStd",
        "label": "clearance_gauge",
    },
    {
        "fcstd": "mechanical/source/tools/length_ruler.FCStd",
        "label": "length_ruler",
    },
    {
        "fcstd": "mechanical/source/tools/threaded_inserts_helper.FCStd",
        "label": "threaded_inserts_helper",
    },
    {
        "fcstd": "mechanical/source/parts/motor_mount.FCStd",
        "label": "motor_mount",
    },
    {
        "fcstd": "mechanical/source/parts/capacitor_holder.FCStd",
        "label": "capacitor_holder",
    },
    {"fcstd": "mechanical/source/parts/rotor_arm.FCStd", "label": "rotor_arm"},
    {
        "fcstd": "mechanical/source/parts/landing_gear_mount.FCStd",
        "label": "landing_gear_mount",
    },
    {
        "fcstd": "mechanical/source/parts/battery_holder.FCStd",
        "label": "battery_holder",
    },
    {
        "fcstd": "mechanical/source/parts/rc_receiver_mount.FCStd",
        "label": "rc_receiver_mount",
    },
    {
        "fcstd": "mechanical/source/parts/mounting_plate.FCStd",
        "label": "mounting_plate",
    },
    {
        "fcstd": "mechanical/source/parts/quick_release_base.FCStd",
        "label": "quick_release_base",
    },
    {
        "fcstd": "mechanical/source/parts/esc_connector_mount.FCStd",
        "label": "esc_connector_mount",
    },
    {
        "fcstd": "mechanical/source/parts/motor_mount_1mm_spacer.FCStd",
        "label": "motor_mount_1mm_spacer",
    },
    {
        "fcstd": "mechanical/source/parts/motor_mount_2mm_spacer.FCStd",
        "label": "motor_mount_2mm_spacer",
    },
    {"fcstd": "mechanical/source/parts/handle.FCStd", "label": "handle"},
    {
        "fcstd": "mechanical/source/parts/xt30_male_mount.FCStd",
        "label": "xt30_male_mount",
    },
    # {
    #     "fcstd": "mechanical/source/parts/template_part.FCStd",
    #     "label": "template_part",
    # },
]

PARAMS_FILE = "mechanical/source/part_parameters.yaml"
