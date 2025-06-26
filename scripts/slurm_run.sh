#!/bin/bash

#SBATCH --job-name=HADDOCK3-docking
#SBATCH --output=HADDOCK3_%j.out
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=2
#SBATCH --mem=128GB
#SBATCH --partition=compute

echo "Starting HADDOCK3 Docking Job"
echo "SLURM_JOBID          = $SLURM_JOBID"
echo "SLURM_JOB_NODELIST   = $SLURM_JOB_NODELIST"
echo "SLURM_NNODES         = $SLURM_NNODES"
echo "SLURMTMPDIR          = $SLURMTMPDIR"
echo "Date                 = $(date)"
echo "Hostname             = $(hostname -s)"
echo "Working Directory    = $(pwd)"
echo "Submit Directory     = $SLURM_SUBMIT_DIR"

# Load necessary environment
source /lustre/oneApi/setvars.sh
export OMP_NUM_THREADS=1

# Run HADDOCK3 via Apptainer
cd /lustre/skhatri/haddock3/examples/docking-protein-protein


apptainer exec --bind /lustre/skhatri:/lustre/skhatri \
  /lustre/skhatri/haddock3_cpu-mpi.sif \
  haddock3 docking-protein-protein-test.cfg


echo "HADDOCK3 Job Complete"
echo "Completed at: $(date)"
