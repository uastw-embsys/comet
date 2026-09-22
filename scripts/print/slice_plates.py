#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>
"""
DOCUMENTATION
"""

__version__ = "1.0.0"
__author__ = "Christoph Böhm"
__contact__ = "christoph.boehm@ieee.org"
__copyright__ = "2026 Christoph Böhm"
__license__ = "LGPL-3.0-or-later"

import argparse
import json
import subprocess
import sys
from pathlib import Path


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


def get_plate_input(plate_spec, input_type, repo_root):
    if input_type == "3mf":
        return resolve(plate_spec["3mf"], repo_root)

    if input_type == "combined_stl":
        return resolve(plate_spec["combined_stl"], repo_root)

    raise RuntimeError(f"Unsupported input_type: {input_type}")


def prusaslicer_command(target, input_file, output_file, repo_root):
    exe = target.get("executable", "prusa-slicer")
    profile = resolve(target["profile"], repo_root)

    cmd = [
        exe,
        "--load",
        str(profile),
        "--export-gcode",
        "--output",
        str(output_file),
    ]

    options = target.get("options", {})

    if options.get("dont_arrange", True):
        cmd.append("--dont-arrange")

    cmd.append(str(input_file))

    return cmd


def orcaslicer_command(target, input_file, output_file, repo_root):
    """
    OrcaSlicer CLI is version/platform dependent.
    This is intentionally similar to PrusaSlicer, but verify with:

        orcaslicer --help
    """
    exe = target.get("executable", "orcaslicer")
    profile = resolve(target["profile"], repo_root)

    cmd = [
        exe,
        "--load",
        str(profile),
        "--export-gcode",
        "--output",
        str(output_file),
    ]

    options = target.get("options", {})

    if options.get("dont_arrange", True):
        cmd.append("--dont-arrange")

    cmd.append(str(input_file))

    return cmd


def superslicer_command(target, input_file, output_file, repo_root):
    exe = target.get("executable", "superslicer")
    profile = resolve(target["profile"], repo_root)

    cmd = [
        exe,
        "--load",
        str(profile),
        "--export-gcode",
        "--output",
        str(output_file),
    ]

    options = target.get("options", {})

    if options.get("dont_arrange", True):
        cmd.append("--dont-arrange")

    cmd.append(str(input_file))

    return cmd


def cura_command(target, input_file, output_file, repo_root):
    """
    Example CuraEngine backend.

    This expects target["profile"] to point to a simplified JSON file like:

    {
      "definition": "mechanical/prints/profiles/cura/ender3.def.json",
      "settings": {
        "layer_height": "0.2",
        "infill_sparse_density": "20"
      }
    }
    """
    exe = target.get("executable", "CuraEngine")
    profile_path = resolve(target["profile"], repo_root)
    profile = load_json(profile_path)

    definition = resolve(profile["definition"], repo_root)
    settings = profile.get("settings", {})

    cmd = [
        exe,
        "slice",
        "-v",
        "-j",
        str(definition),
        "-o",
        str(output_file),
    ]

    for key, value in settings.items():
        cmd += ["-s", f"{key}={value}"]

    cmd += ["-l", str(input_file)]

    return cmd


BACKENDS = {
    "prusaslicer": prusaslicer_command,
    "orcaslicer": orcaslicer_command,
    "superslicer": superslicer_command,
    "cura": cura_command,
}


def build_plate(data, target_name, plate_name, repo_root):
    targets = data["targets"]
    plates = data["plates"]

    if target_name not in targets:
        raise RuntimeError(f"Unknown target: {target_name}")

    if plate_name not in plates:
        raise RuntimeError(f"Unknown plate: {plate_name}")

    target = targets[target_name]
    plate = plates[plate_name]

    slicer = target["slicer"]

    if slicer not in BACKENDS:
        raise RuntimeError(f"Unsupported slicer backend: {slicer}")

    input_type = target.get("input_type", "3mf")
    input_file = get_plate_input(plate, input_type, repo_root)

    if not input_file.exists():
        raise RuntimeError(f"Input plate does not exist: {input_file}")

    output_dir = resolve(target["output_dir"], repo_root)
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{plate_name}.gcode"

    cmd = BACKENDS[slicer](
        target=target,
        input_file=input_file,
        output_file=output_file,
        repo_root=repo_root,
    )

    print("")
    print(f"Slicing plate: {plate_name}")
    print(f"Target:        {target_name}")
    print(f"Slicer:        {slicer}")
    print(f"Input:         {input_file}")
    print(f"Output:        {output_file}")

    run(cmd)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--targets",
        default="mechanical/prints/targets.json",
        help="Path to targets.json",
    )

    parser.add_argument(
        "--target",
        required=True,
        help="Target name from targets.json, e.g. prusaslicer-coreone-pccf",
    )

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("--plate", help="Single plate name, e.g. frame")

    group.add_argument("--all-plates", action="store_true", help="Slice all plates")

    parser.add_argument(
        "--repo-root", default=".", help="Repo root. Default: current directory."
    )

    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    targets_path = resolve(args.targets, repo_root)

    data = load_json(targets_path)

    if args.all_plates:
        plate_names = list(data["plates"].keys())
    else:
        plate_names = [args.plate]

    for plate_name in plate_names:
        build_plate(
            data=data,
            target_name=args.target,
            plate_name=plate_name,
            repo_root=repo_root,
        )


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print("")
        print("build_prints.py failed:")
        print(exc)
        sys.exit(1)
