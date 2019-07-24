#mcandrew

import argparse
import numpy as np
import pandas as pd
from glob import glob

def grabPrior(file):
    return float(file.split('/')[-1].split('_')[-1].replace('.csv',''))

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--preSeason"  , help="1 if the model should be fit to 2010/2011 (preseason) data, otherwise model runs for all seasons other than 2010/2011", nargs='?', type=int, default=0)
    args = parser.parse_args()

    if args.preSeason:
        fldr = "analysisData_preSeason"
    else:
        fldr = "analysisData"
    
    allLogScores = pd.DataFrame()
    for file in glob('./{:s}/ensembleScores__adaptscore*'.format(fldr)):
        d = pd.read_csv(file)
        d = d.dropna()
        d['modelType'] = 'dynamic'
        d['prior'] = grabPrior(file)
        allLogScores = allLogScores.append(d[['modelType','region','target','EWNum','logScore','logScore5','prior']])

    allLogScores.to_csv('./{:s}/allEnsembleScores.csv'.format(fldr))
