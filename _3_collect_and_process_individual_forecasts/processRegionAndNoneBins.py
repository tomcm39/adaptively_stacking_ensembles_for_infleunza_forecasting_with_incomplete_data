#mcandrew

import sys
import numpy as np
import pandas as pd

from glob import glob

def fixRegionAndNoneBins(forecastData):
        forecastData.loc[forecastData.bin0=='none','bin0']=-1 # models assign the probabily a peak, or onset, will never occur
        forecastData.loc[forecastData.bin1=='none','bin1']=-1 # models assign the probabily a peak, or onset, will never occur

        forecastData['region'] = forecastData['region'].str.split(' Region ').str.join('')
        forecastData.loc[forecastData['region']=='US National','region'] = 'Nat'
        return forecastData

if __name__ == "__main__":

    for model in glob('./aggregatedComponentForecasts/*.csv'):
        sys.stdout.write("\033[K")
        sys.stdout.write('\r{:100s}\r'.format(model))
        sys.stdout.flush()
        forecastData = pd.read_csv(model,low_memory=False)
        forecastData = fixRegionAndNoneBins(forecastData)
        forecastData.to_csv(model,index=False)
