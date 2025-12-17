#!/usr/bin/env python3
"""
gggears - Cycloid Gear Example

Demonstrates cycloid gears (used in precision mechanisms, clocks, pumps).
Run with: uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python 19_gggears_cycloid.py
"""
from build123d import export_gltf, export_step
from gggears import CycloidGear, UP

# Create cycloid gear pair
# Cycloid gears use rolling circle profiles instead of involute
gear1 = CycloidGear(
    number_of_teeth=8,
    module=3.0,
    height=8.0,
    inside_cycloid_coefficient=0.5,  # Inner rolling circle ratio
    outside_cycloid_coefficient=0.5,  # Outer rolling circle ratio
    root_fillet=0.1,
    tip_fillet=0.1,
)

gear2 = CycloidGear(
    number_of_teeth=16,
    module=3.0,
    height=8.0,
    inside_cycloid_coefficient=0.5,
    outside_cycloid_coefficient=0.5,
    root_fillet=0.1,
    tip_fillet=0.1,
)

# Adapt cycloid radii for proper meshing
gear1.adapt_cycloid_radii(gear2)

# Mesh the gears
gear1.mesh_to(gear2, target_dir=UP)

# Build parts
part1 = gear1.build_part()
part2 = gear2.build_part()

assembly = part1 + part2

export_gltf(assembly, "./cycloid_gears.glb", binary=True)
export_step(assembly, "./cycloid_gears.step")

print("Cycloid Gears Created:")
print(f"  Gear 1: {gear1.number_of_teeth} teeth")
print(f"  Gear 2: {gear2.number_of_teeth} teeth")
print(f"  Cycloid profile - smoother than involute for low tooth counts")
print("  Applications: clocks, precision mechanisms, gear pumps")
print("Exported to cycloid_gears.glb and cycloid_gears.step")
