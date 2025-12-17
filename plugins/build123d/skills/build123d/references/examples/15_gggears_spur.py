#!/usr/bin/env python3
"""
gggears - Spur Gear Example

Demonstrates creating meshed spur gears with gggears library.
Run with: uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python 15_gggears_spur.py
"""
from build123d import export_gltf, export_step
from gggears import SpurGear, UP

# Create two spur gears with different tooth counts
gear1 = SpurGear(
    number_of_teeth=12,
    module=2.0,           # 2mm module
    height=10.0,          # 10mm thick
    pressure_angle=0.349, # 20 degrees in radians
    profile_shift=0.0,    # No profile shift
    root_fillet=0.2,      # Add root fillet
)

gear2 = SpurGear(
    number_of_teeth=24,
    module=2.0,
    height=10.0,
    pressure_angle=0.349,
    enable_undercut=True,  # Show undercut calculation
    root_fillet=0.2,
)

# Mesh gear1 to gear2 (positions gear1 relative to gear2)
gear1.mesh_to(gear2, target_dir=UP)

# Build the 3D parts
part1 = gear1.build_part()
part2 = gear2.build_part()

# Combine for export
assembly = part1 + part2

# Export
export_gltf(assembly, "./spur_gears.glb", binary=True)
export_step(assembly, "./spur_gears.step")

print("Spur Gears Created:")
print(f"  Gear 1: {gear1.number_of_teeth} teeth, module={gear1.module}")
print(f"  Gear 2: {gear2.number_of_teeth} teeth, module={gear2.module}")
print(f"  Gear ratio: {gear2.number_of_teeth / gear1.number_of_teeth:.2f}:1")
print("Exported to spur_gears.glb and spur_gears.step")
