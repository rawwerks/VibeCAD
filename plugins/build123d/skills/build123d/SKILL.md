---
name: build123d
description: Create parametric 3D CAD models using Build123D Python library. Use when the user wants to create 3D models, CAD designs, mechanical parts, or generate STL/STEP files programmatically. Triggers include requests for 3D modeling, parametric design, mechanical engineering parts, or code-based CAD.
---

# Build123D CAD Modeling

Build123D is a Python CAD library that uses algebra-style syntax for creating parametric 3D models.

## Quick Start

```python
from build123d import *

# Create a simple box with a hole
with BuildPart() as part:
    Box(10, 10, 5)
    Cylinder(radius=2, height=5, mode=Mode.SUBTRACT)

# Export to STL
part.part.export_stl("output.stl")
```

## Core Concepts

### Context Managers

Build123D uses three main context managers:

- `BuildPart()` - For solid 3D objects
- `BuildSketch()` - For 2D sketches
- `BuildLine()` - For 1D paths/curves

### Algebra Operations

Combine shapes using algebra:

```python
# Union (add)
result = box + cylinder

# Subtract
result = box - cylinder

# Intersect
result = box & cylinder
```

### Mode Parameter

Control how shapes combine within context managers:

- `Mode.ADD` - Add to existing geometry (default)
- `Mode.SUBTRACT` - Remove from existing geometry
- `Mode.INTERSECT` - Keep only overlapping regions
- `Mode.REPLACE` - Replace existing geometry

## Common Patterns

### Parametric Box with Rounded Edges

```python
from build123d import *

def rounded_box(length, width, height, fillet_radius):
    with BuildPart() as part:
        Box(length, width, height)
        fillet(part.edges(), radius=fillet_radius)
    return part.part

model = rounded_box(20, 15, 10, 2)
model.export_stl("rounded_box.stl")
```

### Extruded Profile

```python
from build123d import *

with BuildPart() as part:
    with BuildSketch() as sketch:
        Rectangle(20, 10)
        Circle(radius=3, mode=Mode.SUBTRACT)
    extrude(amount=5)

part.part.export_stl("extruded.stl")
```

### Revolved Shape

```python
from build123d import *

with BuildPart() as part:
    with BuildSketch(Plane.XZ) as sketch:
        with BuildLine() as line:
            Polyline([(0, 0), (10, 0), (10, 5), (5, 10), (0, 10)])
            Line(line.vertices()[-1], line.vertices()[0])
        make_face()
    revolve(axis=Axis.Z)
```

### Loft Between Profiles

```python
from build123d import *

with BuildPart() as part:
    with BuildSketch(Plane.XY) as s1:
        Circle(radius=10)
    with BuildSketch(Plane.XY.offset(20)) as s2:
        Rectangle(15, 15)
    loft()
```

## Export Options

```python
# STL (mesh for 3D printing)
part.part.export_stl("model.stl")

# STEP (precise CAD format)
part.part.export_step("model.step")

# SVG (2D projection)
part.part.export_svg("model.svg")
```

## Positioning and Alignment

```python
from build123d import *

# Position at specific location
box = Box(10, 10, 5)
box = Pos(5, 0, 0) * box  # Move 5 units in X

# Align to origin
box = box.locate(Align.CENTER, Align.CENTER, Align.MIN)
```

## Best Practices

1. **Use parameters** - Define dimensions as variables at the top for easy modification
2. **Name your parts** - Use meaningful variable names for complex assemblies
3. **Build incrementally** - Test each step before adding complexity
4. **Check units** - Build123D uses millimeters by default
5. **Validate exports** - View STL files in a mesh viewer before printing
