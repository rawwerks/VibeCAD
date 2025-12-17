# Agent Instructions

This project uses **bd** (beads) for issue tracking. Run `bd onboard` to get started.

## Quick Reference

```bash
bd ready              # Find available work
bd show <id>          # View issue details
bd update <id> --status in_progress  # Claim work
bd close <id>         # Complete work
bd sync               # Sync with git
```

## Planning

**Convert all plans to bd epics/issues with full notes and dependency graphs.** When you create a plan file, translate it into:
- An epic for the overall effort
- Individual issues for each task
- Dependencies between issues (`bd dep add`)
- Full context in issue bodies

## Landing the Plane (Session Completion)

**When ending a work session**, you MUST complete ALL steps below. Work is NOT complete until `git push` succeeds.

**MANDATORY WORKFLOW:**

1. **File issues for remaining work** - Create issues for anything that needs follow-up
2. **Run quality gates** (if code changed) - Tests, linters, builds
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```
5. **Clean up** - Clear stashes, prune remote branches
6. **Verify** - All changes committed AND pushed
7. **Hand off** - Provide context for next session

**CRITICAL RULES:**
- Work is NOT complete until `git push` succeeds
- NEVER stop before pushing - that leaves work stranded locally
- NEVER say "ready to push when you are" - YOU must push
- If push fails, resolve and retry until it succeeds

## Adding Skills to VibeCAD

### Skill Structure

```
plugins/<plugin-name>/skills/<skill-name>/
├── SKILL.md              # Required: frontmatter + instructions
└── references/           # Optional: detailed docs, examples
    ├── <reference>.md    # Detailed documentation
    └── examples/         # Runnable example scripts
```

### Progressive Disclosure (Critical)

Skills use a three-level loading system:
1. **Metadata** (name + description in frontmatter) - Always in context
2. **SKILL.md body** - Loaded when skill triggers
3. **references/** - Loaded as needed by Claude

**Rules:**
- Keep SKILL.md under 500 lines
- Put detailed API docs in `references/`
- SKILL.md should point to references, not duplicate them
- Add source repo links for external dependencies

### Adding a New Skill

1. **Create bd epic/issues** for tracking
2. **Verify the tool works** with uvx or target runtime
3. **Create example scripts** - test each as you create it
4. **Create reference docs** - comprehensive API coverage
5. **Update SKILL.md** - minimal info + pointers to references
6. **Test all examples** - verify exports/outputs
7. **Commit and push**

### Adding build123d Extensions (like bd_warehouse)

For libraries that extend build123d:

1. **Verify uvx installation**: `uvx --from build123d --with <library> python -c "import <library>; print('OK')"`

2. **Create examples** in `references/examples/` numbered sequentially (09_, 10_, etc.)
   - Each example should be self-contained and runnable
   - Export to GLB/STL to verify geometry
   - Include print statements showing what was created

3. **Create reference doc** in `references/<library>-reference.md`
   - Source repo and docs links at top
   - Modules overview table
   - API details per module
   - Examples table at bottom

4. **Update SKILL.md**
   - Add library-specific triggers to frontmatter description
   - Add minimal section: uvx command + pointer to reference
   - Add source repo link

5. **Update quick-reference.md**
   - Add import examples only (no API details)
   - Point to detailed reference

### Example: Adding bd_warehouse

```bash
# 1. Verify installation
uvx --from build123d --with bd_warehouse python -c "from bd_warehouse.thread import IsoThread; print('OK')"

# 2. Create examples (test each)
uvx --from build123d --with bd_warehouse python 09_bd_warehouse_threads.py

# 3. Files created:
#    - references/bd-warehouse-reference.md (full API)
#    - references/examples/09-14_bd_warehouse_*.py (6 examples)

# 4. Files updated:
#    - SKILL.md (triggers + minimal section)
#    - references/quick-reference.md (imports only)
```

### Source Repositories

Always link to source repos for external dependencies:
- **build123d**: https://github.com/gumyr/build123d
- **bd_warehouse**: https://github.com/gumyr/bd_warehouse

