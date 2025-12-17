#!/usr/bin/env python3
"""
bd_warehouse gears example - Run with:
uvx --from build123d --with bd_warehouse python 11_bd_warehouse_gears.py

Demonstrates spur gears with proper meshing calculation.
"""
from build123d import (
    Cylinder, Pos, export_gltf, export_stl, MM, Rot, Align
)
from bd_warehouse.gear import SpurGear

# Gear parameters
module = 2  # Module (pitch diameter / tooth count) in mm
pressure_angle = 20  # Standard pressure angle in degrees
thickness = 8 * MM  # Gear thickness

# Create a driving gear (pinion) with 12 teeth
pinion_teeth = 12
pinion = SpurGear(
    module=module,
    tooth_count=pinion_teeth,
    pressure_angle=pressure_angle,
    thickness=thickness,
)

# Create a driven gear with 24 teeth (2:1 ratio)
gear_teeth = 24
gear = SpurGear(
    module=module,
    tooth_count=gear_teeth,
    pressure_angle=pressure_angle,
    thickness=thickness,
)

# Calculate meshing distance: module * (n1 + n2) / 2
# This is the center-to-center distance for proper meshing
mesh_distance = module * (pinion_teeth + gear_teeth) / 2
print(f"Mesh distance: {mesh_distance} mm")

# Position the driven gear at the mesh distance
# Rotate slightly to mesh teeth properly (half tooth pitch)
tooth_rotation = 180 / gear_teeth  # Rotate by half a tooth
gear = Pos(mesh_distance, 0, 0) * Rot(0, 0, tooth_rotation) * gear

# Add shaft holes to both gears
pinion_shaft = Cylinder(radius=3 * MM, height=thickness + 2 * MM)
gear_shaft = Pos(mesh_distance, 0, 0) * Cylinder(radius=5 * MM, height=thickness + 2 * MM)

# Subtract shaft holes
pinion_with_hole = pinion - pinion_shaft
gear_with_hole = gear - gear_shaft

# Combine
result = pinion_with_hole + gear_with_hole

# Export
export_gltf(result, "./gears_example.glb", binary=True)
export_stl(result, "./gears_example.stl")

print("Exported: gears_example.glb, gears_example.stl")
print(f"Pinion: {pinion_teeth} teeth, {module * pinion_teeth}mm pitch diameter")
print(f"Gear: {gear_teeth} teeth, {module * gear_teeth}mm pitch diameter")
print(f"Gear ratio: {gear_teeth / pinion_teeth}:1")
