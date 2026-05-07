#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: LGPL-3.0-or-later
# SPDX-FileCopyrightText: 2026 Christoph Böhm <christoph.boehm@ieee.org>
"""
Apply user parameters to CAD source files.

Reads YAML parameters from mechanical/source/part_parameters.yaml,
applies them to spreadsheets named "params" inside FreeCAD source parts,
and updates the FreeCAD bodies.

Usage (from repository root):
    freecad.cmd -c scripts/apply_parameters.py
    # or, depending on your install:
    # FreeCADCmd -c scripts/apply_parameters.py
    # FreeCAD -c scripts/apply_parameters.py  (GUI binary, still console mode)

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
import zipfile
import tempfile
import shutil

# Try to load FreeCAD API
try:
    import FreeCAD as App
    import Part
    import Mesh
    import MeshPart
except Exception as e:
    sys.stderr.write(f"Error: run with freecad --console (headless). {e}\n")
    sys.exit(1)

# Define which parts to apply the parameters to
PARTS = [
    {"fcstd": "validation/clearance_gauge.FCStd", "label": "clearance_gauge"},
    {
        "fcstd": "hardware/mechanical/source/parts/length_ruler.FCStd",
        "label": "length_ruler",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/motor_mount.FCStd",
        "label": "motor_mount",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/capacitor_holder.FCStd",
        "label": "capacitor_holder",
    },
    {"fcstd": "hardware/mechanical/source/parts/rotor_arm.FCStd", "label": "rotor_arm"},
    {
        "fcstd": "hardware/mechanical/source/parts/landing_gear_mount.FCStd",
        "label": "landing_gear_mount",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/battery_holder.FCStd",
        "label": "battery_holder",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/rc_receiver_mount.FCStd",
        "label": "rc_receiver_mount",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/mounting_plate.FCStd",
        "label": "mounting_plate",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/quick_release_base.FCStd",
        "label": "quick_release_base",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/esc_connector_mount.FCStd",
        "label": "esc_connector_mount",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/motor_mount_1mm_spacer.FCStd",
        "label": "motor_mount_1mm_spacer",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/motor_mount_2mm_spacer.FCStd",
        "label": "motor_mount_2mm_spacer",
    },
    {"fcstd": "hardware/mechanical/source/parts/handle.FCStd", "label": "handle"},
    {
        "fcstd": "hardware/mechanical/source/parts/xt30_male_mount.FCStd",
        "label": "xt30_male_mount",
    },
    {
        "fcstd": "hardware/mechanical/source/parts/template_part.FCStd",
        "label": "template_part",
    },
]

PARAMS_FILE = "params/default.yaml"


# Helper functions
def find_spreadsheet(doc):
    # Try by Label "params"
    for o in doc.Objects:
        # if o.isDerivedFrom("Spreadsheet::Sheet") and (o.Label == "params"):
        if o.isDerivedFrom("Spreadsheet::Sheet") and (o.Label == "params"):
            return o
    return None


def load_params_yaml(path, variant=None):
    try:
        import yaml
    except ImportError:
        sys.stderr.write("Install PyYAML (pip install pyyaml) or use CSV mode.\n")
        sys.exit(1)
    with open(path, "r") as f:
        data = yaml.safe_load(f) or {}
    params = {k: v for k, v in data.items() if k != "variants"}
    if variant and "variants" in data and variant in data["variants"]:
        params.update(data["variants"][variant] or {})
    # Convert numbers to strings with units if needed
    for k, v in list(params.items()):
        if isinstance(v, (int, float)):
            # Assume millimeters for geometry; FreeCAD likes unit strings
            params[k] = f"{v} mm"
        else:
            params[k] = str(v)
    return params


def apply_params_to_sheet(sheet, params):
    # Sheet aliases: aliases map names to cells; we set by alias
    for name, value in params.items():
        try:
            # If alias exists, set the cell by alias
            cell = sheet.getCellFromAlias(name)
            if cell:
                sheet.set(cell, value)
            else:
                # If alias missing, optionally create an alias (requires a free cell)
                # Here we skip creation to avoid clobbering; warn instead.
                print(f"[WARN] Alias '{name}' not found in Spreadsheet '{sheet.Label}'")
        except Exception as e:
            print(f"[WARN] Could not set '{name}'='{value}': {e}")
    # Recompute expressions
    sheet.recompute()


def extract_gui_xml(fcstd_path):
    """Read GuiDocument.xml bytes from an FCStd. Returns None if missing."""
    with zipfile.ZipFile(fcstd_path, "r") as zf:
        try:
            return zf.read("GuiDocument.xml")
        except KeyError:
            return None


def restore_gui_xml(fcstd_path, gui_xml_bytes):
    """
    Replace GuiDocument.xml with gui_xml_bytes.
    Returns True if the file was written/rebuilt, False if nothing done.
    """
    # If we have nothing to restore, bail out early
    if gui_xml_bytes is None:
        return False

    # Check if the archive currently has GuiDocument.xml
    with zipfile.ZipFile(fcstd_path, "r") as zin:
        has_gui = "GuiDocument.xml" in zin.namelist()

    # Rebuild the archive, replacing (or adding) GuiDocument.xml
    fd, tmp = tempfile.mkstemp(suffix=".FCStd", prefix="fcad_gui_restore_")
    os.close(fd)
    try:
        with (
            zipfile.ZipFile(fcstd_path, "r") as zin,
            zipfile.ZipFile(tmp, "w", compression=zipfile.ZIP_DEFLATED) as zout,
        ):
            names = zin.namelist()
            for name in names:
                data = zin.read(name)
                if name == "GuiDocument.xml":
                    zout.writestr(name, gui_xml_bytes)  # replace
                else:
                    zout.writestr(name, data)

            if not has_gui:
                # Original archive lacked GuiDocument.xml; add it now
                zout.writestr("GuiDocument.xml", gui_xml_bytes)

        shutil.move(tmp, fcstd_path)
        return True
    finally:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except OSError:
                pass


def verify_gui_xml(fcstd_path, expected_bytes):
    try:
        with zipfile.ZipFile(fcstd_path, "r") as zf:
            return zf.read("GuiDocument.xml") == expected_bytes
    except Exception:
        return False


# PropertiesList (list) = ['Comment', 'Company', 'CreatedBy', 'CreationDate', 'FileName', 'Id', 'Label', 'LastModifiedBy', 'LastModifiedDate', 'License', 'LicenseURL', 'Material', 'Meta', 'ShowHidden', 'Tip', 'TipName', 'TransientDir', 'Uid', 'UnitSystem', 'UseHasher']
# Possible entries
entries = [
    "Comment",
    "Company",
    "CreatedBy",
    "CreationDate",
    "FileName",
    "Id",
    "Label",
    "LastModifiedBy",
    "LastModifiedDate",
    "License",
    "LicenseURL",
    "Material",
    "Meta",
    "ShowHidden",
    "Tip",
    "TipName",
    "TransientDir",
    "Uid",
    "UnitSystem",
    "UseHasher",
]


def set_document_properties(doc, **props):
    for k, v in props.items():
        if k in entries and hasattr(doc, k):
            setattr(doc, k, v)


def apply_metadata(doc):
    set_document_properties(doc, CreatedBy="Christoph Böhm")
    set_document_properties(doc, Company="UAS Technikum Wien")
    set_document_properties(
        doc, Comment="Source: https://github.com/uastw-embsys/comet"
    )
    set_document_properties(doc, License="CERN-OHL-W-2.0")
    set_document_properties(doc, LicenseURL="https://ohwr.org/cern_ohl_w_v2.txt")


# Main

# Load parameters
params = load_params_yaml(PARAMS_FILE)

# Go through each entry in part list
for item in PARTS:
    fcstd = item["fcstd"]
    label = item["label"]
    print(f"\n[Open] {fcstd}")

    # 1) Snapshot original GUI document
    original_gui = extract_gui_xml(fcstd)

    # 2) Open, modify, save
    doc = App.openDocument(fcstd)
    try:
        # # Read current values
        # for p in entries:
        #     print(f"{p}: {getattr(doc, p, None)}")

        # Apply parameters
        sheet = find_spreadsheet(doc)
        if sheet:
            print(f"[Params] Apply {len(params)} values to '{sheet.Label}'")
            apply_params_to_sheet(sheet, params)
        else:
            print("[WARN] No Spreadsheet found; skipping parameter application.")

        apply_metadata(doc)

        # Recompute
        doc.recompute()
        doc.save()
    finally:
        # 3) Always close before touching the zip on disk
        try:
            App.closeDocument(doc.Name)
        except Exception:
            pass

    # 4) Restore GUI XML at file level
    ok = restore_gui_xml(fcstd, original_gui)

    # 5) Optional verification
    print("GUI settings restored:", ok)
    print("GUI settings verified:", verify_gui_xml(fcstd, original_gui))

print("\n[Done] Parameters applied.")
exit()
