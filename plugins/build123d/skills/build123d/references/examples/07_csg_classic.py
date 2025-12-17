#!/usr/bin/env python3
"""
Classic CSG example: Sphere-box intersection with cylinder holes

Run with: uvx --from build123d python 07_csg_classic.py
"""
from build123d import Sphere, Box, Cylinder, Axis, export_gltf

# Create a sphere and a box centered at the origin
sphere = Sphere(radius=20)
box = Box(length=30, width=30, height=30)

# Boolean intersection of sphere and box
body = sphere & box

# Create three orthogonal cylinders centered at the origin
cylinder_x = Cylinder(radius=10, height=60)
cylinder_y = cylinder_x.rotate(axis=Axis.Y, angle=90)
cylinder_z = cylinder_x.rotate(axis=Axis.X, angle=90)

# Union the three cylinders
three_cylinders = cylinder_x + cylinder_y + cylinder_z

# Subtract the cylinder assembly from the body
result = body - three_cylinders

export_gltf(result, "./csg_classic.glb", binary=True)
print("Exported csg_classic.glb")

# result already defined above - harness compatible
