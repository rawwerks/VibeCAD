#!/usr/bin/env python3
"""
Construction Sequence: Build Order Matters

Recommended order for complex parts:
1. Foundation (base)
2. Major features (bosses, protrusions)
3. Cuts (holes, slots)
4. Final trimming (RectangleRounded + INTERSECT for corner radii)
"""
from build123d import *

with BuildPart() as bracket:
    # 1. FOUNDATION - always first
    with BuildSketch():
        Rectangle(100, 50)
        with Locations((15, 0)):
            SlotOverall(60, 12, mode=Mode.SUBTRACT)
    extrude(amount=15)

    # 2. MAJOR FEATURES - save results for face references
    with BuildSketch(Plane.XZ.offset(25)):
        with Locations((-30, 15)):
            SlotOverall(50, 40, rotation=90)
    boss = extrude(amount=-12)
    split(bisect_by=Plane.XY)

    # 3. CUTS - use saved extrusion for face placement
    with Locations(boss.faces().sort_by(Axis.Y)[0]):
        with Locations((18, 0)):
            CounterBoreHole(8, 12, 3)
    mirror(about=Plane.XZ)

    # Add mounting holes
    with Locations((40, 15, 15)):
        Hole(4)
    mirror(about=Plane.XZ)

    # 4. FINAL TRIMMING - applies corner radii via intersection
    with BuildSketch():
        RectangleRounded(100, 50, 6)
    extrude(amount=80, mode=Mode.INTERSECT)

result = bracket.part
export_gltf(result, "./26_construction_sequence.glb", binary=True)
