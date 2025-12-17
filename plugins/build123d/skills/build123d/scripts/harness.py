#!/usr/bin/env python3
"""
build123d Harness - Run scripts and inspect geometry properties.

Usage:
    uvx --from build123d python harness.py <script.py> [output.glb]

The script must define a `result` variable containing the geometry to export.
Outputs: GLB file, geometry properties (volume, bbox, topology).
"""

import sys
import os
import runpy
import subprocess
import argparse
from pathlib import Path

from build123d import export_gltf


def get_geometry_properties(shape):
    """Extract properties from a build123d shape."""
    props = {}

    # Bounding box
    try:
        bbox = shape.bounding_box()
        props["bounding_box"] = {
            "min": (bbox.min.X, bbox.min.Y, bbox.min.Z),
            "max": (bbox.max.X, bbox.max.Y, bbox.max.Z),
            "size": (bbox.max.X - bbox.min.X, bbox.max.Y - bbox.min.Y, bbox.max.Z - bbox.min.Z)
        }
    except Exception as e:
        props["bounding_box"] = f"Error: {e}"

    # Volume
    try:
        props["volume"] = shape.volume
    except Exception as e:
        props["volume"] = f"Error: {e}"

    # Surface area
    try:
        props["area"] = shape.area
    except Exception as e:
        props["area"] = f"Error: {e}"

    # Center of mass
    try:
        com = shape.center()
        props["center"] = (com.X, com.Y, com.Z)
    except Exception as e:
        props["center"] = f"Error: {e}"

    # Topology counts
    try:
        props["vertices"] = len(shape.vertices())
    except Exception:
        props["vertices"] = "N/A"

    try:
        props["edges"] = len(shape.edges())
    except Exception:
        props["edges"] = "N/A"

    try:
        props["faces"] = len(shape.faces())
    except Exception:
        props["faces"] = "N/A"

    try:
        props["solids"] = len(shape.solids())
    except Exception:
        props["solids"] = "N/A"

    return props


def print_properties(props):
    """Pretty print geometry properties."""
    print("\n" + "=" * 50)
    print("GEOMETRY PROPERTIES")
    print("=" * 50)

    if isinstance(props.get("bounding_box"), dict):
        bb = props["bounding_box"]
        print(f"\nBounding Box:")
        print(f"  Min: ({bb['min'][0]:.3f}, {bb['min'][1]:.3f}, {bb['min'][2]:.3f})")
        print(f"  Max: ({bb['max'][0]:.3f}, {bb['max'][1]:.3f}, {bb['max'][2]:.3f})")
        print(f"  Size: {bb['size'][0]:.3f} x {bb['size'][1]:.3f} x {bb['size'][2]:.3f}")
    else:
        print(f"\nBounding Box: {props.get('bounding_box', 'N/A')}")

    if isinstance(props.get("volume"), (int, float)):
        print(f"\nVolume: {props['volume']:.3f} cubic units")
    else:
        print(f"\nVolume: {props.get('volume', 'N/A')}")

    if isinstance(props.get("area"), (int, float)):
        print(f"Surface Area: {props['area']:.3f} square units")
    else:
        print(f"Surface Area: {props.get('area', 'N/A')}")

    if isinstance(props.get("center"), tuple):
        c = props["center"]
        print(f"\nCenter of Mass: ({c[0]:.3f}, {c[1]:.3f}, {c[2]:.3f})")
    else:
        print(f"\nCenter of Mass: {props.get('center', 'N/A')}")

    print(f"\nTopology:")
    print(f"  Vertices: {props.get('vertices', 'N/A')}")
    print(f"  Edges: {props.get('edges', 'N/A')}")
    print(f"  Faces: {props.get('faces', 'N/A')}")
    print(f"  Solids: {props.get('solids', 'N/A')}")

    print("=" * 50 + "\n")


def run_harness(script_path, output_path=None):
    """Run a build123d script and process the `result` object."""
    script_path = Path(script_path).resolve()

    if not script_path.exists():
        print(f"Error: Script not found: {script_path}")
        sys.exit(1)

    # Default output path
    if output_path is None:
        output_path = script_path.with_suffix(".glb")
    else:
        output_path = Path(output_path)

    print(f"Running: {script_path}")
    print(f"Output: {output_path}")

    # Run the script using runpy (standard library)
    try:
        script_result = runpy.run_path(str(script_path), run_name="__main__")
    except Exception as e:
        print(f"Error running script: {e}")
        sys.exit(1)

    # Get the result object
    if "result" not in script_result:
        print("Error: Script must define a 'result' variable with the geometry to export")
        sys.exit(1)

    result_shape = script_result["result"]

    # Get and print properties
    props = get_geometry_properties(result_shape)
    print_properties(props)

    # Export to GLB
    try:
        export_gltf(result_shape, str(output_path), binary=True)
        print(f"Exported: {output_path}")
        print(f"File size: {output_path.stat().st_size:,} bytes")
    except Exception as e:
        print(f"Error exporting GLB: {e}")
        sys.exit(1)

    # Run gltf-transform inspect if available
    print("\n" + "=" * 50)
    print("GLB INSPECTION (gltf-transform)")
    print("=" * 50)
    try:
        result = subprocess.run(
            ["gltf-transform", "inspect", str(output_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print(f"  gltf-transform not available: {result.stderr.strip()}")
    except FileNotFoundError:
        print("  gltf-transform not installed (optional: bun add -g @gltf-transform/cli)")
    except subprocess.TimeoutExpired:
        print("  gltf-transform timed out")
    except Exception as e:
        print(f"  Error running gltf-transform: {e}")

    return {
        "properties": props,
        "glb_path": output_path
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", help="Path to build123d script")
    parser.add_argument("output", nargs="?", help="Output GLB path (default: script_name.glb)")

    args = parser.parse_args()
    run_harness(args.script, args.output)
