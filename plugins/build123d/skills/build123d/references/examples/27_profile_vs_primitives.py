#!/usr/bin/env python3
"""
Profile vs Primitives: When to Use Each

PRIMITIVES (Box, Cylinder, Sphere):
- Simple blocky shapes
- Few features
- Quick prototypes

PROFILES (BuildSketch + extrude):
- Complex cross-sections
- Curved edges
- Precise dimensions
- Symmetric features

Run with: uvx --from build123d python 27_profile_vs_primitives.py
"""
from build123d import *

# PRIMITIVE approach: simple assembly
with BuildPart() as primitive_example:
    Box(60, 40, 20)
    with Locations((0, 0, 20)):
        Cylinder(15, 30)
    with Locations((20, 10, 0)):
        Hole(5, depth=20)

export_gltf(primitive_example.part, "./27a_primitives.glb", binary=True)
print("Exported 27a_primitives.glb")

# PROFILE approach: complex cross-section
with BuildPart() as profile_example:
    with BuildSketch():
        RectangleRounded(60, 40, 8)  # Rounded corners built-in
        with Locations((15, 0)):
            SlotOverall(20, 10, mode=Mode.SUBTRACT)
    extrude(amount=20)

    with BuildSketch(Plane.XY.offset(20)):
        with Locations((-15, 0)):
            Circle(12)
            Circle(8, mode=Mode.SUBTRACT)
    extrude(amount=15)

export_gltf(profile_example.part, "./27b_profiles.glb", binary=True)
print("Exported 27b_profiles.glb")

# Decision guide example: bracket needs profiles
with BuildPart() as bracket:
    # Profile for base with rounded slot
    with BuildSketch():
        RectangleRounded(80, 40, 5)
        SlotOverall(50, 10, mode=Mode.SUBTRACT)
    extrude(amount=10)

    # Profile for boss
    with BuildSketch(Plane.XZ.offset(20)):
        with Locations((-25, 10)):
            SlotOverall(40, 30, rotation=90)
    extrude(amount=-8)
    split(bisect_by=Plane.XY)

result = bracket.part
export_gltf(result, "./27c_bracket_profiles.glb", binary=True)
print("Exported 27c_bracket_profiles.glb")
