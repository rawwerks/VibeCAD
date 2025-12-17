#!/usr/bin/env python3
"""
Mode.INTERSECT: Reliable Corner Radii

RectangleRounded + extrude(mode=Mode.INTERSECT) trims corners reliably.
Use when fillet() fails on complex geometry.
"""
from build123d import *

# Complex part that might break fillet()
with BuildPart() as bracket:
    # Base with features
    with BuildSketch():
        Rectangle(100, 50)
    extrude(amount=15)

    # Add boss
    with BuildSketch(Plane.XY.offset(15)):
        with Locations((-30, 0)):
            Circle(20)
    extrude(amount=25)

    # Add ribs
    with BuildSketch(Plane.XZ.offset(0)):
        with Locations((-30, 15)):
            Rectangle(5, 25)
    extrude(amount=10, both=True)

    # Apply R6 corner radii via intersection (works reliably)
    with BuildSketch():
        RectangleRounded(100, 50, 6)
    extrude(amount=100, mode=Mode.INTERSECT)

result = bracket.part
export_gltf(result, "./24_intersection_corners.glb", binary=True)
