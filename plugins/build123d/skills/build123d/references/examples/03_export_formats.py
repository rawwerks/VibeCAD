#!/usr/bin/env python3
"""
Export to different formats: GLB, STEP, STL, BREP

Run with: uvx --from build123d python 03_export_formats.py

Available export functions:
- export_gltf(shape, path, binary=True)  # GLB for web/3D viewers
- export_step(shape, path)               # STEP for CAD interchange
- export_stl(shape, path)                # STL for 3D printing
- export_brep(shape, path)               # BREP for OpenCASCADE
"""
import os
import tempfile
from build123d import Sphere, export_gltf, export_step, export_stl, export_brep

# Create a simple shape
sphere = Sphere(radius=20)

# Use /workspace if available (container), else temp directory
output_dir = "/workspace" if os.path.isdir("/workspace") else tempfile.gettempdir()

# GLB (binary glTF) - for web/3D viewers
export_gltf(sphere, f"{output_dir}/sphere.glb", binary=True)

# STEP - for CAD interchange (industry standard)
export_step(sphere, f"{output_dir}/sphere.step")

# STL - for 3D printing (mesh format)
export_stl(sphere, f"{output_dir}/sphere.stl")

# BREP - OpenCASCADE native format
export_brep(sphere, f"{output_dir}/sphere.brep")

print(f"Exported to {output_dir}: sphere.glb, sphere.step, sphere.stl, sphere.brep")

# For harness compatibility
result = sphere
