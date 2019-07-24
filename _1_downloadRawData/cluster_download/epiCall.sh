#!/bin/bash
#BSUB -W 00:2git 
#BSUB -n 1
#BSUB -R rusage[mem=256]
#BSUB -q condo_grid
#BSUB -e onlineFlu_%J.err
#BSUB -o onlineFlu_%J.out

export PYTHONPATH="/home/tm66a/pythonPackages" # need to change this to your own profile.
source /etc/profile.d/modules.sh # specific to UMASS cluster
module load python3/3.5.0        # specific to UMASS cluster

cd ~/adaptively_stacking_ensembles_for_infleunza_forecasting_with_incomplete_data/_1_downloadRawData/

# execute program
echo Year = ${year}
echo Region = ${region}
echo "Starting"
python3 downloadRawData_inputYearAndRegion.py ${year} ${region}
echo "finished"
