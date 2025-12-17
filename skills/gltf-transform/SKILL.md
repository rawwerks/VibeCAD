---
name: gltf-transform
description: Optimize and post-process GLB/glTF 3D models. Use when compressing models for web delivery, reducing file size, simplifying geometry, inspecting model stats, merging models, or converting textures. Triggers on: optimize GLB, compress model, reduce file size, simplify mesh, draco compression, meshopt, webp textures, inspect model, merge GLB, model optimization.
---

# glTF Transform

Post-process GLB/glTF files: optimize, compress, inspect, and transform 3D models.

- CLI docs: https://gltf-transform.dev/cli
- GitHub: https://github.com/donmccurdy/glTF-Transform
- npm: `@gltf-transform/cli`

## Installation

```bash
npm install -g @gltf-transform/cli
```

## Quick Start

```bash
# Inspect model stats first
gltf-transform inspect model.glb

# One-command optimization (good defaults)
gltf-transform optimize input.glb output.glb --compress draco --texture-compress webp
```

## CAD Workflow Integration

Typical pipeline after generating models with build123d:

```
create geometry → export GLB → optimize → verify visually
```

1. **build123d** exports high-quality CAD geometry
2. **gltf-transform** compresses for web delivery
3. **render-glb** verifies the result

## Compression Methods

| Method | Best For | Trade-offs |
|--------|----------|------------|
| **Draco** | Web delivery, Three.js | Smallest geometry, requires decoder |
| **Meshopt** | Universal, animations | Good compression + animation support |
| **Quantize** | Compatibility | No decoder needed, moderate compression |

```bash
# Draco - best geometry compression
gltf-transform draco input.glb output.glb

# Meshopt - geometry + animation compression
gltf-transform meshopt input.glb output.glb

# Quantize only - no external decoder needed
gltf-transform quantize input.glb output.glb
```

## Texture Compression

```bash
# WebP - good compression, wide browser support
gltf-transform webp input.glb output.glb

# Resize large textures
gltf-transform resize input.glb output.glb --width 1024 --height 1024
```

## Common Operations

### Inspect Model Stats
```bash
gltf-transform inspect model.glb
```

Shows vertex count, file size breakdown, texture sizes - helps decide what to optimize.

### Simplify Geometry
```bash
# Weld duplicate vertices first
gltf-transform weld input.glb temp.glb

# Then simplify
gltf-transform simplify temp.glb output.glb --ratio 0.5
```

Useful for CAD models which often have more detail than needed for web viewing.

### Merge Multiple Models
```bash
gltf-transform merge part1.glb part2.glb assembly.glb
```

### Aggressive Optimization
```bash
gltf-transform optimize input.glb output.glb \
  --compress draco \
  --texture-compress webp \
  --simplify true \
  --simplify-ratio 0.5
```

## When to Use

| Scenario | Commands |
|----------|----------|
| Web delivery | `optimize --compress draco --texture-compress webp` |
| Check model stats | `inspect` |
| High-poly CAD model | `weld` then `simplify --ratio 0.5` |
| Combine parts | `merge` |
| Debug issues | `inspect` then targeted fixes |
