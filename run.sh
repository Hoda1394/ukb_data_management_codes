#!/bin/bash
#SBATCH -t 7-00:00:00
#SBATCH -n 30
#SBATCH -p gablab
#SBATCH --mem=64G
#SBATCH -o /om4/project/biobank/outputs/move_data-%j.out

set -e

source ~/.bashrc
conda activate datalad_env

export PATH="/om4/project/biobank/bin:$PATH"


datalad run -m 'moving data to subject datasets' 'python3 get_data.py'  

