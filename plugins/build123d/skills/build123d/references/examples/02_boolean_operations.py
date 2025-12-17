#!/usr/bin/env python3
"""
Boolean operations: Union (+), Difference (-), Intersection (&)

Run with: uvx --from build123d python 02_boolean_operations.py
"""
from build123d import Box, Sphere, Cylinder, export_gltf, Pos

# Union: combine shapes
sphere = Sphere(radius=20)
box = Box(30, 30, 30)
union_result = sphere + Pos(15, 0, 0) * box

# Difference: subtract one shape from another
base = Box(40, 40, 40)
hole = Cylinder(radius=10, height=50)
difference_result = base - hole

# Intersection: keep only overlapping volume
sphere2 = Sphere(radius=25)
box2 = Box(35, 35, 35)
intersection_result = sphere2 & box2

# Export all three
export_gltf(union_result, "./boolean_union.glb", binary=True)
export_gltf(difference_result, "./boolean_difference.glb", binary=True)
export_gltf(intersection_result, "./boolean_intersection.glb", binary=True)

print("Exported boolean_union.glb, boolean_difference.glb, boolean_intersection.glb")

# For harness compatibility (difference is most interesting)
result = difference_result
