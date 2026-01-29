# Key Molecular Visualization Categories

## Categories to Master (from curriculum analysis)

### 1. Protein Structure Basics
- Cartoon representations
- Secondary structure coloring
- B-factor visualization
- Multiple representations (cartoon + sticks + surface)

### 2. Ligand Binding
- Binding site visualization
- Protein-ligand interactions (H-bonds, hydrophobic)
- Pharmacophore features
- Binding pocket cavities

### 3. Structural Comparisons
- Alignment of multiple structures
- RMSD calculations
- Conformational changes (morphing)
- Wild-type vs mutant

### 4. Antibody/Immunology
- CDR loop identification and coloring
- Antibody-antigen interfaces
- Epitope mapping
- Paratope surface visualization

### 5. Membrane Proteins
- TM helix identification
- Membrane orientation
- Ion channel pores
- GPCR topology

### 6. Crystallography
- Electron density maps
- Crystal symmetry
- Resolution-dependent visualization

### 7. Large Assemblies
- Viral capsids
- Ribosomes
- Multi-subunit complexes

## Priority Order

For becoming a useful "claude-mol" assistant, focus on:

1. **Ligand Binding** - Most common use case in drug discovery
2. **Structural Comparisons** - Essential for understanding mutations, conformations
3. **Antibody/Immunology** - High-value therapeutic area
4. **Protein Structure Basics** - Foundation for everything else

## Publication-Quality Checklist

For each category, I should be able to:

- [ ] Create a compelling overview figure
- [ ] Create relevant detail views
- [ ] Apply appropriate color schemes
- [ ] Ray-trace at publication resolution
- [ ] Explain what the figure shows biologically
- [ ] Create a reusable skill/function for the pattern

## Progress

### Ligand Binding ✓
- [x] Overview figure (1HSG HIV protease)
- [x] Detail views (binding site close-up)
- [x] Color scheme (green ligand, white pocket, gray protein)
- [x] Ray-traced at 1200x900
- [x] Skill: `binding-site-visualization`

### Structural Comparisons ✓
- [x] Conformational change (calmodulin 9.55Å RMSD)
- [x] WT vs mutant (p53 R248Q 0.42Å RMSD)
- [x] Multi-view (overview, side, detail)
- [x] Color scheme (marine vs salmon)
- [x] Skill: `structure-alignment-analysis` (enhanced)

### Antibody/Immunology ✓
- [x] Fab-antigen complex (trastuzumab/HER2)
- [x] CDR loop identification and coloring
- [x] Epitope/paratope interface
- [x] Multi-view (overview, paratope, surface, interface)
- [x] Skill: `antibody-visualization` (created)

### Protein Structure Basics ✓
- [x] Overview figure (GFP beta-barrel)
- [x] Multiple representations (cartoon, surface, sticks)
- [x] Secondary structure coloring (helix=blue, sheet=orange, loop=gray)
- [x] B-factor visualization (blue_white_red spectrum)
- [x] Skill: `protein-structure-basics` (created)

### Membrane Proteins
- [ ] TM helix identification
- [ ] Membrane orientation
- [ ] Not yet attempted

### Crystallography
- [ ] Electron density maps
- [ ] Already done in Tier 2 curriculum
- [ ] Need to consolidate into skill

### Large Assemblies
- [ ] Viral capsids (done: Zika in curriculum)
- [ ] Need to consolidate into skill
