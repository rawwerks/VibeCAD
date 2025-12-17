#!/usr/bin/env python3
"""
2D Sketches and Extrusion: Create shapes from 2D profiles

Run with: uvx --from build123d python 05_sketch_extrude.py
"""
from build123d import (
    Circle, Rectangle, RegularPolygon,
    extrude, export_gltf
)

# Simple circle extruded to cylinder
circle = Circle(radius=15)
cylinder = extrude(circle, amount=30)

# Rectangle with circle cut out, then extruded
plate_sketch = Rectangle(50, 30) - Circle(radius=8)
plate = extrude(plate_sketch, amount=5)

# Hexagon extruded
hexagon = RegularPolygon(radius=20, side_count=6)
hex_prism = extrude(hexagon, amount=15)

# Combine and export
from build123d import Pos
result = cylinder + Pos(60, 0, 0) * plate + Pos(120, 0, 0) * hex_prism

export_gltf(result, "./sketch_extrude.glb", binary=True)
print("Exported sketch_extrude.glb")

# result already defined above - harness compatible
