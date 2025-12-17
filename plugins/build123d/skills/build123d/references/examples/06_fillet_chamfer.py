#!/usr/bin/env python3
"""
Edge operations: Fillet (round) and Chamfer (bevel)

Run with: uvx --from build123d python 06_fillet_chamfer.py
"""
from build123d import Box, fillet, chamfer, export_gltf, Pos

# Create boxes
box1 = Box(30, 30, 30)
box2 = Box(30, 30, 30)

# Fillet: round all edges (must specify edges!)
filleted = fillet(box1.edges(), radius=5)

# Chamfer: bevel all edges (must specify edges!)
chamfered = chamfer(box2.edges(), length=3)

# Combine
result = filleted + Pos(50, 0, 0) * chamfered

export_gltf(result, "./fillet_chamfer.glb", binary=True)
print("Exported fillet_chamfer.glb")

# result already defined above - harness compatible
