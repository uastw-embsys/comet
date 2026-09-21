#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>
"""
Generate positioned print plate geometry from a layout JSON file.

Run with FreeCADCmd, for example:

    FreeCADCmd scripts/cad/generate_plates.py --pass mechanical/prints/layouts/frame.layout.json mechanical/prints/layouts/color-coding.layout.json mechanical/prints/layouts/clearance-gauge.layout.json

Typical outputs:
    - positioned STL files
    - positioned 3MF file

This script assumes layout part files are already exported meshes, usually STL.

Recommended repo flow:

    FreeCAD source
      -> scripts/freecad/export_source.py
      -> mechanical/exports/stl/*.stl
      -> scripts/freecad/generate_plate.py mechanical/prints/layouts/frame.layout.json
      -> mechanical/prints/generated/plates/frame/...
"""

__version__ = "1.0.0"
__author__ = "Christoph Böhm"
__contact__ = "christoph.boehm@ieee.org"
__copyright__ = "2026 Christoph Böhm"
__license__ = "LGPL-3.0-or-later"

import argparse
import json
import math
import os
import re
import sys
from pathlib import Path

import FreeCAD as App
import Mesh

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------


def log(message):
    App.Console.PrintMessage(str(message) + "\n")


def warn(message):
    App.Console.PrintWarning(str(message) + "\n")


def error(message):
    App.Console.PrintError(str(message) + "\n")


# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------


def resolve_path(path, base_dir):
    """
    Resolve path relative to base_dir unless it is already absolute.
    """
    if path is None:
        return None

    p = Path(path)

    if p.is_absolute():
        return p

    return Path(base_dir) / p


def ensure_parent_dir(path):
    Path(path).parent.mkdir(parents=True, exist_ok=True)


def ensure_dir(path):
    Path(path).mkdir(parents=True, exist_ok=True)


def slugify(name):
    """
    Convert part name to a safe-ish filename.
    """
    name = str(name).strip().lower()
    name = re.sub(r"[^a-z0-9._-]+", "-", name)
    name = re.sub(r"-+", "-", name)
    return name.strip("-") or "part"


# ---------------------------------------------------------------------------
# Layout expansion
# ---------------------------------------------------------------------------


def as_vector3(value, default=None, field_name="vector"):
    if value is None:
        if default is None:
            return [0, 0, 0]
        return list(default)

    if not isinstance(value, list) or len(value) != 3:
        raise RuntimeError(f"{field_name} must be a list of 3 numbers, got: {value!r}")

    return value


def add_vec3(a, b):
    return [
        float(a[0]) + float(b[0]),
        float(a[1]) + float(b[1]),
        float(a[2]) + float(b[2]),
    ]


def mul_vec3(v, scalar):
    return [
        float(v[0]) * scalar,
        float(v[1]) * scalar,
        float(v[2]) * scalar,
    ]


def merge_part_with_overrides(base_part, overrides):
    """
    Return a new part spec made from base_part plus instance-specific overrides.

    The 'instances' key is deliberately removed from the resulting concrete part.
    """

    result = dict(base_part)
    result.pop("instances", None)

    for key, value in overrides.items():
        result[key] = value

    return result


def format_instance_name(name_format, base_name, index=None, row=None, col=None):
    """
    Format instance names.

    Supported placeholders:
      {name}
      {index}       one-based index
      {index0}      zero-based index
      {row}         one-based row
      {row0}        zero-based row
      {col}         one-based column
      {col0}        zero-based column
    """

    index0 = None if index is None else index - 1
    row0 = None if row is None else row - 1
    col0 = None if col is None else col - 1

    return name_format.format(
        name=base_name,
        index=index,
        index0=index0,
        row=row,
        row0=row0,
        col=col,
        col0=col0,
    )


def expand_parts(parts):
    """
    Expand layout parts into concrete per-instance part specs.

    Supported JSON forms:

    1. No instances:

       {
         "name": "mounting_plate",
         "file": "...",
         "position": [0, 0, 0]
       }

    2. Explicit instances list:

       {
         "name": "motor_mount",
         "file": "...",
         "rotation": [0, 0, 0],
         "instances": [
           { "name": "motor_mount_1", "position": [50, 0, 0] },
           { "name": "motor_mount_2", "position": [-50, 0, 0] }
         ]
       }

    3. Linear count:

       {
         "name": "motor_mount",
         "file": "...",
         "position": [-50, 0, 0],
         "instances": {
           "count": 2,
           "step": [100, 0, 0],
           "name_format": "{name}_{index}"
         }
       }

    4. Grid:

       {
         "name": "clip",
         "file": "...",
         "position": [-60, -40, 0],
         "instances": {
           "grid": [4, 3],
           "step": [40, 35, 0],
           "name_format": "{name}_{row}_{col}"
         }
       }
    """

    expanded = []

    for part_index, part in enumerate(parts, start=1):
        if not isinstance(part, dict):
            raise RuntimeError(f"Part #{part_index} must be an object/dict.")

        instances = part.get("instances")

        if instances is None:
            concrete = dict(part)
            expanded.append(concrete)
            continue

        base_name = part.get("name", f"part-{part_index}")

        # ------------------------------------------------------------------
        # Explicit instance list
        # ------------------------------------------------------------------
        if isinstance(instances, list):
            for instance_index, instance_overrides in enumerate(instances, start=1):
                if not isinstance(instance_overrides, dict):
                    raise RuntimeError(
                        f"Instance #{instance_index} of part {base_name!r} "
                        f"must be an object/dict."
                    )

                overrides = dict(instance_overrides)

                if "name" not in overrides:
                    overrides["name"] = f"{base_name}_{instance_index}"

                concrete = merge_part_with_overrides(part, overrides)
                expanded.append(concrete)

            continue

        # ------------------------------------------------------------------
        # Generated instances object
        # ------------------------------------------------------------------
        if not isinstance(instances, dict):
            raise RuntimeError(
                f"'instances' for part {base_name!r} must be either "
                f"a list or an object."
            )

        name_format = instances.get("name_format", "{name}_{index}")

        base_position = as_vector3(
            part.get("position", [0, 0, 0]),
            field_name=f"position for part {base_name!r}",
        )

        # ------------------------------------------------------------------
        # Linear count array
        # ------------------------------------------------------------------
        if "count" in instances:
            count = int(instances["count"])

            if count < 1:
                raise RuntimeError(
                    f"'instances.count' for part {base_name!r} must be >= 1."
                )

            step = as_vector3(
                instances.get("step", [0, 0, 0]),
                field_name=f"instances.step for part {base_name!r}",
            )

            for i in range(count):
                index = i + 1

                position = add_vec3(
                    base_position,
                    mul_vec3(step, i),
                )

                instance_name = format_instance_name(
                    name_format,
                    base_name,
                    index=index,
                )

                concrete = merge_part_with_overrides(
                    part,
                    {
                        "name": instance_name,
                        "position": position,
                    },
                )

                expanded.append(concrete)

            continue

        # ------------------------------------------------------------------
        # Grid array
        # ------------------------------------------------------------------
        if "grid" in instances:
            grid = instances["grid"]

            if not isinstance(grid, list) or len(grid) != 2:
                raise RuntimeError(
                    f"'instances.grid' for part {base_name!r} must be "
                    f"[columns, rows], got: {grid!r}"
                )

            cols = int(grid[0])
            rows = int(grid[1])

            if cols < 1 or rows < 1:
                raise RuntimeError(
                    f"'instances.grid' for part {base_name!r} must have "
                    f"positive columns and rows."
                )

            step = as_vector3(
                instances.get("step", [0, 0, 0]),
                field_name=f"instances.step for part {base_name!r}",
            )

            index = 0

            for row0 in range(rows):
                for col0 in range(cols):
                    index += 1

                    offset = [
                        float(step[0]) * col0,
                        float(step[1]) * row0,
                        float(step[2]) * 0,
                    ]

                    position = add_vec3(base_position, offset)

                    instance_name = format_instance_name(
                        name_format,
                        base_name,
                        index=index,
                        row=row0 + 1,
                        col=col0 + 1,
                    )

                    concrete = merge_part_with_overrides(
                        part,
                        {
                            "name": instance_name,
                            "position": position,
                        },
                    )

                    expanded.append(concrete)

            continue

        raise RuntimeError(
            f"'instances' for part {base_name!r} must contain either "
            f"'count' or 'grid'."
        )

    return expanded


# ---------------------------------------------------------------------------
# Mesh transforms
# ---------------------------------------------------------------------------


def load_mesh(path):
    """
    Load mesh file with FreeCAD Mesh module.

    Intended for STL. OBJ may also work depending on FreeCAD build.
    """
    mesh = Mesh.Mesh(str(path))

    if mesh.CountFacets == 0:
        raise RuntimeError(f"Mesh has zero facets: {path}")

    return mesh


def get_bounds(mesh):
    return mesh.BoundBox


def scale_mesh(mesh, scale):
    """
    Scale mesh.

    Supports:
        "scale": 2.0
    or:
        "scale": [1.0, 1.0, 1.0]
    """
    if scale is None:
        return

    if isinstance(scale, list):
        sx, sy, sz = float(scale[0]), float(scale[1]), float(scale[2])
    else:
        sx = sy = sz = float(scale)

    matrix = App.Matrix()
    matrix.A11 = sx
    matrix.A22 = sy
    matrix.A33 = sz

    mesh.transform(matrix)


def make_rotation(rx_deg, ry_deg, rz_deg):
    """
    Make FreeCAD rotation.

    Rotation order:
        R = Rz * Ry * Rx

    For print-bed layout, usually only RZ is used.
    """
    rx = App.Rotation(App.Vector(1, 0, 0), float(rx_deg))
    ry = App.Rotation(App.Vector(0, 1, 0), float(ry_deg))
    rz = App.Rotation(App.Vector(0, 0, 1), float(rz_deg))

    return rz.multiply(ry).multiply(rx)


def rotate_mesh(mesh, rotation):
    rx, ry, rz = rotation

    rot = make_rotation(rx, ry, rz)
    placement = App.Placement(App.Vector(0, 0, 0), rot)
    matrix = placement.toMatrix()

    mesh.transform(matrix)


def recenter_mesh_xy_to_origin(mesh):
    """
    Move mesh so its XY bounding-box center is at X=0, Y=0.
    Z is unchanged.
    """
    bb = get_bounds(mesh)

    cx = 0.5 * (bb.XMin + bb.XMax)
    cy = 0.5 * (bb.YMin + bb.YMax)

    mesh.translate(-cx, -cy, 0)


def drop_mesh_to_z(mesh, target_z):
    """
    Move mesh so its lowest point is at target_z.
    """
    bb = get_bounds(mesh)
    dz = float(target_z) - bb.ZMin

    mesh.translate(0, 0, dz)


def translate_mesh(mesh, x, y, z):
    mesh.translate(App.Vector(float(x), float(y), float(z)))


def place_mesh(mesh, spec):
    """
    Position one mesh according to layout spec.

    Common behavior:
      - scale if requested
      - center XY around origin
      - drop bottom to Z=0
      - rotate around origin
      - drop again to requested Z
      - move XY center to requested X/Y

    With center_xy=true, position means:
        bounding-box XY center goes to [X, Y]
        bottom goes to Z

    With center_xy=false, position means:
        raw mesh is translated by X/Y, after optional drop-to-bed behavior
    """
    position = spec.get("position", [0, 0, 0])
    rotation = spec.get("rotation", [0, 0, 0])

    x, y, z = float(position[0]), float(position[1]), float(position[2])
    rx, ry, rz = float(rotation[0]), float(rotation[1]), float(rotation[2])

    center_xy = bool(spec.get("center_xy", True))
    drop_to_bed = bool(spec.get("drop_to_bed", True))

    scale_mesh(mesh, spec.get("scale"))

    if center_xy:
        recenter_mesh_xy_to_origin(mesh)

    if drop_to_bed:
        drop_mesh_to_z(mesh, 0.0)

    rotate_mesh(mesh, [rx, ry, rz])

    if drop_to_bed:
        drop_mesh_to_z(mesh, z)

    if center_xy:
        # Robust final centering after rotation.
        bb = get_bounds(mesh)

        cx = 0.5 * (bb.XMin + bb.XMax)
        cy = 0.5 * (bb.YMin + bb.YMax)

        mesh.translate(x - cx, y - cy, 0)
    else:
        if drop_to_bed:
            # Z was already handled by drop_mesh_to_z(mesh, z).
            mesh.translate(x, y, 0)
        else:
            mesh.translate(x, y, z)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def validate_on_bed(mesh, part_name, bed):
    """
    Validate rectangular bed bounds.

    Assumes front-left origin:
        X from 0 to bed width
        Y from 0 to bed depth
    """
    if not bed:
        return

    shape = bed.get("shape", "rect")

    if shape != "rect":
        warn(
            f"Bed validation only supports rectangular beds. Skipping for shape={shape!r}."
        )
        return

    size = bed.get("size")

    if not size:
        return

    bed_x = float(size[0])
    bed_y = float(size[1])
    margin = float(bed.get("margin", 0))

    bb = get_bounds(mesh)

    problems = []

    if bb.XMin < margin:
        problems.append(f"XMin {bb.XMin:.3f} < margin {margin:.3f}")

    if bb.YMin < margin:
        problems.append(f"YMin {bb.YMin:.3f} < margin {margin:.3f}")

    if bb.XMax > bed_x - margin:
        problems.append(f"XMax {bb.XMax:.3f} > {bed_x - margin:.3f}")

    if bb.YMax > bed_y - margin:
        problems.append(f"YMax {bb.YMax:.3f} > {bed_y - margin:.3f}")

    if problems:
        raise RuntimeError(
            f"Part {part_name!r} is outside printable bed/margin:\n  "
            + "\n  ".join(problems)
        )


def boxes_overlap_xy(bb1, bb2, clearance):
    """
    Bounding-box overlap check in XY.

    This is conservative and simple. It may report overlap even when actual
    meshes do not touch, but it is useful for catching layout mistakes.
    """
    c = float(clearance)

    return not (
        bb1.XMax + c <= bb2.XMin
        or bb2.XMax + c <= bb1.XMin
        or bb1.YMax + c <= bb2.YMin
        or bb2.YMax + c <= bb1.YMin
    )


def validate_collision(mesh, part_name, placed, collision_settings):
    if not collision_settings:
        return

    if not bool(collision_settings.get("check", False)):
        return

    clearance = float(collision_settings.get("clearance", 0.0))
    bb = get_bounds(mesh)

    for other_name, other_bb in placed:
        if boxes_overlap_xy(bb, other_bb, clearance):
            raise RuntimeError(
                f"XY bounding-box overlap: {part_name!r} overlaps {other_name!r} "
                f"with clearance={clearance}"
            )


# ---------------------------------------------------------------------------
# Export
# ---------------------------------------------------------------------------


def make_mesh_feature(doc, mesh, internal_name, label=None):
    obj = doc.addObject("Mesh::Feature", internal_name)
    obj.Mesh = mesh

    if label:
        obj.Label = label

    return obj


def export_single_stl(obj, output_path):
    ensure_parent_dir(output_path)
    Mesh.export([obj], str(output_path))


def export_3mf(objects, output_path):
    ensure_parent_dir(output_path)
    Mesh.export(objects, str(output_path))


def export_combined_stl(meshes, output_path):
    output_path = Path(output_path)
    ensure_dir(output_path.parent)

    combined = Mesh.Mesh()

    for mesh in meshes:
        try:
            combined.addMesh(mesh)
        except AttributeError:
            # Fallback for FreeCAD versions where addMesh is unavailable.
            for facet in mesh.Facets:
                combined.addFacet(
                    facet.Points[0],
                    facet.Points[1],
                    facet.Points[2],
                )

    combined.write(str(output_path))


def patch_3mf_object_names(path, object_names):
    """
    Patch a FreeCAD-exported 3MF file so that individual mesh objects have names.

    FreeCAD's Mesh.export() may not write object labels into 3MF.
    This function opens the 3MF as a ZIP, edits 3D/3dmodel.model,
    and writes name attributes onto the 3MF <object> elements.

    object_names should be in the same order as the exported mesh_objects list.
    """

    import zipfile
    import tempfile
    import shutil
    import xml.etree.ElementTree as ET

    path = Path(path)

    model_filename = "3D/3dmodel.model"
    core_ns = "http://schemas.microsoft.com/3dmanufacturing/core/2015/02"

    ns = {
        "m": core_ns,
    }

    ET.register_namespace("", core_ns)

    tmp_path = path.with_suffix(path.suffix + ".tmp")

    with zipfile.ZipFile(path, "r") as zin:
        if model_filename not in zin.namelist():
            raise RuntimeError(
                f"Could not find {model_filename} inside 3MF file: {path}"
            )

        model_xml = zin.read(model_filename)

        root = ET.fromstring(model_xml)

        objects = root.findall(".//m:resources/m:object", ns)
        build_items = root.findall(".//m:build/m:item", ns)

        id_to_object = {
            obj.get("id"): obj for obj in objects if obj.get("id") is not None
        }

        patched = 0

        # Prefer build order, because that usually matches exported object order.
        build_order_objects = []

        for item in build_items:
            object_id = item.get("objectid")
            obj = id_to_object.get(object_id)

            if obj is not None:
                build_order_objects.append((obj, item))

        if len(build_order_objects) == len(object_names):
            for name, (obj, item) in zip(object_names, build_order_objects):
                obj.set("name", name)

                # Some tools/slicers expose partnumber more reliably than name.
                obj.set("partnumber", name)
                item.set("partnumber", name)

                patched += 1

        elif len(objects) == len(object_names):
            # Fallback: resource object order.
            for name, obj in zip(object_names, objects):
                obj.set("name", name)
                obj.set("partnumber", name)
                patched += 1

        else:
            warn(
                "Could not confidently patch all 3MF object names. "
                f"3MF contains {len(objects)} resource objects and "
                f"{len(build_order_objects)} build items, but script has "
                f"{len(object_names)} mesh objects."
            )

            # Best-effort fallback.
            for name, obj in zip(object_names, objects):
                obj.set("name", name)
                obj.set("partnumber", name)
                patched += 1

        new_model_xml = ET.tostring(
            root,
            encoding="utf-8",
            xml_declaration=True,
        )

        with zipfile.ZipFile(tmp_path, "w", compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == model_filename:
                    zout.writestr(item, new_model_xml)
                else:
                    zout.writestr(item, zin.read(item.filename))

    shutil.move(str(tmp_path), str(path))

    log(f"Patched {patched} object name(s) in 3MF: {path}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def get_freecad_script_args():
    argv = list(sys.argv)

    if "--pass" in argv:
        return argv[argv.index("--pass") + 1 :]

    if "--" in argv:
        return argv[argv.index("--") + 1 :]

    for i, arg in enumerate(argv):
        if Path(arg).name == "generate_plate.py":
            return argv[i + 1 :]

    return argv[1:]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate positioned print plate geometry from a layout JSON file."
    )

    parser.add_argument(
        "layouts",
        nargs="+",
        help="Path to layout JSON file, e.g. mechanical/prints/layouts/frame.layout.json",
    )

    parser.add_argument(
        "--base-dir",
        default=".",
        help=(
            "Base directory for relative paths in the layout file. "
            "Default: current working directory, normally the repo root."
        ),
    )

    parser.add_argument(
        "--no-3mf",
        action="store_true",
        help="Do not export positioned 3MF, even if layout has outputs.positioned_3mf.",
    )

    parser.add_argument(
        "--no-stl",
        action="store_true",
        help="Do not export positioned STLs, even if layout has outputs.positioned_stl_dir.",
    )

    parser.add_argument(
        "--allow-3mf-failure",
        action="store_true",
        help="Do not fail the build if 3MF export fails. Positioned STLs may still be exported.",
    )

    return parser.parse_args(get_freecad_script_args())


# def main():
args = parse_args()

print(args)

for layout_arg in args.layouts:
    log("")
    log("=" * 80)
    log(f"Processing layout: {layout_arg}")
    log("=" * 80)

    base_dir = Path("/app").resolve()
    # layout_path = resolve_path(
    #     # "mechanical/prints/layouts/clearance-gauge.layout.json", base_dir
    #     # "mechanical/prints/layouts/color-coding.layout.json", base_dir,
    #     "mechanical/prints/layouts/frame.layout.json",
    #     base_dir,
    # )
    layout_path = resolve_path(
        layout_arg,
        base_dir,
    )

    if not layout_path.exists():
        raise RuntimeError(f"Layout file does not exist: {layout_path}")

    with open(layout_path, "r", encoding="utf-8") as f:
        layout = json.load(f)
    print(layout)
    plate_name = layout.get("name", layout_path.stem.replace(".layout", ""))
    outputs = layout.get("outputs", {})

    positioned_3mf = outputs.get("3mf")
    combined_stl = outputs.get("combined_stl")

    positioned_3mf_path = (
        resolve_path(positioned_3mf, base_dir) if positioned_3mf else None
    )
    combined_stl_path = resolve_path(combined_stl, base_dir) if combined_stl else None

    bed = layout.get("bed", None)
    collision_settings = layout.get("collision", None)

    parts = expand_parts(layout.get("parts", []))

    if not parts:
        raise RuntimeError(f"No parts found in layout: {layout_path}")

    log(f"Generating plate: {plate_name}")
    log(f"Layout: {layout_path}")
    log(f"Base dir: {base_dir}")

    doc = App.newDocument(f"plate_{slugify(plate_name)}")

    mesh_objects = []
    placed_bounds = []
    used_output_names = {}

    placed_meshes = []

    for index, spec in enumerate(parts, start=1):
        name = spec.get("name", f"part-{index}")
        safe_name = slugify(name)

        # Avoid overwriting files if duplicate names occur.
        count = used_output_names.get(safe_name, 0) + 1
        used_output_names[safe_name] = count

        if count > 1:
            safe_name_with_index = f"{safe_name}-{count}"
        else:
            safe_name_with_index = safe_name

        input_file = spec.get("file")

        if not input_file:
            raise RuntimeError(f"Part {name!r} is missing required field 'file'.")

        input_path = resolve_path(input_file, base_dir)

        if not input_path.exists():
            raise RuntimeError(
                f"Input mesh does not exist for part {name!r}: {input_path}"
            )

        log("")
        log(f"[{index}/{len(parts)}] {name}")
        log(f"  input: {input_path}")

        mesh = load_mesh(input_path)
        place_mesh(mesh, spec)

        placed_meshes.append(mesh.copy())

        validate_on_bed(mesh, name, bed)
        validate_collision(mesh, name, placed_bounds, collision_settings)

        bb = get_bounds(mesh)
        placed_bounds.append((name, bb))

        log(
            "  bounds: "
            f"X[{bb.XMin:.3f}, {bb.XMax:.3f}] "
            f"Y[{bb.YMin:.3f}, {bb.YMax:.3f}] "
            f"Z[{bb.ZMin:.3f}, {bb.ZMax:.3f}]"
        )

        obj = make_mesh_feature(doc, mesh, safe_name_with_index, label=name)
        mesh_objects.append(obj)

    doc.recompute()

    if combined_stl_path and not args.no_stl:
        log("")
        log(f"Writing combined STL: {combined_stl_path}")
        export_combined_stl(placed_meshes, combined_stl_path)

    if positioned_3mf_path and not args.no_3mf:
        log("")
        log(f"Writing positioned 3MF: {positioned_3mf_path}")

        try:
            export_3mf(mesh_objects, positioned_3mf_path)

            object_names = [
                obj.Label if obj.Label else obj.Name for obj in mesh_objects
            ]

            patch_3mf_object_names(positioned_3mf_path, object_names)

        except Exception as exc:
            message = (
                f"Failed to export 3MF: {positioned_3mf_path}\n"
                f"Reason: {exc}\n\n"
                "Your FreeCAD build may not support 3MF export, "
                "or the 3MF name patching step failed."
            )

            if args.allow_3mf_failure:
                warn(message)
            else:
                raise RuntimeError(message)

log("")
log("Done.")

exit()
