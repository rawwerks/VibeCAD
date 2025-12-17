#!/usr/bin/env python3
"""
Hole patterns using GridLocations

Run with: uvx --from build123d python 08_hole_pattern.py
"""
from build123d import (
    Box, Cylinder, extrude, Circle,
    GridLocations, Pos, export_gltf
)

# Create a base plate
plate = Box(100, 80, 10)

# Create a pattern of holes using GridLocations
# GridLocations(x_spacing, y_spacing, x_count, y_count)
holes = [
    Pos(loc.position.X, loc.position.Y, 0) * Cylinder(radius=5, height=20)
    for loc in GridLocations(20, 20, 4, 3)
]

# Subtract all holes from the plate
result = plate
for hole in holes:
    result = result - hole

export_gltf(result, "./hole_pattern.glb", binary=True)
print("Exported hole_pattern.glb")

# result already defined above - harness compatible
