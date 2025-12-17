#!/usr/bin/env python3
"""
gggears - Rack and Pinion Example

Demonstrates gear racks for linear motion conversion.
Run with: uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python 20_gggears_rack.py
"""
from math import pi
from build123d import export_gltf, export_step, Pos
from gggears import HelicalGear, HelicalRack, InvoluteRack, RIGHT

# Create a spur rack and pinion
pinion1 = HelicalGear(
    number_of_teeth=15,
    module=2.0,
    height=15.0,
    helix_angle=0,        # Spur gear (no helix)
    root_fillet=0.15,
)

rack1 = InvoluteRack(
    number_of_teeth=30,
    module=2.0,
    height=15.0,
    root_fillet=0.15,
    tip_fillet=0.1,
)

# Mesh rack to pinion
rack1.mesh_to(pinion1, target_dir=RIGHT)

# Build spur parts
pinion1_part = pinion1.build_part()
rack1_part = rack1.build_part()
spur_assembly = pinion1_part + rack1_part

# Create a helical rack and pinion (offset to the side)
pinion2 = HelicalGear(
    number_of_teeth=15,
    module=2.0,
    height=15.0,
    helix_angle=pi / 6,   # 30 degree helix
    herringbone=True,     # Double helix
    root_fillet=0.15,
)

rack2 = HelicalRack(
    number_of_teeth=30,
    module=2.0,
    height=15.0,
    helix_angle=pi / 6,
    herringbone=True,
    root_fillet=0.15,
)

rack2.mesh_to(pinion2, target_dir=RIGHT)

# Build and offset helical parts
pinion2_part = Pos(0, 100, 0) * pinion2.build_part()
rack2_part = Pos(0, 100, 0) * rack2.build_part()

# Combine all
assembly = spur_assembly + pinion2_part + rack2_part

export_gltf(assembly, "./rack_and_pinion.glb", binary=True)
export_step(assembly, "./rack_and_pinion.step")

print("Rack and Pinion Created:")
print(f"  Front: Spur rack and pinion, 15 teeth pinion")
print(f"  Back: Helical herringbone rack and pinion")
print(f"  Linear travel per pinion revolution: {pi * 2 * 15:.1f}mm")
print("Exported to rack_and_pinion.glb and rack_and_pinion.step")
