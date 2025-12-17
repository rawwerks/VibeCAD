#!/usr/bin/env python3
"""
bd_warehouse threads example - Run with:
uvx --from build123d --with bd_warehouse python 09_bd_warehouse_threads.py
"""
from build123d import (
    Box, Cylinder, Pos, export_gltf, export_stl,
    Axis, Location, Align, Mode, MM
)
from bd_warehouse.thread import IsoThread, AcmeThread

# Create an M10 external ISO thread (like a bolt)
bolt_thread = IsoThread(
    major_diameter=10 * MM,
    pitch=1.5 * MM,
    length=25 * MM,
    external=True,
    end_finishes=("chamfer", "fade"),  # chamfer at start, fade at end
)

# Create a bolt head (hex approximated as cylinder)
bolt_head = Cylinder(radius=8 * MM, height=6 * MM, align=(Align.CENTER, Align.CENTER, Align.MIN))
bolt_head = Pos(0, 0, 25 * MM) * bolt_head  # Position above thread

# Combine into bolt
bolt = bolt_thread + bolt_head

# Create an M10 internal ISO thread (like a nut - the threaded hole)
nut_body = Cylinder(radius=9 * MM, height=8 * MM)
nut_thread = IsoThread(
    major_diameter=10 * MM,
    pitch=1.5 * MM,
    length=8 * MM,
    external=False,  # Internal thread
    end_finishes=("fade", "fade"),
)
nut = nut_body - nut_thread  # Subtract thread from cylinder

# Position nut to the side
nut = Pos(30 * MM, 0, 0) * nut

# Create an Acme thread (power screw) - 1/2" size
acme_thread = AcmeThread(
    size="1/2",  # 1/2 inch
    length=40 * MM,
    external=True,
    end_finishes=("fade", "fade"),
)
acme_thread = Pos(60 * MM, 0, 0) * acme_thread

# Combine all parts
result = bolt + nut + acme_thread

# Export
export_gltf(result, "./threads_example.glb", binary=True)
export_stl(result, "./threads_example.stl")

print("Exported: threads_example.glb, threads_example.stl")
print(f"ISO Bolt thread: M10x1.5, 25mm length")
print(f"ISO Nut thread: M10x1.5 internal, 8mm thick")
print(f"Acme thread: 1/2 inch, 40mm length")
