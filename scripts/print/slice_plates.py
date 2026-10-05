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

import argparse
import json
import subprocess
import sys
from pathlib import Path

from slicer_backends import BACKENDS


def run(cmd):
    print("+", " ".join(str(x) for x in cmd))
    subprocess.run(cmd, check=True)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve(path, repo_root):
    p = Path(path)
    if p.is_absolute():
        return p
    return repo_root / p


def get_plate_input(data, plate_name, input_type, repo_root):
    paths = data["paths"]

    if input_type == "3mf":
        template = paths["plate_3mf_template"]
    elif input_type == "combined_stl":
        template = paths["combined_stl_template"]
    else:
        raise RuntimeError(f"Unsupported input_type: {input_type}")

    return resolve(template.format(plate=plate_name), repo_root)


def build_plate(data, plate_name, slicer_name, printer_name, material_name, repo_root):
    if slicer_name not in BACKENDS:
        raise RuntimeError(f"Unsupported slicer backend: {slicer_name}")

    input_type = data["slicers"][slicer_name].get("input_type", "3mf")
    input_file = get_plate_input(data, plate_name, input_type, repo_root)

    if not input_file.exists():
        raise RuntimeError(f"Input plate does not exist: {input_file}")

    output_dir = resolve(
        Path(data["paths"]["output_dir"]) / slicer_name / printer_name / material_name,
        repo_root,
    )
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{plate_name}-{printer_name}-{material_name}"

    print(output_file)

    cmd = BACKENDS[slicer_name](
        printer=data["slicers"][slicer_name]["printers"][printer_name],
        material_name=material_name,
        input_file=input_file,
        output_file=output_file,
    )
    print("")
    print(f"Slicing plate: {plate_name}")
    print(f"Slicer:        {slicer_name}")
    print(f"Target:        {printer_name}:{material_name}")
    print(f"Input:         {input_file}")
    print(f"Output:        {output_file}")
    print(cmd)

    run(cmd)


# "Main"
parser = argparse.ArgumentParser()

group_plates = parser.add_mutually_exclusive_group(required=True)

group_plates.add_argument("--plate", help="Single plate name, e.g. frame")

group_plates.add_argument("--all-plates", action="store_true", help="Slice all plates")

group_slicers = parser.add_mutually_exclusive_group(required=True)

group_slicers.add_argument(
    "--slicer", help="Select one supported slicer, e.g. prusaslicer"
)

group_slicers.add_argument("--all-slicers", action="store_true", help="Use all slicers")

group_printers = parser.add_mutually_exclusive_group(required=True)

group_printers.add_argument(
    "--printer", help="Select a supported printer, e.g. coreone"
)

group_printers.add_argument(
    "--all-printers", action="store_true", help="Use all printers"
)

parser.add_argument(
    "--repo-root", default=".", help="Repo root. Default: current directory."
)

args = parser.parse_args()

repo_root = Path(args.repo_root).resolve()
targets_path = resolve("mechanical/prints/targets.json", repo_root)

print(targets_path)

data = load_json(targets_path)

# Iterate through all wanted plated
if args.all_plates:
    plate_names = data["plates"]
else:
    plate_names = [args.plate]

for plate_name in plate_names:

    # Iterate through all wanted slicers
    if args.all_slicers:
        slicer_names = list(data["slicers"].keys())
    else:
        slicer_names = [args.slicer]

    for slicer_name in slicer_names:

        # Iterate through all wanted printers
        if args.all_printers:
            printer_names = list(data["slicers"][slicer_name]["printers"].keys())
        else:
            printer_names = [args.printer]

        for printer_name in printer_names:

            # Iterate through all defined materials
            material_names = list(
                data["slicers"][slicer_name]["printers"][printer_name][
                    "materials"
                ].keys()
            )

            for material_name in material_names:

                # Apply only if material is selected
                material = data["slicers"][slicer_name]["printers"][printer_name][
                    "materials"
                ][material_name]

                if plate_name in material.get("plates", []):

                    print(
                        plate_name
                        + ":"
                        + slicer_name
                        + ":"
                        + printer_name
                        + ":"
                        + material_name
                    )

                    build_plate(
                        data=data,
                        plate_name=plate_name,
                        slicer_name=slicer_name,
                        printer_name=printer_name,
                        material_name=material_name,
                        repo_root=repo_root,
                    )
