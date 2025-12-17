# Advanced build123d Patterns

## Two Modes: Algebra vs Builder

### Algebra Mode (Simple, Direct)
```python
from build123d import Sphere, Box, export_gltf
result = Sphere(radius=20) - Box(15, 15, 40)
export_gltf(result, "./out.glb", binary=True)
```

### Builder Mode (Context Managers)
```python
from build123d import *

with BuildPart() as part:
    with BuildSketch() as profile:
        Rectangle(30, 4, align=Align.MIN)
        Rectangle(4, 30, align=Align.MIN)
    extrude(amount=100)
    fillet(part.edges().filter_by(lambda e: e.is_interior), 5)

export_gltf(part.part, "./out.glb", binary=True)
```

## Edge Selection and Filtering

```python
from build123d import Box, fillet, chamfer, Axis

box = Box(30, 30, 30)

# Fillet all edges
filleted = fillet(box, radius=3)

# Fillet only top edges (filter by Z position)
top_edges = box.edges().filter_by_position(Axis.Z, 25, 30)
filleted_top = fillet(box, top_edges, radius=3)

# Fillet edges parallel to Z axis
z_edges = box.edges().filter_by(Axis.Z)
filleted_z = fillet(box, z_edges, radius=3)
```

## Sketch to 3D Operations

### Extrude
```python
from build123d import Circle, Rectangle, extrude

profile = Rectangle(50, 30) - Circle(radius=10)
solid = extrude(profile, amount=20)
```

### Revolve
```python
from build123d import Rectangle, Axis, revolve

profile = Rectangle(10, 30)
vase = revolve(profile, axis=Axis.Y, revolution_arc=360)
```

### Loft (Connect Multiple Profiles)
```python
from build123d import Circle, Rectangle, loft, Plane

bottom = Circle(radius=20)
top = Plane.XY.offset(50) * Circle(radius=10)
tapered = loft([bottom, top])
```

### Sweep (Profile Along Path)
```python
from build123d import Circle, Helix, sweep

path = Helix(pitch=10, height=50, radius=20)
profile = Circle(radius=3)
spring = sweep(profile, path)
```

## Units

```python
from build123d import MM, CM, IN

box = Box(10 * CM, 5 * CM, 2 * CM)  # 100mm x 50mm x 20mm
hole = Cylinder(radius=0.25 * IN, height=3 * CM)  # 6.35mm radius
```

## Alignment

```python
from build123d import Box, Align

# Center aligned (default)
box1 = Box(10, 10, 10)

# Corner aligned
box2 = Box(10, 10, 10, align=(Align.MIN, Align.MIN, Align.MIN))

# Mixed alignment
box3 = Box(10, 10, 10, align=(Align.CENTER, Align.MIN, Align.MAX))
```

## Grid Patterns

```python
from build123d import Box, Cylinder, GridLocations, Pos

plate = Box(100, 80, 10)

# Create hole pattern: 4 columns x 3 rows, 20mm spacing
for loc in GridLocations(20, 20, 4, 3):
    hole = Pos(loc.position.X, loc.position.Y, 0) * Cylinder(radius=5, height=20)
    plate = plate - hole
```

## Helix (Springs, Threads)

```python
from build123d import Helix, Circle, sweep

# Create a spring
helix_path = Helix(pitch=10, height=50, radius=20)
wire_profile = Circle(radius=2)
spring = sweep(wire_profile, helix_path)

# Helix with direction
helix = Helix(75, 150, 15, center=(0, 0, 0), direction=(0, 0, 1))
```

Example: `roller_coaster.py`

## Shelling (Hollow Parts)

```python
from build123d import *

with BuildPart() as vase:
    # Create solid shape first
    with BuildSketch() as profile:
        # ... profile sketch
    revolve(axis=Axis.Y)

    # Shell it - remove material from inside, keeping wall thickness
    # openings= specifies which face(s) to remove
    offset(openings=vase.faces().filter_by(Axis.Y)[-1], amount=-1)
```

Example: `vase.py`

## Pack Algorithm (2D Bin Packing)

```python
import build123d as bd

# Create random boxes
boxes = [bd.Box(10, 10, 5), bd.Box(15, 8, 5), bd.Box(20, 12, 5)]

# Pack them in 2D with padding
packed = bd.pack(boxes, padding=3)

# Result is a list of positioned shapes
result = bd.Compound(packed)
```

Example: `packed_boxes.py`

## Joints for Assembly

```python
from build123d import *

# Create parts
with BuildPart() as body:
    Box(50, 30, 10)
    # Define a joint location on this part
    RigidJoint("attachment_point", joint_location=Location((0, 0, 5)))

with BuildPart() as attachment:
    Cylinder(radius=5, height=20)
    RigidJoint("base", joint_location=Location((0, 0, 0)))

# Connect parts using joints
body.joints["attachment_point"].connect_to(attachment.joints["base"])

# Result: attachment is now positioned relative to body
result = Compound([body.part, attachment.part])
```

Joint types: `RigidJoint`, `RevoluteJoint`, `LinearJoint`, `BallJoint`

Example: `toy_truck.py`

## Multi-Color 3MF Export

```python
from build123d import Box, Cylinder, Mesher, export_3mf, Color

# Create colored parts
red_part = Box(20, 20, 10)
red_part.color = Color("red")

blue_part = Cylinder(radius=5, height=15)
blue_part.color = Color("blue")

# Export as multi-color 3MF
mesher = Mesher()
mesher.add_shape(red_part)
mesher.add_shape(blue_part)
export_3mf(mesher.mesh, "./multicolor.3mf")
```

Example: `dual_color_3mf.py`
