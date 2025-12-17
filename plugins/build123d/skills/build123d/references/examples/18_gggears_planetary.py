#!/usr/bin/env python3
"""
gggears - Planetary Gear System Example

Demonstrates ring gears for planetary gear systems.
Run with: uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python 18_gggears_planetary.py
"""
from math import pi
from build123d import export_gltf, export_step, Pos, Rot, Compound
from gggears import HelicalGear, HelicalRingGear, UP

# Planetary gear system design
# Ring teeth = Sun teeth + 2 * Planet teeth
sun_teeth = 12
planet_teeth = 18
ring_teeth = sun_teeth + 2 * planet_teeth  # = 48

module = 2.0
height = 12.0
helix_angle = pi / 8  # 22.5 degrees

# Create sun gear (center)
sun_gear = HelicalGear(
    number_of_teeth=sun_teeth,
    module=module,
    height=height,
    helix_angle=helix_angle,
    herringbone=True,
    root_fillet=0.15,
)

# Create ring gear (outer, internal teeth)
ring_gear = HelicalRingGear(
    number_of_teeth=ring_teeth,
    module=module,
    height=height,
    helix_angle=helix_angle,
    herringbone=True,
    root_fillet=0.15,
)

# Create planet gears (3 planets evenly spaced)
planets = []
for i in range(3):
    planet = HelicalGear(
        number_of_teeth=planet_teeth,
        module=module,
        height=height,
        helix_angle=helix_angle,
        herringbone=True,
        root_fillet=0.15,
    )
    # Mesh planet to sun gear first
    planet.mesh_to(sun_gear, target_dir=UP)
    planets.append(planet)

# Build all parts
sun_part = sun_gear.build_part()
ring_part = ring_gear.build_part()

# Position planets around sun (120 degrees apart)
planet_parts = []
for i, planet in enumerate(planets):
    angle = i * 120  # degrees
    part = Rot(0, 0, angle) * planets[0].build_part()
    planet_parts.append(part)

# Combine all parts using Compound for proper export
all_parts = [sun_part, ring_part] + planet_parts
assembly = Compound(children=all_parts)

export_gltf(assembly, "./planetary_gears.glb", binary=True)
export_step(assembly, "./planetary_gears.step")

print("Planetary Gear System Created:")
print(f"  Sun gear: {sun_teeth} teeth")
print(f"  Planet gears: {planet_teeth} teeth (x3)")
print(f"  Ring gear: {ring_teeth} teeth")
print(f"  Module: {module}mm")
print(f"  Herringbone design for thrust load handling")
print("Exported to planetary_gears.glb and planetary_gears.step")
