# 5-Minute Quick Start

Get Claude controlling PyMOL in 5 minutes.

## Prerequisites

- PyMOL installed on your system
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI installed
- Python 3.10+

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/ANaka/ai-mol
cd ai-mol
```

### 2. Set Up the PyMOL Plugin

Add this line to your `~/.pymolrc` (create the file if it doesn't exist):

```python
run /path/to/ai-mol/claude_socket_plugin.py
```

Replace `/path/to/ai-mol` with the actual path where you cloned the repository.

### 3. Start Using It

Open Claude Code in the `ai-mol` directory:

```bash
claude
```

Then say:

> "Open PyMOL and load structure 1UBQ"

Claude will launch PyMOL, connect to it, and load the structure.

## What You Can Do

### Basic Visualization

- "Load PDB 4HHB and show as cartoon"
- "Color the protein by secondary structure"
- "Show the surface and make it semi-transparent"

### Binding Sites

- "Load 1HSG and show the ligand binding site"
- "Highlight hydrogen bonds between ligand and protein"

### Structure Comparison

- "Align these two structures and calculate RMSD"
- "Show where the conformations differ"

### Publication Figures

- "Create a publication-quality figure with ray tracing"
- "Make a 360-degree rotation movie"

## Troubleshooting

### "Cannot connect to PyMOL"

1. Make sure PyMOL is running
2. Run `claude_status` in PyMOL's command line to check the listener
3. Try `claude_stop` then `claude_start` in PyMOL

### Plugin Not Loading

1. Verify the path in `~/.pymolrc` is correct
2. Check PyMOL's output for errors on startup
3. Try running `run /path/to/ai-mol/claude_socket_plugin.py` manually in PyMOL

### Need More Help?

Run `/pymol-setup` in Claude Code for guided setup assistance.

## Learn More

See [README.md](README.md) for full documentation and available skills.
