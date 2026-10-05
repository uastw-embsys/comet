#!/usr/bin/env python3
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>
"""
DOCUMENTATION
"""

__version__ = "1.0.0"
__author__ = "Christoph Böhm"
__email__ = "christoph.boehm@ieee.org"
__copyright__ = "2026 Christoph Böhm"
__license__ = "LGPL-3.0-or-later"

from pathlib import Path


def command(printer, material_name, input_file, output_file):
    material = printer["materials"][material_name]

    center = printer["center"]
    center_string = f"{center[0]},{center[1]}"

    return [
        "prusa-slicer",
        "--printer-profile",
        printer["printer_profile"],
        "--print-profile",
        printer["print_profile"],
        "--material-profile",
        material["material_profile"],
        "--perimeter-generator",
        "classic",
        str(input_file),
        "--export-gcode",
        "--output",
        str(output_file) + ".bgcode",
        "--dont-arrange",
        "--info",
        "--center",
        center_string,
    ]
