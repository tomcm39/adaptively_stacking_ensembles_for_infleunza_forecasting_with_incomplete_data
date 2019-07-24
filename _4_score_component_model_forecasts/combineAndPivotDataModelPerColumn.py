#mcandrew

import sys
import numpy as np
import pandas as pd
from glob import glob

def scoringFiles(FSN):
    if FSN:
        return glob('./analysisData/[!c][!d][!c]*.csv.gz')
    return glob('./analysisData/cdc*.csv.gz')

def defineLogScoresFileName(FSN):
    if FSN:
        return './analysisData/allFSNLogScores.csv'
    return './analysisData/allCDCLogScores.csv'

if __name__ == "__main__":

    allLogScores = pd.DataFrame()
    for file in scoringFiles(FSN=1):
        sys.stdout.write("\033[K")
        sys.stdout.write('\r{:100s}\r'.format(file))
        sys.stdout.flush()
        logScores = pd.read_csv(file)
        allLogScores = allLogScores.append(logScores)
    allLogScores = allLogScores.pivot_table(index=['region','calendarEW','target','EWNum']
                                            ,columns = ['model']
                                            ,values = 'logScore').reset_index()
    outFileName = defineLogScoresFileName(FSN=1)
    allLogScores.to_csv(outFileName)
