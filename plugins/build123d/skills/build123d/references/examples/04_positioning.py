#!/usr/bin/env python3
"""
Positioning: Pos (translate), Rot (rotate)

Run with: uvx --from build123d python 04_positioning.py
"""
from build123d import Box, Sphere, export_gltf, Pos, Rot

# Original shape at origin
box = Box(20, 20, 20)

# Translate: move in X, Y, Z
moved_x = Pos(40, 0, 0) * box      # Move 40 units in X
moved_y = Pos(0, 40, 0) * box      # Move 40 units in Y
moved_z = Pos(0, 0, 40) * box      # Move 40 units in Z

# Rotate: angles in degrees around X, Y, Z axes
rotated_z = Rot(0, 0, 45) * box               # 45 degrees around Z
rotated_y = Pos(80, 0, 0) * Rot(0, 45, 0) * box  # 45 degrees around Y, then translate

# Combine all
result = box + moved_x + moved_y + moved_z + rotated_z + rotated_y

export_gltf(result, "./positioning.glb", binary=True)
print("Exported positioning.glb")

# result already defined above - harness compatible
