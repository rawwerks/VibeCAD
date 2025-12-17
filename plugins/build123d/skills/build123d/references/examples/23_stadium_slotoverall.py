#!/usr/bin/env python3
"""
SlotOverall: Stadium/Pill Shapes

SlotOverall(length, width) creates rounded-rectangle profiles.
- length = total length including rounded ends
- width = full width (not radius!)
- rotation=90 for vertical orientation

Run with: uvx --from build123d python 23_stadium_slotoverall.py
"""
from build123d import *

# Basic horizontal stadium
with BuildPart() as horizontal:
    with BuildSketch():
        SlotOverall(60, 20)  # 60mm long, 20mm wide
    extrude(amount=10)

export_gltf(horizontal.part, "./23a_horizontal_stadium.glb", binary=True)
print("Exported 23a_horizontal_stadium.glb")

# Vertical stadium (bearing housing profile)
with BuildPart() as vertical:
    with BuildSketch():
        SlotOverall(80, 30, rotation=90)
    extrude(amount=15)

export_gltf(vertical.part, "./23b_vertical_stadium.glb", binary=True)
print("Exported 23b_vertical_stadium.glb")

# Stadium as slot cutout
with BuildPart() as slotted_plate:
    with BuildSketch():
        Rectangle(100, 50)
        with Locations((10, 0)):
            SlotOverall(60, 12, mode=Mode.SUBTRACT)
    extrude(amount=8)

export_gltf(slotted_plate.part, "./23c_slotted_plate.glb", binary=True)
print("Exported 23c_slotted_plate.glb")

# Stadium on side face for bearing boss
with BuildPart() as bearing_boss:
    with BuildSketch():
        Rectangle(100, 50)
    extrude(amount=15)

    with BuildSketch(Plane.XZ.offset(25)):
        with Locations((-30, 15)):
            SlotOverall(50, 40, rotation=90)
    extrude(amount=-12)

result = bearing_boss.part
export_gltf(result, "./23d_bearing_boss.glb", binary=True)
print("Exported 23d_bearing_boss.glb")
