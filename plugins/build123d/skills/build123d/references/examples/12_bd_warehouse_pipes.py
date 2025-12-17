#!/usr/bin/env python3
"""
bd_warehouse pipes example - Run with:
uvx --from build123d --with bd_warehouse python 12_bd_warehouse_pipes.py

Demonstrates pipe creation with different materials and sizes.
"""
from build123d import (
    Edge, Pos, export_gltf, export_stl, MM, FT, Vector
)
from bd_warehouse.pipe import Pipe

# Create a 1" stainless steel pipe, 2 feet long (Schedule 10S)
# Path defines the pipe trajectory
straight_path = Edge.make_line((0, 0, 0), (2 * FT, 0, 0))

stainless_pipe = Pipe(
    nps="1",
    material="stainless",
    identifier="10S",
    path=straight_path,
)

# Create a 1/2" copper pipe (Type L), 18 inches long
copper_path = Edge.make_line((0, 50 * MM, 0), (18 * 25.4, 50 * MM, 0))  # 18 inches

copper_pipe = Pipe(
    nps="1/2",
    material="copper",
    identifier="L",
    path=copper_path,
)

# Create a 2" PVC pipe (Schedule 40), 1 foot long
pvc_path = Edge.make_line((0, 100 * MM, 0), (1 * FT, 100 * MM, 0))

pvc_pipe = Pipe(
    nps="2",
    material="pvc",
    identifier="40",
    path=pvc_path,
)

# Combine all pipes
result = stainless_pipe + copper_pipe + pvc_pipe

# Export
export_gltf(result, "./pipes_example.glb", binary=True)
export_stl(result, "./pipes_example.stl")

print("Exported: pipes_example.glb, pipes_example.stl")
print("Pipes created:")
print(f"  - 1\" Stainless Steel (Schedule 10S), 2 ft")
print(f"  - 1/2\" Copper (Type L), 18 in")
print(f"  - 2\" PVC (Schedule 40), 1 ft")

# Show available materials and identifiers
print("\nAvailable materials: abs, copper, iron, pvc, stainless, steel")
print("Copper identifiers: K, L, M")
print("Steel identifiers: 10, 20, 30, 40, 60, 80, 100, 120, 140, 160")
