#!/usr/bin/env python3
"""
bd_warehouse fasteners example - Run with:
uvx --from build123d --with bd_warehouse python 10_bd_warehouse_fasteners.py
"""
from build123d import (
    Box, Pos, export_gltf, export_stl, MM, IN, Locations, Align
)
from bd_warehouse.fastener import (
    HexNut, SocketHeadCapScrew, PlainWasher, ClearanceHole
)

# Create an M6 hex nut (ISO 4032 standard)
hex_nut = HexNut(size="M6-1", fastener_type="iso4032")

# Create an M6 socket head cap screw, 20mm long
cap_screw = SocketHeadCapScrew(
    size="M6-1",
    length=20 * MM,
    fastener_type="iso4762",
    simple=False,  # Full detail threads
)
cap_screw = Pos(25 * MM, 0, 0) * cap_screw

# Create a plain washer for M6
washer = PlainWasher(size="M6", fastener_type="iso7089")
washer = Pos(50 * MM, 0, 0) * washer

# Create a plate with clearance holes for the cap screw
plate = Box(80 * MM, 40 * MM, 10 * MM, align=(Align.MIN, Align.CENTER, Align.MIN))
plate = Pos(70 * MM, 0, 0) * plate

# Add clearance holes using ClearanceHole
simple_screw = SocketHeadCapScrew(size="M6-1", length=20 * MM, fastener_type="iso4762")

# Note: ClearanceHole is typically used in builder mode context
# For algebra mode, we create a simple demonstration plate

# Combine all visible parts (the plate is separate, holes shown conceptually)
result = hex_nut + cap_screw + washer + plate

# Export
export_gltf(result, "./fasteners_example.glb", binary=True)
export_stl(result, "./fasteners_example.stl")

print("Exported: fasteners_example.glb, fasteners_example.stl")
print("Parts created:")
print(f"  - M6 Hex Nut (ISO 4032)")
print(f"  - M6x20 Socket Head Cap Screw (ISO 4762)")
print(f"  - M6 Plain Washer (ISO 7089)")
print(f"  - Demo plate 80x40x10mm")

# Show available fastener info
print("\nAvailable HexNut types:", HexNut.types())
print("M6 HexNut sizes available:", "M6-1" in HexNut.sizes("iso4032"))
