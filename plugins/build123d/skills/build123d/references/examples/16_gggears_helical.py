#!/usr/bin/env python3
"""
gggears - Helical Gear Example

Demonstrates helical gears and herringbone (double-helix) gears.
Run with: uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python 16_gggears_helical.py
"""
from math import pi
from build123d import export_gltf, export_step, Pos, Compound
from gggears import HelicalGear, UP

# Create helical gear pair
gear1 = HelicalGear(
    number_of_teeth=15,
    helix_angle=pi / 6,   # 30 degrees helix angle
    module=2.0,
    height=12.0,
    herringbone=False,    # Single helix
    profile_shift=0.2,    # Small profile shift
    root_fillet=0.15,
)

gear2 = HelicalGear(
    number_of_teeth=30,
    helix_angle=pi / 6,   # Must match for proper meshing
    module=2.0,
    height=12.0,
    herringbone=False,
    root_fillet=0.15,
)

# Mesh the gears
gear1.mesh_to(gear2, target_dir=UP)

# Build parts
part1 = gear1.build_part()
part2 = gear2.build_part()

# Also create a herringbone gear example (offset to the side)
herringbone1 = HelicalGear(
    number_of_teeth=15,
    helix_angle=pi / 6,
    module=2.0,
    height=15.0,
    herringbone=True,     # Double helix (herringbone)
    root_fillet=0.15,
)

herringbone2 = HelicalGear(
    number_of_teeth=30,
    helix_angle=pi / 6,
    module=2.0,
    height=15.0,
    herringbone=True,
    root_fillet=0.15,
)

herringbone1.mesh_to(herringbone2, target_dir=UP)

# Build and offset herringbone parts
hb_part1 = Pos(100, 0, 0) * herringbone1.build_part()
hb_part2 = Pos(100, 0, 0) * herringbone2.build_part()

# Combine all using Compound for proper export
assembly = Compound(children=[part1, part2, hb_part1, hb_part2])

export_gltf(assembly, "./helical_gears.glb", binary=True)
export_step(assembly, "./helical_gears.step")

print("Helical Gears Created:")
print(f"  Left pair: Single helix, 15:30 teeth")
print(f"  Right pair: Herringbone (double helix), 15:30 teeth")
print(f"  Helix angle: 30 degrees")
print("Exported to helical_gears.glb and helical_gears.step")
