# claudemol Distribution Design

## Decision

Monorepo with two distribution paths:
- **pip package** (`claudemol`) for PyMOL plugin + connection code
- **Claude Code plugin** (`claudemol-skills`) for skills, distributed from same repo

## Target Users

Both:
- Claude Code users who want PyMOL integration
- PyMOL users who want AI assistance

## Repository Structure

```
claudemol/
├── pyproject.toml              # pip package config
├── src/
│   └── claudemol/
│       ├── __init__.py
│       ├── connection.py       # PyMOLConnection class
│       ├── session.py          # Session management
│       ├── view.py             # View utilities
│       ├── plugin.py           # Socket plugin (copied to PyMOL)
│       └── cli.py              # Entry point for `claudemol setup`
├── claude-plugin/              # Claude Code plugin
│   ├── .claude-plugin/
│   │   └── plugin.json
│   └── skills/
│       ├── pymol-fundamentals/
│       ├── binding-site-visualization/
│       ├── antibody-visualization/
│       └── ... (all skills)
└── README.md
```

## Distribution

### pip package

```bash
pip install claudemol
claudemol setup  # Installs PyMOL plugin, configures ~/.pymolrc
```

Package includes:
- `claudemol.connection` - Socket communication with PyMOL
- `claudemol.session` - Session management utilities
- CLI command `claudemol setup` to configure PyMOL

### Claude Code plugin

```bash
/plugin marketplace add ANaka/claudemol?path=claude-plugin
/plugin install claudemol-skills
```

Plugin includes:
- All visualization skills (pymol-fundamentals, binding-site, antibody, etc.)
- README pointing to pip package for setup

## User Flows

**PyMOL user discovers pip package:**
1. `pip install claudemol`
2. `claudemol setup`
3. README mentions: "For Claude Code users, install the skills plugin"

**Claude Code user discovers skills plugin:**
1. `/plugin marketplace add ...`
2. `/plugin install claudemol-skills`
3. Plugin README says: "Requires `pip install claudemol && claudemol setup`"

## Versioning

Single version in pyproject.toml applies to pip package. Plugin has its own version in plugin.json. They can diverge but should stay roughly aligned.

## Trade-offs Accepted

- Coupled git history (skills + code together)
- Plugin install URL slightly longer due to path parameter
- Need to coordinate if versions diverge significantly
