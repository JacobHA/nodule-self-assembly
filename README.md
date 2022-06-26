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
- Speed up Euclidean distance calculation (maybe don't need sqrt...? https://stackoverflow.com/questions/37794849/efficient-and-precise-calculation-of-the-euclidean-distance)
- Use rng for reproducibility in speed testing!!
-[x] Allow cells to grow
 

### Visualization:
- Make axis log scale on histogram
- Remove axes on gif?


## Dependencies
Numpy
Matplotlib

### Optional:
cProfile
snakeviz (for visualizing profiler output)