#!/usr/bin/env python3
"""
Split and Mirror: Symmetric Half-Shapes

split(bisect_by=Plane.XY) keeps Z > 0 (positive normal side)
mirror(about=Plane.XZ) duplicates features symmetrically

Run with: uvx --from build123d python 21_split_and_mirror.py
"""
from build123d import *

# Split: Sphere becomes hemisphere
with BuildPart() as dome:
    Sphere(radius=30)
    split(bisect_by=Plane.XY)  # Keeps Z > 0

export_gltf(dome.part, "./21a_hemisphere.glb", binary=True)
print("Exported 21a_hemisphere.glb")

# Split: Stadium becomes fork lugs
with BuildPart() as fork:
    with BuildSketch():
        Rectangle(80, 40)
    extrude(amount=10)

    with BuildSketch(Plane.XZ.offset(20)):
        with Locations((-20, 10)):
            SlotOverall(50, 30, rotation=90)
    extrude(amount=-8)
    split(bisect_by=Plane.XY)  # Stadium → two lugs

export_gltf(fork.part, "./21b_fork_lugs.glb", binary=True)
print("Exported 21b_fork_lugs.glb")

# Mirror: One hole → symmetric pair
with BuildPart() as plate:
    Box(100, 60, 10)
    with Locations((30, 15, 10)):
        Hole(5)
    mirror(about=Plane.XZ)  # Creates hole at (30, -15, 10)

export_gltf(plate.part, "./21c_mirrored_holes.glb", binary=True)
print("Exported 21c_mirrored_holes.glb")

# Combined: Fork bracket with mirrored holes
with BuildPart() as bracket:
    with BuildSketch():
        RectangleRounded(100, 50, 5)
    extrude(amount=12)

    with BuildSketch(Plane.XZ.offset(25)):
        with Locations((-30, 12)):
            SlotOverall(60, 40, rotation=90)
    boss = extrude(amount=-10)
    split(bisect_by=Plane.XY)

    with Locations(boss.faces().sort_by(Axis.Y)[0]):
        with Locations((18, 0)):
            CounterBoreHole(8, 12, 3)
    mirror(about=Plane.XZ)

result = bracket.part
export_gltf(result, "./21d_bracket.glb", binary=True)
print("Exported 21d_bracket.glb")
