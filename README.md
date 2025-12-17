# VibeCAD

A library of Claude Code skills for teaching coding agents how to use various CAD tools.

Sponsored by [neThing.xyz](https://neThing.xyz)

## Installation

Add the marketplace to Claude Code:

```
/plugin marketplace add raymondweitekamp/VibeCAD
```

Then install the plugins you need:

```
/plugin install build123d@vibecad
/plugin install render-glb@vibecad
/plugin install gltf-transform@vibecad
```

## Using Skills

After installation, invoke skills using the format `<plugin-name>:<skill-name>`:

| Plugin | Skill Invocation |
|--------|------------------|
| build123d | `build123d:build123d` |
| render-glb | `render-glb:render-glb` |
| gltf-transform | `gltf-transform:gltf-transform` |

Skills are automatically triggered when Claude detects relevant tasks (CAD modeling, GLB rendering, model optimization), or you can explicitly load them.

## Available Plugins

### build123d

Skills for using [Build123D](https://github.com/gumyr/build123d) - a Python CAD library for creating parametric 3D models with code.

- Algebra-style syntax for intuitive model creation
- Parametric design patterns
- Export to GLB, STL, STEP, and other formats
- Includes bd_warehouse (threads, fasteners, pipes, flanges, bearings)
- Includes gggears (spur, helical, bevel, planetary, cycloid gears)

### render-glb

Render GLB 3D models to PNG images for visual verification.

- Zero-setup with `bunx render-glb model.glb output.png`
- Enables agents to see what they build and iterate visually
- Configurable resolution and background color

### gltf-transform

Optimize and post-process GLB/glTF 3D models.

- Draco/Meshopt compression for web delivery
- Texture compression (WebP)
- Mesh simplification and welding
- Model inspection and merging

## Contributing

We welcome contributions! To add a new CAD tool:

1. Create a new plugin directory under `plugins/`
2. Add `.claude-plugin/plugin.json` with the plugin manifest
3. Add skills under `skills/` with `SKILL.md` files
4. Update the marketplace.json to include your plugin
5. Submit a PR

### Skill Format

Each skill requires a `SKILL.md` with YAML frontmatter:

```yaml
---
name: skill-name
description: What the skill does and when to use it
---

# Skill Name

Instructions for using the skill...
```

## License

MIT License - see [LICENSE](LICENSE) for details.
