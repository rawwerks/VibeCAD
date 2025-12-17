# Claude Code Instructions

## Plugin Versioning (MANDATORY)

**When modifying ANY plugin, you MUST bump the version in `plugin.json`:**

| Change Type | Version Bump | Example |
|-------------|--------------|---------|
| New skill added | MINOR | 0.1.0 → 0.2.0 |
| Skill modified | PATCH | 0.2.0 → 0.2.1 |
| Breaking change | MAJOR | 0.2.1 → 1.0.0 |
| Bug fix | PATCH | 0.2.1 → 0.2.2 |

```bash
# After ANY plugin change, update version in:
plugins/<name>/.claude-plugin/plugin.json
```

**Why:** The `claude plugin update` command checks version strings to detect updates. If you don't bump the version, users won't get your changes.

## Plan Mode Workflow

When exiting plan mode, **always convert the plan to bd epics and issues first**:

1. Create an epic for the overall effort
2. Create individual issues for each task
3. Add dependencies between issues (`bd dep add <issue> <depends-on>`)
4. Include full context in issue descriptions
5. Then proceed with implementation

This ensures work is tracked, dependencies are clear, and progress is visible.

## Issue Tracking

This project uses **bd** (beads) for issue tracking:

```bash
bd ready                    # Find available work
bd create --title="..." --type=task --priority=2
bd update <id> --status=in_progress
bd close <id> --reason="..."
bd dep add <issue> <depends-on>
```

## Session End Protocol

Before ending any session:

1. `git status` - check what changed
2. `git add <files>` - stage changes
3. `bd sync --from-main` - sync beads
4. `git commit` - commit with descriptive message
5. `git push` - push to remote

Work is NOT complete until `git push` succeeds.
