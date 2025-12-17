# VibeCAD

A library of Claude Code skills for teaching coding agents how to use various CAD tools.

## Installation

Add the marketplace to Claude Code:

```
/plugin marketplace add raymondweitekamp/VibeCAD
```

Then install the plugins you need:

```
/plugin install build123d@vibecad
```

## Available Plugins

### build123d

Skills for using [Build123D](https://github.com/gumyr/build123d) - a Python CAD library for creating parametric 3D models with code.

- Algebra-style syntax for intuitive model creation
- Parametric design patterns
- Export to STL, STEP, and other formats

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
