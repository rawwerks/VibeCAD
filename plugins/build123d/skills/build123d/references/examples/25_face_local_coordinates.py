#!/usr/bin/env python3
"""
Face Local Coordinates

Faces have their own coordinate system.
Use extrusion_result.faces() to get faces, then position in local coords.

Run with: uvx --from build123d python 25_face_local_coordinates.py
"""
from build123d import *

with BuildPart() as bracket:
    # Base
    with BuildSketch():
        Rectangle(100, 50)
    extrude(amount=15)

    # Boss - save extrusion result!
    with BuildSketch(Plane.XZ.offset(25)):
        with Locations((-30, 15)):
            SlotOverall(50, 40, rotation=90)
    boss = extrude(amount=-12)

    # Get boss face from extrusion result
    boss_face = boss.faces().sort_by(Axis.Y)[0]

    # Position hole in FACE LOCAL coordinates
    # (20, 0) means 20mm in face-local X, 0 in face-local Y
    with Locations(boss_face):
        with Locations((20, 0)):
            CounterBoreHole(8, 12, 3)

    # Add hole through base using global coordinates
    with Locations((30, 10, 15)):
        Hole(4)

result = bracket.part
export_gltf(result, "./25_face_coords.glb", binary=True)
print("Exported 25_face_coords.glb")
