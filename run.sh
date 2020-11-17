#!/bin/bash
#SBATCH --array=1-985%1
#SBATCH -t 7-00:00:00
#SBATCH -n 20
#SBATCH -p gablab
#SBATCH --mem=32G
#SBATCH -o /om4/project/biobank/outputs/move_data-%A-%3a.out

set -e

source ~/.bashrc
conda activate datalad_env

export PATH="/om4/project/biobank/bin:$PATH"

offset=$((($SLURM_ARRAY_TASK_ID*500)+6))

datalad run -m 'moving data to subject datasets' "python3 get_data.py $offset"  

# usage: sbatch run.sh