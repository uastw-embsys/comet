#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>
"""
Export the "source" files to STL and STEP.

Scans the "mechanical/source/parts" folder for the FreeCAD sources of interest
and exports them to STL meshes and STEP solids in the "mechanical/exports/" folder.
This ensures deterministic and reproducible outputs.

Usage (from repository root):
    freecad.cmd -c scripts/export_source.py
    # or, depending on your install:
    # FreeCADCmd -c scripts/export_source.py
    # FreeCAD -c scripts/export_source.py  (GUI binary, still console mode)

License: LGPL-3.0-or-later
See the LICENSE file (or https://www.gnu.org/licenses/lgpl-3.0.txt).
"""

__version__ = "1.0.0"
__author__ = "Christoph Böhm"
__contact__ = "christoph.boehm@ieee.org"
__copyright__ = "2026 Christoph Böhm"
__license__ = "LGPL-3.0-or-later"

# Import all relevant modules
import os
import sys

# Try to load FreeCAD API
try:
    import FreeCAD as App
    import Part
    import Mesh
    import MeshPart
    import Import  # for STEP and 3MF export via Import.export on document objects
except Exception as e:
    sys.stderr.write(f"Error: run with freecad --console (headless). {e}\n")
    sys.exit(1)

from common import *


def ensure_dir(path):
    d = os.path.dirname(path)
    if d and not os.path.exists(d):
        os.makedirs(d)


def find_object_by_label(doc, label):
    for o in doc.Objects:
        if o.Label == label:
            return o
    return None


def export_one(item):
    import math

    fcstd = item["fcstd"]
    label = item["label"]  # base label, Body is expected to be labeled "B_<label>"
    out_stl = "mechanical/exports/stl/" + item["label"] + ".stl"  # item.get("out_stl")
    out_step = (
        "mechanical/exports/step/" + item["label"] + ".step"
    )  # item.get("out_step")
    out_3mf = item.get("out_3mf")
    mesh = item.get("mesh", {"linear": 0.1, "angular": 15.0, "relative": False})

    print(f"Opening {fcstd}")
    doc = App.openDocument(fcstd)
    try:
        doc.recompute()

        # Find the PartDesign Body (use its document object, not only its Shape)
        body_label = "B_" + label
        obj = find_object_by_label(doc, body_label)
        if not obj:
            # fallback: accept plain label if B_ prefix not used
            obj = find_object_by_label(doc, label)

        if not obj:
            raise RuntimeError(
                f"Body with label '{body_label}' (or '{label}') not found in {fcstd}"
            )

        if not hasattr(obj, "Shape"):
            raise RuntimeError(f"Found object '{obj.Label}', but it has no Shape")

        # Always recompute before export
        doc.recompute()

        # 1) STEP export (use the document object)
        if out_step:
            ensure_dir(out_step)
            print(f"Export STEP: {out_step}")
            # Import.export wants document objects
            Import.export([obj], out_step)

        # Prepare meshing parameters (convert degrees → radians)
        lin = float(mesh.get("linear", 0.1))  # 0.05mm - 0.15mm
        ang_deg = float(mesh.get("angular", 15.0))  # 10° - 20°
        ang_rad = math.radians(ang_deg)
        rel = bool(mesh.get("relative", False))

        # 2) STL export (create a temporary Mesh::Feature)
        if out_stl:
            ensure_dir(out_stl)
            print(f"Tessellate and export STL: {out_stl}")
            m = MeshPart.meshFromShape(
                Shape=obj.Shape,
                LinearDeflection=lin,
                AngularDeflection=ang_rad,
                Relative=rel,
            )
            tmp_mesh = doc.addObject("Mesh::Feature", f"__tmp_mesh_{obj.Name}")
            tmp_mesh.Mesh = m
            doc.recompute()
            try:
                Mesh.export([tmp_mesh], out_stl)
            finally:
                # cleanup temp mesh object
                try:
                    doc.removeObject(tmp_mesh.Name)
                    doc.recompute()
                except Exception:
                    pass

    finally:
        try:
            App.closeDocument(doc.Name)
        except Exception:
            pass


for item in PARTS:
    export_one(item)
print("Export completed.")
exit()
