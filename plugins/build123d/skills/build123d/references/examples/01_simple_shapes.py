#!/usr/bin/env python3
"""
Basic shapes: Box, Sphere, Cylinder, Cone, Torus

Run with: uvx --from build123d python 01_simple_shapes.py
"""
from build123d import Box, Sphere, Cylinder, Cone, Torus, export_gltf, Pos

# Basic shapes
box = Box(30, 20, 10)              # length, width, height
sphere = Sphere(radius=15)
cylinder = Cylinder(radius=10, height=25)
cone = Cone(bottom_radius=15, top_radius=5, height=20)
torus = Torus(major_radius=20, minor_radius=5)

# Position them in a row for visualization
shapes = (
    box
    + Pos(50, 0, 0) * sphere
    + Pos(100, 0, 0) * cylinder
    + Pos(150, 0, 0) * cone
    + Pos(200, 0, 0) * torus
)

export_gltf(shapes, "./simple_shapes.glb", binary=True)
print("Exported simple_shapes.glb")

# For harness compatibility
result = shapes
