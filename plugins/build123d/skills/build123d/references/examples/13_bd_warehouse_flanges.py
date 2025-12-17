#!/usr/bin/env python3
"""
bd_warehouse flanges example - Run with:
uvx --from build123d --with bd_warehouse python 13_bd_warehouse_flanges.py

Demonstrates different flange types and pipe connections.
"""
from build123d import (
    Edge, Pos, export_gltf, export_stl, MM, IN
)
from bd_warehouse.flange import WeldNeckFlange, SlipOnFlange, BlindFlange
from bd_warehouse.pipe import Pipe

# Create a weld neck flange (most common for high-pressure)
# 4" pipe size, Class 150 pressure rating
weld_neck = WeldNeckFlange(
    nps="4",
    flange_class=150,
    face_type="Raised",
)

# Create a slip-on flange (slides over pipe, then welded)
slip_on = SlipOnFlange(
    nps="4",
    flange_class=150,
    face_type="Raised",
)
slip_on = Pos(200 * MM, 0, 0) * slip_on

# Create a blind flange (closes off pipe end)
blind = BlindFlange(
    nps="4",
    flange_class=150,
    face_type="Raised",
)
blind = Pos(400 * MM, 0, 0) * blind

# Create a short pipe section to show flange-pipe assembly
# Position it between the weld neck and slip-on flanges
pipe_path = Edge.make_line((50 * MM, -100 * MM, 0), (150 * MM, -100 * MM, 0))
pipe_section = Pipe(
    nps="4",
    material="steel",
    identifier="40",
    path=pipe_path,
)

# Add flanges at pipe ends (positioned manually for demo)
pipe_weld_neck = Pos(50 * MM, -100 * MM, 0) * WeldNeckFlange(nps="4", flange_class=150)
pipe_slip_on = Pos(150 * MM, -100 * MM, 0) * SlipOnFlange(nps="4", flange_class=150)

# Combine all parts
result = weld_neck + slip_on + blind + pipe_section + pipe_weld_neck + pipe_slip_on

# Export
export_gltf(result, "./flanges_example.glb", binary=True)
export_stl(result, "./flanges_example.stl")

print("Exported: flanges_example.glb, flanges_example.stl")
print("Flanges created (all 4\" NPS, Class 150):")
print(f"  - Weld Neck Flange at origin")
print(f"  - Slip-On Flange at X=200mm")
print(f"  - Blind Flange at X=400mm")
print(f"  - Pipe assembly with flanges at Y=-100mm")

# Show flange info
print(f"\nWeld Neck Flange OD: {weld_neck.od:.1f}mm, thickness: {weld_neck.thickness:.1f}mm")
print("Face types available: Flat, Raised, Ring, Tongue, Groove, Male, Female")
print("Flange classes: 150, 300, 400, 600, 900, 1500, 2500")
