# build123d Quick Reference

Run scripts with: `uvx --from build123d python script.py`

## Imports (IMPORTANT)

Export functions are in the **main module**, NOT in `build123d.exporters`:

```python
# CORRECT
from build123d import Sphere, Box, Cylinder, export_gltf, export_step, export_stl

# WRONG - will fail with ImportError
from build123d.exporters import export_gltf  # Does not exist here!
```

## Common Shapes

```python
from build123d import Sphere, Box, Cylinder, Cone, Torus

sphere = Sphere(radius=20)
box = Box(10, 20, 30)           # length, width, height
cylinder = Cylinder(radius=5, height=20)
cone = Cone(bottom_radius=10, top_radius=5, height=15)
torus = Torus(major_radius=20, minor_radius=5)
```

## Export Functions

```python
from build123d import export_gltf, export_step, export_stl, export_brep

# GLB (binary glTF) - for web/3D viewers
export_gltf(shape, "./model.glb", binary=True)

# STEP - for CAD interchange
export_step(shape, "./model.step")

# STL - for 3D printing
export_stl(shape, "./model.stl")

# BREP - OpenCASCADE native format
export_brep(shape, "./model.brep")
```

## Boolean Operations

```python
from build123d import Sphere, Box

sphere = Sphere(radius=20)
box = Box(30, 30, 30)

union = sphere + box           # Fuse shapes
difference = box - sphere      # Cut sphere from box
intersection = sphere & box    # Common volume
```

## Positioning

```python
from build123d import Sphere, Pos, Rot

# Translate
sphere = Sphere(radius=10)
moved = Pos(10, 0, 0) * sphere     # Move 10 units in X

# Rotate (degrees)
rotated = Rot(0, 0, 45) * sphere   # Rotate 45 degrees around Z
```

## Example: Complete Script

```python
#!/usr/bin/env python3
from build123d import Sphere, Box, export_gltf, Pos

# Create shapes
sphere = Sphere(radius=20)
box = Pos(15, 0, 0) * Box(10, 10, 10)

# Boolean union
model = sphere + box

# Export to GLB
export_gltf(model, "./model.glb", binary=True)
print("Exported to ./model.glb")
```

## bd_warehouse (Parametric Parts)

Run with: `uvx --from build123d --with bd_warehouse python script.py`

```python
from bd_warehouse.thread import IsoThread
from bd_warehouse.fastener import HexNut, SocketHeadCapScrew
from bd_warehouse.gear import SpurGear
from bd_warehouse.pipe import Pipe
from bd_warehouse.flange import WeldNeckFlange
from bd_warehouse.bearing import SingleRowDeepGrooveBallBearing
```

**Full API & examples**: See `bd-warehouse-reference.md`

## Source Repositories

- **build123d**: https://github.com/gumyr/build123d
- **bd_warehouse**: https://github.com/gumyr/bd_warehouse
