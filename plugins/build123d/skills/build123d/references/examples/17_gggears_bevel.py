#!/usr/bin/env python3
"""
gggears - Bevel Gear Example

Demonstrates bevel gears for transmitting power between angled shafts.
Run with: uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python 17_gggears_bevel.py
"""
from math import pi, atan
from build123d import export_gltf, export_step
from gggears import BevelGear, RIGHT

# Calculate cone angles for 90-degree shaft intersection
# For bevel gears: tan(gamma1)/tan(gamma2) = N1/N2
teeth1, teeth2 = 12, 24
gamma1 = atan(teeth1 / teeth2)  # Cone angle for gear 1
gamma2 = atan(teeth2 / teeth1)  # Cone angle for gear 2

# Small spiral angle for smoother operation
beta = pi / 12  # 15 degree spiral

gear1 = BevelGear(
    number_of_teeth=teeth1,
    module=2.0,
    height=15.0,          # Tooth face length
    cone_angle=gamma1 * 2,  # Full cone angle
    helix_angle=beta,     # Spiral angle
    root_fillet=0.15,
)

gear2 = BevelGear(
    number_of_teeth=teeth2,
    module=2.0,
    height=15.0,
    cone_angle=gamma2 * 2,
    helix_angle=-beta,    # Opposite spiral direction
    root_fillet=0.15,
)

# Mesh the gears
gear1.mesh_to(gear2, target_dir=RIGHT)

# Build parts
part1 = gear1.build_part()
part2 = gear2.build_part()

assembly = part1 + part2

export_gltf(assembly, "./bevel_gears.glb", binary=True)
export_step(assembly, "./bevel_gears.step")

print("Bevel Gears Created:")
print(f"  Gear 1: {teeth1} teeth, cone angle={gamma1 * 180 / pi:.1f} deg")
print(f"  Gear 2: {teeth2} teeth, cone angle={gamma2 * 180 / pi:.1f} deg")
print(f"  Spiral angle: {beta * 180 / pi:.1f} degrees")
print(f"  Shaft angle: 90 degrees")
print("Exported to bevel_gears.glb and bevel_gears.step")
