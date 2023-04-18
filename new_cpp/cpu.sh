#!/bin/bash
#SBATCH --job-name=nodules
#SBATCH --time=1:00:00
#SBATCH --mem-per-cpu=8gb
#SBATCH --cpus-per-task=4

#set an account to use
#if not used then default will be used
# for scavenger users, use this format:
##SBATCH --account=pi_first.last
# for contributing users, use this format:
##SBATCH --account=math

# Set filenames for stdout and stderr.  %j can be used for the jobid.
# see "filename patterns" section of the sbatch man page for
# additional options
#SBATCH --error=outfiles/%x-%A_%a.err
#SBATCH --output=outfiles/%x-%A_%a.out

# set the partition where the job will run.  Multiple partitions can
# be specified as a comma separated list
# Use command "sinfo" to get the list of partitions
#SBATCH --partition=Intel6248
# https://www.umb.edu/rc/hpc/chimera/chimera_scheduler


# Can comment this out (for single node jobs)

# Put your job commands here, including loading any needed
# modules or diagnostic echos. Needed for GPU partitions:
export USER=jacob.adamczyk001
export HOME=/home/jacob.adamczyk001
source /etc/profile


eval "$(conda shell.bash hook)"
conda activate /home/jacob.adamczyk001/miniconda3/envs/oblenv
export CPATH=$CPATH:$CONDA_PREFIX/include
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib


echo "starting task $SLURM_ARRAY_TASK_ID"
echo "using $SLURM_CPUS_ON_NODE CPUs"
echo `date`

python eps_expt_rate.py

# Diagnostic/Logging Information
echo "Finish Run"
echo "end time is `date`"

# To run this file, use sbatch --options submit.sh
# (see --options at top of this file, using this in cmd line will overwrite those options at top of file)