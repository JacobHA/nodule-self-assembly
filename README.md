# nodule-self-assembly
 Modelling the self-assembly seen among cancer cells

![link to gif](/simulation_results/animation_of_gif_folder.gif)
![link to histogram](/simulation_results/animation_of_histograms.gif)

# TODO:
*Need to try profiling and find possible speedups*

### Modelling:
- "Repellent" mechanism / genotypes
- Cells that inherit repellent / attractive genes (cancer cells "want" to spread i.e. invade)

### Calculations:
- Do subgridding / more efficient collision detection
- Check for collisions across the boundary (we have periodic BCs)
- Speed up plotting (there seems to be a memory leak with matplotlib multiple figures)
-[x] Allow cells to grow
 

### Visualization:
- Make axis log scale on histogram
- Remove axes on gif?


## Dependencies
Numpy
Matplotlib
