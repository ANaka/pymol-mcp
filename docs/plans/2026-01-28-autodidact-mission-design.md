# PyMOL MCP Autodidact Mission Design

## Overview

Claude will iteratively learn to use PyMOL MCP effectively through experimentation, then capture that knowledge as skills and documentation. Server improvements will be queued on a branch for later deployment.

## Constraints

- No MCP server restarts (user will be asleep during ralph loop)
- If MCP connection dies, continue with code/documentation work
- All server changes queued on branch, not deployed live

## Deliverables

### 1. Skills (Layered Approach)

**Foundation skill:**
- `pymol-fundamentals` - Selections, representations, colors, camera controls

**Domain workflow skills:**
- `structure-alignment-analysis`
- `binding-site-visualization`
- `publication-figures`
- `movie-creation`
- Additional skills as useful patterns emerge

### 2. COOKBOOK.md

User-facing guide organized by task:

- Quick Start (connecting, first visualization)
- Viewing Structures (load, represent, color)
- Comparing Structures (align, differences, RMSD)
- Binding Sites & Ligands (pocket visualization, interactions)
- Analysis (distances, angles, hydrogen bonds)
- Publication Figures (clean views, ray tracing, export)
- Movies & Animations (rotation, morphing, export)

Each section includes: natural language examples, explanations, tips learned.

### 3. Server Improvements Branch

Branch: `autodidact-improvements`

Track and fix:
- Missing commands
- Pattern issues (regex not matching natural phrasing)
- Parameter gaps
- Error handling improvements

Each commit explains what was learned and why the change helps.

### 4. Learning Log

`learning-log.md` - Scratch file tracking:
- What was tried
- What worked/failed
- Recovery context if things break

## Learning Cycle

```
EXPLORE → TEST → DOCUMENT → IMPROVE
```

**EXPLORE:** Pick domain, review available commands, form workflow hypotheses.

**TEST:** Execute commands through MCP. Try realistic tasks. Note successes, failures, gaps.

**DOCUMENT:** Working patterns → skills. User workflows → COOKBOOK. Learnings → log.

**IMPROVE:** Missing commands → server code. Awkward patterns → refactoring notes.

## Exploration Order

1. Protein visualization basics (foundation)
2. Structural analysis & alignment
3. Ligand & binding site work
4. Multi-structure comparison
5. Publication figures
6. Movies & animations

## Skill Testing Approach

Skills tested with realistic scenarios before finalizing. During ralph loop, Claude is own test subject - if workflow doesn't work when attempting to use it, skill needs fixing.

## Success Criteria

- Foundation skill covers core PyMOL operations
- At least 3 domain workflow skills completed
- COOKBOOK.md provides clear user guidance
- Server improvements branch ready for review
- Learning log captures experiments for debugging
