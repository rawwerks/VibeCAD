#!/usr/bin/env python3
"""
bd_warehouse bearings example - Run with:
uvx --from build123d --with bd_warehouse python 14_bd_warehouse_bearings.py

Demonstrates bearing creation and housing design.
"""
from build123d import (
    Cylinder, Box, Pos, export_gltf, export_stl, MM, Align
)
from bd_warehouse.bearing import SingleRowDeepGrooveBallBearing

# Create a skateboard bearing (608 type: 8mm bore, 22mm OD, 7mm width)
# Size format is "M[bore]-[OD]-[width]"
bearing = SingleRowDeepGrooveBallBearing(size="M8-22-7")

# Create a second bearing positioned to the side
bearing2 = Pos(50 * MM, 0, 0) * SingleRowDeepGrooveBallBearing(size="M8-22-7")

# Create a simple bearing housing block
# The housing has a hole sized for the bearing OD (22mm)
housing_block = Box(40 * MM, 40 * MM, 20 * MM, align=(Align.CENTER, Align.CENTER, Align.CENTER))
bearing_hole = Cylinder(radius=11 * MM, height=20 * MM)  # 22mm diameter hole for bearing
housing = housing_block - bearing_hole

# Position housing below the bearings for display
housing = Pos(0, -60 * MM, 0) * housing

# Create a shaft that fits through the bearing bore (8mm)
shaft = Cylinder(radius=4 * MM, height=60 * MM)
shaft = Pos(0, -60 * MM, 0) * shaft

# Create a larger bearing (10mm bore, 35mm OD, 11mm width)
large_bearing = SingleRowDeepGrooveBallBearing(size="M10-35-11")
large_bearing = Pos(100 * MM, 0, 0) * large_bearing

# Combine all parts
result = bearing + bearing2 + housing + shaft + large_bearing

# Export
export_gltf(result, "./bearings_example.glb", binary=True)
export_stl(result, "./bearings_example.stl")

print("Exported: bearings_example.glb, bearings_example.stl")
print("Parts created:")
print(f"  - 608 Bearing (8mm bore, 22mm OD, 7mm width) - skateboard type")
print(f"  - 608 Bearing copy at X=50mm")
print(f"  - Large Bearing (10mm bore, 35mm OD, 11mm width) at X=100mm")
print(f"  - Bearing housing block at Y=-60mm")
print(f"  - 8mm shaft through housing")

# Show available bearing info
print("\nBearing size format: M[bore]-[OD]-[width]")
print("Common sizes: M8-22-7 (608), M10-26-8, M10-35-11")
