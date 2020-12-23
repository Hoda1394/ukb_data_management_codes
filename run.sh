#!/bin/bash
#SBATCH --array=15-246%1
#SBATCH -t 3-00:00:00
#SBATCH -N 1
#SBATCH -n 30
#SBATCH --mem=40G
#SBATCH -o /om4/project/biobank/outputs/move_data-%A-%3a.out
##SBATCH -p gablab

set -e

source ~/.bashrc
conda activate datalad_env

export PATH="/om4/project/biobank/bin:$PATH"

offset=$((($SLURM_ARRAY_TASK_ID*2000)+506))

datalad run -m 'moving data to subject datasets' "python3 get_data.py $offset"  

# usage: sbatch run.sh