#mcandrew

import sys
import numpy as np
import pandas as pd

def downloadData(FSN):
    if FSN:
        return pd.read_csv('../../../_5_compute_and_score__ensembles/analysisData/allEnsembleScores.csv') 

def meanLogScore(d):
    return pd.Series({'avgLogScore':d.logScore.mean()})

def meanLogScore5(d):
    return pd.Series({'avgLogScore':d.logScore5.mean()})

def addSeason(d):
    d['year'] = d.EWNum.astype(str).str.slice(0,4).astype(int)
    d['week'] = d.EWNum.astype(str).str.slice(4,6).astype(int)

    idx = (d.week >= 40) & (d.week<=53)
    d.loc[idx,'season'] = d[idx].apply( lambda x: "{:d}/{:d}".format(x['year'],x['year']+1),1 )
    d.loc[~idx,'season'] = d[~idx].apply( lambda x:  "{:d}/{:d}".format(x['year']-1,x['year']),1)
    return d

def add1stHalgVs2ndHalf(d):
    d['year'] = d.EWNum.astype(str).str.slice(0,4).astype(int)
    d['week'] = d.EWNum.astype(str).str.slice(4,6).astype(int)

    idx = (d.week >= 40) & (d.week<=53)
    d.loc[idx,'half'] = "First 1/2 of Season"
    d.loc[~idx,'half'] = "Second 1/2 of Season"
    return d

def separateIntoDynamicAndSeparate(d):
    dynamic = d[(d.modelType=='dynamic') & (d.prior!=-1)]
    static  = d[(d.modelType=='static') & (d.prior!=-1)]
    return dynamic,static

def computeBy(data,G):
    singleScore = data.groupby(['modelType','prior',"{:s}".format(G)]).apply(meanLogScore).reset_index()
    fiveScore = data.groupby(['modelType','prior',"{:s}".format(G)]).apply(meanLogScore5).reset_index()
    return singleScore, fiveScore

def computeBy2(data,G0,G1):
    singleScore = data.groupby(['modelType','prior',"{:s}".format(G0),"{:s}".format(G1)]).apply(meanLogScore).reset_index()
    fiveScore = data.groupby(['modelType','prior',"{:s}".format(G0),"{:s}".format(G1)]).apply(meanLogScore5).reset_index()
    return singleScore, fiveScore

def computeBy3(data,G0,G1,G2):
    singleScore = data.groupby(['modelType','prior',"{:s}".format(G0),"{:s}".format(G1),"{:s}".format(G2)]).apply(meanLogScore).reset_index()
    fiveScore = data.groupby(['modelType','prior',"{:s}".format(G0),"{:s}".format(G1),"{:s}".format(G2)]).apply(meanLogScore5).reset_index()
    return singleScore, fiveScore

def createData(FSN):
    allLogScores = downloadData(FSN)
    allLogScores = addSeason(allLogScores)
    allLogScores = add1stHalgVs2ndHalf(allLogScores)

    if FSN:
        fldr = './plotData'

    averagedOverAll  = allLogScores.groupby(['modelType','prior']).apply(meanLogScore).reset_index()
    dynamic,static   = separateIntoDynamicAndSeparate(averagedOverAll)
    dynamic.to_parquet('{:s}/dynamic.pq'.format(fldr))
    static.to_parquet('{:s}/static.pq'.format(fldr))
    
if __name__ == "__main__":
    createData(FSN=1)
