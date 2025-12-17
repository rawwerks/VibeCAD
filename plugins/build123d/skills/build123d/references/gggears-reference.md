# gggears Reference

Advanced parametric gear generation library for build123d. Creates various gear types with proper involute and cycloid tooth profiles.

**Source**: https://github.com/GarryBGoode/gggears
**License**: Apache 2.0

## Installation

Run scripts with gggears using uvx (zero-setup):

```bash
uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python script.py
```

## Supported Gear Types

| Class | Type | Use Case |
|-------|------|----------|
| `SpurGear` | Straight-tooth cylindrical | General power transmission |
| `HelicalGear` | Angled-tooth cylindrical | Smooth, quiet operation |
| `BevelGear` | Conical | Angled shaft transmission (90°) |
| `SpurRingGear` | Internal straight-tooth | Planetary systems |
| `HelicalRingGear` | Internal angled-tooth | Planetary systems |
| `CycloidGear` | Cycloid profile | Precision, low tooth count |
| `InvoluteRack` | Linear straight | Rack and pinion |
| `HelicalRack` | Linear angled | Smooth rack and pinion |

---

## SpurGear

Standard involute spur gear with straight teeth.

```python
from gggears import SpurGear, UP

gear = SpurGear(
    number_of_teeth=24,       # Required: tooth count
    module=2.0,               # Gear module (pitch diameter / teeth)
    height=10.0,              # Gear thickness
    pressure_angle=0.349,     # 20 degrees in radians (default)
    profile_shift=0.0,        # Profile shift coefficient
    enable_undercut=True,     # Calculate undercut (default True)
    root_fillet=0.0,          # Root fillet coefficient
    tip_fillet=0.0,           # Tip fillet coefficient
    tip_truncation=0.1,       # Tip truncation coefficient
    addendum_coefficient=1.0, # Addendum height coefficient
    dedendum_coefficient=1.2, # Dedendum height coefficient
    backlash=0,               # Backlash coefficient
    crowning=0,               # Tooth crowning coefficient
    z_anchor=0,               # Z-axis reference point
)

# Mesh to another gear
gear.mesh_to(other_gear, target_dir=UP, backlash=0.1, angle_bias=0)

# Build 3D part
part = gear.build_part()
```

### Key Parameters

- **module**: `pitch_diameter = module * number_of_teeth`
- **pressure_angle**: Standard is 20° (0.349 rad) or 14.5° (0.253 rad)
- **profile_shift**: Positive moves pitch line outward, prevents undercut
- **backlash**: Gap between meshed teeth (0.05-0.2 typical)
- **angle_bias**: -1 to 1, distributes backlash between gears

---

## HelicalGear

Helical gears with angled teeth for smoother operation.

```python
from gggears import HelicalGear
from math import pi

gear = HelicalGear(
    number_of_teeth=20,
    helix_angle=pi / 6,       # 30 degrees helix angle
    herringbone=False,        # True for double-helix
    module=2.0,
    height=15.0,
    # ... same parameters as SpurGear
)
```

### Helix Angle

- **Common values**: 15° to 30° (pi/12 to pi/6)
- **Meshing rule**: Both gears must have same helix angle
- **Herringbone**: Set `herringbone=True` for double-helix (no thrust load)

---

## BevelGear

Conical gears for transmitting power between angled shafts.

```python
from gggears import BevelGear
from math import pi, atan

# For 90° shaft angle: tan(gamma1)/tan(gamma2) = N1/N2
teeth1, teeth2 = 12, 24
gamma1 = atan(teeth1 / teeth2)
gamma2 = atan(teeth2 / teeth1)

gear = BevelGear(
    number_of_teeth=teeth1,
    cone_angle=gamma1 * 2,    # Full cone angle
    helix_angle=0,            # Spiral angle (0 = straight bevel)
    height=15.0,              # Tooth face length
    module=2.0,
    # ... same parameters as SpurGear
)
```

### Cone Angle Calculation

For shaft angle θ (typically 90°):
```python
gamma1 = atan(sin(theta) / (N2/N1 + cos(theta)))
gamma2 = theta - gamma1
```

---

## Ring Gears (SpurRingGear, HelicalRingGear)

Internal-tooth gears for planetary systems.

```python
from gggears import SpurRingGear, HelicalRingGear

ring = SpurRingGear(
    number_of_teeth=60,
    module=2.0,
    height=12.0,
    enable_undercut=False,         # Not recommended for rings
    root_fillet=0.2,
    addendum_coefficient=1.2,      # Reversed for internal teeth
    dedendum_coefficient=1.0,
)

# Helical version
ring = HelicalRingGear(
    number_of_teeth=60,
    helix_angle=pi / 6,
    herringbone=True,
    module=2.0,
    height=12.0,
    root_fillet=0.15,
)
```

### Planetary System Design

```python
# Ring teeth = Sun teeth + 2 * Planet teeth
sun_teeth = 12
planet_teeth = 18
ring_teeth = sun_teeth + 2 * planet_teeth  # = 48
```

---

## CycloidGear

Cycloid profile gears for precision mechanisms.

```python
from gggears import CycloidGear

gear = CycloidGear(
    number_of_teeth=12,
    module=3.0,
    height=8.0,
    inside_cycloid_coefficient=0.5,   # Inner rolling circle ratio
    outside_cycloid_coefficient=0.5,  # Outer rolling circle ratio
    inside_teeth=False,               # True for ring gear mode
    # ... standard parameters
)

# Adapt radii for proper meshing
gear1.adapt_cycloid_radii(gear2)
gear1.mesh_to(gear2, target_dir=UP)
```

### Cycloid Coefficients

- **0.5**: Standard full cycloid profile
- **Lower values**: Shallower teeth
- **Applications**: Clocks, gear pumps, precision mechanisms

---

## Racks (InvoluteRack, HelicalRack)

Linear gear elements for rack-and-pinion systems.

```python
from gggears import InvoluteRack, HelicalRack, RIGHT

# Spur rack
rack = InvoluteRack(
    number_of_teeth=30,
    module=2.0,
    height=15.0,              # Rack width
    root_fillet=0.15,
    tip_fillet=0.1,
    beta_angle=0,             # Slant angle
)

# Helical rack
rack = HelicalRack(
    number_of_teeth=30,
    module=2.0,
    height=15.0,
    helix_angle=pi / 6,       # Must match pinion
    herringbone=True,
)

# Mesh to gear
rack.mesh_to(gear, target_dir=RIGHT, offset=0)
```

### Linear Travel

```python
# Travel per pinion revolution
travel = pi * module * pinion_teeth
```

---

## Common Methods

### mesh_to()

Positions one gear relative to another for proper meshing.

```python
gear1.mesh_to(
    gear2,                    # Target gear
    target_dir=UP,            # Direction vector (UP, DOWN, LEFT, RIGHT)
    backlash=0.1,             # Optional backlash override
    angle_bias=0,             # -1 to 1, backlash distribution
)
```

### build_part()

Generates build123d Part object for export/visualization.

```python
part = gear.build_part()
export_gltf(part, "gear.glb", binary=True)
```

### update_part()

Updates existing part after position/angle changes.

```python
gear.angle = 0.5  # Rotate gear
gear.update_part()
```

---

## Direction Constants

```python
from gggears import UP, DOWN, LEFT, RIGHT, FRONT, BACK

# UP    = (0, 1, 0)
# DOWN  = (0, -1, 0)
# LEFT  = (-1, 0, 0)
# RIGHT = (1, 0, 0)
# FRONT = (0, 0, 1)
# BACK  = (0, 0, -1)
```

---

## Examples

Located in `examples/`:

| Example | Demonstrates |
|---------|--------------|
| `15_gggears_spur.py` | Basic spur gear pair |
| `16_gggears_helical.py` | Helical and herringbone gears |
| `17_gggears_bevel.py` | Bevel gears for 90° shafts |
| `18_gggears_planetary.py` | Planetary gear system |
| `19_gggears_cycloid.py` | Cycloid gear pair |
| `20_gggears_rack.py` | Rack and pinion systems |

Run any example:
```bash
uvx --from build123d --with "gggears @ git+https://github.com/GarryBGoode/gggears" python examples/15_gggears_spur.py
```
