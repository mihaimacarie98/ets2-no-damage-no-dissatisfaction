#!/usr/bin/env python3
"""Build 'No Damage + No Passenger Dissatisfaction' mod for ETS2 1.62.
v1.1: whitespace-preserving edits, plus def/used_vehicle_config.sii override
so used-truck dealer offers also spawn at 0% wear (unfixable included).
Reads the REAL extracted game files and applies minimal field edits.
"""
import os
import re
import sys
import zipfile
import shutil

SRC = "/mnt/c/Users/yo2mn/ets2mod/extract/def/def"
BUILD = "/home/hackerman/ets2-mod-work/build/zzz_no_damage_no_dissatisfaction"
OUT = "/home/hackerman/ets2-mod-work/zzz_no_damage_no_dissatisfaction.scs"
DOCS_MOD = "/mnt/c/Users/yo2mn/Documents/Euro Truck Simulator 2/mod"

# ---- def/damage_data.sii : zero every damage + wear source -----------------
DAMAGE_EDITS = [
    ("truck_damage_coef:", "0.0"),
    ("trailer_damage_coef:", "0.0"),
    ("dragged_trailer_damage_coef:", "0.0"),
    ("truck_to_trailer_dmg:", "0.0"),
    ("side_damage_factor:", "0.0"),
    ("roof_damage_factor:", "0.0"),
    ("cargo_damage_ratio:", "0.0"),
    ("cabin_wear:", "0.0"),
    ("chassis_wear:", "0.0"),
    ("engine_wear:", "0.0"),
    ("transmission_wear:", "0.0"),
    ("wheel_wear:", "0.0"),
    ("cabin_wear_unfixable:", "0.0"),
    ("chassis_wear_unfixable:", "0.0"),
    ("engine_wear_unfixable:", "0.0"),
    ("transmission_wear_unfixable:", "0.0"),
    ("wheel_wear_unfixable:", "0.0"),
    ("trailer_body_wear:", "0.0"),
    ("trailer_chassis_wear:", "0.0"),
    ("trailer_wheel_wear:", "0.0"),
    ("trailer_body_wear_unfixable:", "0.0"),
    ("trailer_chassis_wear_unfixable:", "0.0"),
    ("trailer_wheel_wear_unfixable:", "0.0"),
]

# ---- def/bus_economy_data.sii : zero every satisfaction penalty ------------
BUS_EDITS = [
    ("satisfaction_new_passenger:", "(1.0, 1.0)"),
    ("satisfaction_new_passenger_core_wear_penalty:", "(0.0, 0.0)"),
    ("satisfaction_acceleration_penalties[]:", "(0.0, 0.0)"),
    ("satisfaction_crash_penalties[]:", "(0.0, 0.0)"),
    ("satisfaction_speed_penalty:", "(0.0, 0.0)"),
    ("satisfaction_core_wear_penalties[]:", "(0.0, 0.0)"),
    ("satisfaction_late_penalty:", "(0.0, 0.0)"),
    ("satisfaction_offence_penalty:", "(0.0, 0.0)"),
    ("failure_acceleration_limit:", "(-1.0, -1.0, 999.0)"),
]

# ---- def/used_vehicle_config.sii : used trucks spawn at 0% wear ------------
USED_VEHICLE_EDITS = [
    ("truck_chassis_wear_unfixable_max:", "0.0"),
    ("truck_wheels_wear_unfixable_max:", "0.0"),
    ("truck_engine_wear_unfixable_max:", "0.0"),
    ("truck_transmission_wear_unfixable_max:", "0.0"),
    ("truck_cabin_wear_unfixable_max:", "0.0"),
]

MANIFEST = """SiiNunit
{
mod_package : .package_name
{
	package_version: "1.1"

	display_name: "No Damage + No Passenger Dissatisfaction"

	author: "hackerman"

	category[]: "other"

	compatible_versions[]: "1.62.*"

	description_file: "description.txt"
}
}
"""

DESCRIPTION = """Keeps your truck and trailer damage permanently at 0% and pins bus passenger
satisfaction at maximum, no matter how you drive.

Truck damage:
- all collision damage coefficients zeroed (truck, trailer, dragged trailer, side/roof impacts)
- all mileage wear zeroed (engine, transmission, wheels, fixable and unfixable)
- cargo damage ratio zeroed
- used-truck dealer offers also spawn at 0% wear (unfixable included)

Bus passenger satisfaction (official bus DLC):
- every satisfaction penalty zeroed: harsh acceleration, crashes, speeding,
  core part wear, late arrivals, traffic offences
- new-passenger satisfaction set to maximum
- job-failure acceleration limit disabled

Note: damage or wear already present in an existing save is NOT reset.
Repair your truck once at a service station, and from then on it stays at 0%.
"""


def apply_edits(src_path, edits, rel_out):
    with open(src_path, encoding="utf-8") as f:
        text = f.read()
    total = 0
    for key, newval in edits:
        pat = re.compile(
            r"^([ \t]*" + re.escape(key) + r")([ \t]*)(?:\([^)\n]*\)|[\d.eE+-]+)",
            re.M,
        )
        text, n = pat.subn(lambda m: m.group(1) + m.group(2) + newval, text)
        total += n
    dst = os.path.join(BUILD, rel_out)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    with open(dst, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return total


def main():
    os.makedirs(BUILD, exist_ok=True)
    n1 = apply_edits(os.path.join(SRC, "damage_data.sii"), DAMAGE_EDITS, "def/damage_data.sii")
    n2 = apply_edits(os.path.join(SRC, "bus_economy_data.sii"), BUS_EDITS, "def/bus_economy_data.sii")
    n3 = apply_edits(os.path.join(SRC, "used_vehicle_config.sii"), USED_VEHICLE_EDITS, "def/used_vehicle_config.sii")
    with open(os.path.join(BUILD, "manifest.sii"), "w", encoding="utf-8", newline="\n") as f:
        f.write(MANIFEST)
    with open(os.path.join(BUILD, "description.txt"), "w", encoding="utf-8", newline="\n") as f:
        f.write(DESCRIPTION)
    print(f"damage_data.sii edits applied: {n1}")
    print(f"bus_economy_data.sii edits applied: {n2}")
    print(f"used_vehicle_config.sii edits applied: {n3}")

    for rel in ("def/damage_data.sii", "def/bus_economy_data.sii", "def/used_vehicle_config.sii"):
        t = open(os.path.join(BUILD, rel), encoding="utf-8").read()
        if t.count("{") != t.count("}"):
            print(f"ERROR: unbalanced braces in {rel}")
            sys.exit(1)
    print("brace check OK")

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, _dirs, files in os.walk(BUILD):
            for fn in files:
                p = os.path.join(root, fn)
                arc = os.path.relpath(p, BUILD).replace(os.sep, "/")
                zf.write(p, arc)
    print(f"wrote {OUT}")

    os.makedirs(DOCS_MOD, exist_ok=True)
    dst = os.path.join(DOCS_MOD, "zzz_no_damage_no_dissatisfaction.scs")
    shutil.copyfile(OUT, dst)
    print(f"installed to {dst}")


if __name__ == "__main__":
    main()
