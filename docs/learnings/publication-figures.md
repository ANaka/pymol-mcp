# Publication-Quality Figure Guidelines

## Key Principles

1. **Purpose over speed** - Each figure should communicate a specific biological concept
2. **Multiple views** - Overview + detail views tell a complete story
3. **Consistent color schemes** - Colors should have meaning (e.g., warm=light chain, cool=heavy chain)
4. **Ray-tracing for final figures** - OpenGL is for exploration, ray-tracing for publication

## PyMOL Settings for Publication

```python
# Anti-aliasing
cmd.set("antialias", 2)

# Ray-trace mode (1 = quantized colors, cleaner look)
cmd.set("ray_trace_mode", 1)

# Lighting
cmd.set("ray_shadows", 0)  # Often cleaner without harsh shadows
cmd.set("depth_cue", 0)    # No fog unless needed
cmd.set("spec_reflect", 0.3)
cmd.set("ambient", 0.4)

# Smooth cartoons
cmd.set("cartoon_smooth_loops", 1)
cmd.set("cartoon_fancy_helices", 1)

# White background for print
cmd.bg_color("white")

# High-resolution output
# IMPORTANT: Always use ray() THEN png() without dimensions!
# cmd.png(path, width, height) causes a view inflation bug
cmd.ray(1200, 900)
cmd.png("figure.png")  # NO dimensions here - ray() already set them
```

## Critical: Avoiding the View Inflation Bug

**DO NOT** use `cmd.png(path, width, height)` with explicit dimensions.

This causes PyMOL's view matrix to become corrupted after multiple cycles, making the view zoom out to infinity.

**ALWAYS** use:
```python
cmd.ray(width, height)
cmd.png(path)  # No dimensions - ray already rendered at the right size
```

This applies to ALL image captures, not just ray-traced ones.

## Example: Antibody CDR Loops (Task 38)

### Figures produced:
1. **Overview** - Full Fab with CDRs highlighted in context
2. **Paratope view** - Looking down at antigen-binding surface
3. **Surface representation** - Shows binding surface shape

### Color scheme:
- Light chain CDRs: tv_red, salmon, lightorange
- Heavy chain CDRs: marine, slate, deepblue
- Framework: gray70 (light), gray50 (heavy)

### Key selections:
```python
cmd.select("CDR_L1", "chain A and resi 24-34")
cmd.select("CDR_L2", "chain A and resi 50-56")
cmd.select("CDR_L3", "chain A and resi 89-97")
cmd.select("CDR_H1", "chain B and resi 31-35")
cmd.select("CDR_H2", "chain B and resi 50-65")
cmd.select("CDR_H3", "chain B and resi 95-99")
```

## Workflow

1. Load and clean structure
2. Plan the story (what concept to communicate)
3. Set up selections and color scheme
4. Explore camera angles interactively
5. Apply publication settings
6. Ray-trace multiple views
7. Export at high resolution
