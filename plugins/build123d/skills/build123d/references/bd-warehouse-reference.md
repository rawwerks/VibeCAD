# bd_warehouse Reference

Parametric parts library for build123d. Creates industry-standard mechanical components.

**Source**: https://github.com/gumyr/bd_warehouse
**Docs**: https://bd-warehouse.readthedocs.io/

## Installation

Run scripts with bd_warehouse using uvx (zero-setup):

```bash
uvx --from build123d --with bd_warehouse python script.py
```

## Modules Overview

| Module | Components | Use Case |
|--------|------------|----------|
| `thread` | IsoThread, AcmeThread, MetricTrapezoidalThread | Fastener threads, power screws |
| `fastener` | Nut, Screw, Washer + hole creation | Standard hardware |
| `gear` | SpurGear, InvoluteToothProfile | Power transmission |
| `pipe` | Pipe (various materials) | Plumbing, process piping |
| `flange` | WeldNeckFlange, SlipOnFlange, BlindFlange | Pipe connections |
| `bearing` | SingleRowDeepGrooveBallBearing | Rotary support |

---

## Thread Module

```python
from bd_warehouse.thread import IsoThread, AcmeThread, MetricTrapezoidalThread
```

### IsoThread (ISO Standard 60° threads)

```python
thread = IsoThread(
    major_diameter=10 * MM,  # Nominal thread diameter
    pitch=1.5 * MM,          # Thread pitch
    length=25 * MM,          # Thread length
    external=True,           # True=bolt, False=nut
    end_finishes=("chamfer", "fade"),  # Start and end finish
)
```

**End finishes:** `"raw"`, `"fade"`, `"square"`, `"chamfer"`

### AcmeThread (29° trapezoidal, imperial)

```python
thread = AcmeThread(
    size="1/2",        # Imperial size: "1/4", "3/8", "1/2", "3/4", "1", etc.
    length=40 * MM,
    external=True,
    end_finishes=("fade", "fade"),
)
```

### MetricTrapezoidalThread (ISO 2904, 30°)

```python
thread = MetricTrapezoidalThread(
    size="8x1.5",      # Format: "diameter x pitch"
    length=30 * MM,
    external=True,
)
```

---

## Fastener Module

```python
from bd_warehouse.fastener import (
    HexNut, SocketHeadCapScrew, PlainWasher,
    ClearanceHole, TapHole
)
```

### Common Fasteners

```python
# Hex Nut (ISO 4032)
nut = HexNut(size="M6-1", fastener_type="iso4032")

# Socket Head Cap Screw (ISO 4762)
screw = SocketHeadCapScrew(
    size="M6-1",
    length=20 * MM,
    fastener_type="iso4762",
    simple=False,  # True=faster, False=detailed threads
)

# Plain Washer (ISO 7089)
washer = PlainWasher(size="M6", fastener_type="iso7089")
```

### Size Format

- Metric: `"M6-1"` (M6 x 1.0 pitch)
- Imperial: `"#6-32"`, `"1/4-20"`

### Available Types

**Nuts:** `HexNut`, `DomedCapNut`, `HeatSetNut`, `SquareNut`

**Screws:** `SocketHeadCapScrew`, `ButtonHeadScrew`, `CounterSunkScrew`, `HexHeadScrew`, `PanHeadScrew`, `SetScrew`

**Washers:** `PlainWasher`, `ChamferedWasher`

### Hole Creation (Builder Mode)

```python
from bd_warehouse.fastener import ClearanceHole, TapHole

# Clearance hole for a screw
ClearanceHole(fastener=screw, fit="Normal", depth=None, counter_sunk=True)

# Tap hole (for threading)
TapHole(fastener=screw, material="Soft", depth=None)
```

---

## Gear Module

```python
from bd_warehouse.gear import SpurGear
```

### SpurGear

```python
gear = SpurGear(
    module=2,             # Pitch diameter / tooth count (mm)
    tooth_count=24,       # Number of teeth
    pressure_angle=20,    # Standard: 14.5 or 20 degrees
    thickness=8 * MM,     # Gear thickness
    root_fillet=0.5 * MM, # Optional fillet at tooth root
)
```

### Meshing Distance Formula

```python
# Center-to-center distance for proper meshing
mesh_distance = module * (teeth1 + teeth2) / 2
```

---

## Pipe Module

```python
from bd_warehouse.pipe import Pipe
```

### Pipe

```python
from build123d import Edge, FT

path = Edge.make_line((0, 0, 0), (5 * FT, 0, 0))

pipe = Pipe(
    nps="2",              # Nominal Pipe Size
    material="stainless", # Material type
    identifier="10S",     # Schedule/identifier
    path=path,            # Trajectory
)
```

### NPS Sizes

`"1/8"`, `"1/4"`, `"3/8"`, `"1/2"`, `"3/4"`, `"1"`, `"1 1/4"`, `"1 1/2"`, `"2"`, `"2 1/2"`, `"3"`, `"4"`, `"6"`, `"8"`, `"10"`, `"12"`, etc.

### Materials & Identifiers

| Material | Identifiers |
|----------|-------------|
| `"abs"` | `"40"` |
| `"copper"` | `"K"`, `"L"`, `"M"` |
| `"iron"` | `"STD"`, `"XS"`, `"XXS"` |
| `"pvc"` | `"40"`, `"80"` |
| `"stainless"` | `"5S"`, `"10S"`, `"20S"`, `"40S"`, `"80S"` |
| `"steel"` | `"10"`, `"20"`, `"30"`, `"40"`, `"60"`, `"80"`, etc. |

---

## Flange Module

```python
from bd_warehouse.flange import WeldNeckFlange, SlipOnFlange, BlindFlange
```

### Flange Types

```python
# Weld Neck - strongest, for high pressure
flange = WeldNeckFlange(
    nps="4",           # Nominal pipe size
    flange_class=150,  # Pressure rating
    face_type="Raised",
)

# Slip On - slides over pipe
flange = SlipOnFlange(nps="4", flange_class=150)

# Blind - closes pipe end
flange = BlindFlange(nps="4", flange_class=150)
```

### Flange Classes (Pressure Ratings)

`150`, `300`, `400`, `600`, `900`, `1500`, `2500`

### Face Types

`"Flat"`, `"Raised"`, `"Ring"`, `"Tongue"`, `"Groove"`, `"Male"`, `"Female"`

### Properties & Joints

```python
flange.od         # Outside diameter
flange.id         # Inside diameter (not BlindFlange)
flange.thickness  # Flange thickness

# Joints for assembly
flange.joints["pipe"]  # Pipe connection point
flange.joints["face"]  # Face connection point
```

---

## Bearing Module

```python
from bd_warehouse.bearing import SingleRowDeepGrooveBallBearing
```

### SingleRowDeepGrooveBallBearing

```python
bearing = SingleRowDeepGrooveBallBearing(size="M8-22-7")
```

**Size format:** `"M[bore]-[OD]-[width]"` in mm

### Common Sizes

| Size | Description |
|------|-------------|
| `"M8-22-7"` | 608 bearing (skateboard) |
| `"M10-26-8"` | 6000 series |
| `"M10-35-11"` | Larger 10mm bore |

### Available Sizes

Call `SingleRowDeepGrooveBallBearing.sizes("SKT")` to get all valid sizes.

---

## Examples

Located in `examples/`:

| Example | Module | Demonstrates |
|---------|--------|--------------|
| `09_bd_warehouse_threads.py` | thread | IsoThread, AcmeThread |
| `10_bd_warehouse_fasteners.py` | fastener | HexNut, SocketHeadCapScrew, PlainWasher |
| `11_bd_warehouse_gears.py` | gear | SpurGear with meshing calculation |
| `12_bd_warehouse_pipes.py` | pipe | Pipe (stainless, copper, pvc) |
| `13_bd_warehouse_flanges.py` | flange | WeldNeckFlange, SlipOnFlange, BlindFlange |
| `14_bd_warehouse_bearings.py` | bearing | SingleRowDeepGrooveBallBearing with housing |

Run any example:
```bash
uvx --from build123d --with bd_warehouse python examples/09_bd_warehouse_threads.py
```
