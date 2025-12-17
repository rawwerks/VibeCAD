#!/usr/bin/env python3
"""
Plane Offsets vs Positions: Two Different Concepts

Plane.XZ.offset(25) = plane moved 25mm in Y direction (distance)
Locations((-30, 15)) = position ON that plane (coordinates)

These are NOT the same! Don't confuse them.
"""
from build123d import *

with BuildPart() as demo:
    # Base for reference
    Box(100, 50, 20)

    # Sketch on XZ plane, offset 25mm in Y (front face of 50mm wide part)
    with BuildSketch(Plane.XZ.offset(25)):
        # Position (-30, 15) means X=-30, Z=15 on this offset plane
        with Locations((-30, 15)):
            Circle(8)
    extrude(amount=-10)  # Extrude into part

    # Another sketch on XZ plane, offset 25mm in negative Y (back face)
    with BuildSketch(Plane.XZ.offset(-25)):
        # Same position coords, different plane
        with Locations((-30, 15)):
            Circle(8)
    extrude(amount=10)

    # Add hole through top using Locations for position
    with Locations((20, 10, 20)):
        Hole(5, depth=20)

result = demo.part
export_gltf(result, "./22_plane_offsets.glb", binary=True)
