#mcandrew

import sys
import pandas as pd
from glob import glob

if __name__ == "__main__":

    allEWS = []
    for model in glob('./aggregatedComponentForecasts/*'):
        sys.stdout.write('\r{:100s}\r'.format(model))
        sys.stdout.flush()
        forecastData = pd.read_csv(model,low_memory=False)
        
        EWS = list(forecastData.EWNum.unique())
        allEWS = set(list(allEWS)+EWS)

    fout = open('./allPossibleEpidemicWeeks.csv','w')
    for ew in sorted(allEWS):
        fout.write('{:d}\n'.format(ew))
    fout.close()
