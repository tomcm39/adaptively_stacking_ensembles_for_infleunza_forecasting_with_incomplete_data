#mcandrew

import numpy as np
import pandas as pd
from glob import glob

if __name__ == "__main__":

    allWts = pd.DataFrame()
    for file in glob("./analysisData/ensembleWeights__staticweight*.csv"):
        d = pd.read_csv(file)
        d['modelType'] = "static" 
        allWts = allWts.append(d)
    for file in glob("./analysisData/ensembleWeights__adaptweight*.csv"):
        d = pd.read_csv(file)
        d['modelType'] = "dynamic" 
        allWts = allWts.append(d)
    allWts.to_csv('./analysisData/allEnsembleWeights.csv')
