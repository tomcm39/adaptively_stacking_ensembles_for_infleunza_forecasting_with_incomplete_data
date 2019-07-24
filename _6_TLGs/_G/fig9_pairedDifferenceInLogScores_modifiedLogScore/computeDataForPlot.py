#mcandrew

import sys
import numpy as np
import pandas as pd


def downloadData():
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

if __name__ == "__main__":

    allLogScores = downloadData()
    allLogScores = addSeason(allLogScores)
    allLogScores = add1stHalgVs2ndHalf(allLogScores)

    dynamic, static, equal = allLogScores[allLogScores.modelType=='dynamic'], allLogScores[allLogScores.modelType=='static'], allLogScores[allLogScores.modelType=='equal']
    dynamic = dynamic[dynamic.prior==0.08]
    static  = static[static.prior==0.0]
    
    dynamic.rename(columns = {'logScore5':'logScoreDynamic'},inplace=True)
    static.rename(columns = {'logScore5':'logScoreStatic'},inplace=True)
    equal.rename(columns = {'logScore5':'logScoreEqual'},inplace=True)

    logDifs = static.merge(dynamic, on = ['region','target','EWNum','season'])
    logDifs = logDifs.merge(equal, on = ['region','target','EWNum','season'])

    logDifs['difLogScore__dynStat'] = logDifs.logScoreDynamic - logDifs.logScoreStatic
    logDifs['difLogScore__dynEW'] = logDifs.logScoreDynamic - logDifs.logScoreEqual
    logDifs['difLogScore__StatEW'] = logDifs.logScoreStatic - logDifs.logScoreEqual

    
    logDifs['relDifLogScore__dynStat'] = logDifs.logScoreDynamic / logDifs.logScoreStatic- 1.0
    logDifs['relDifLogScore__dynEW']   = logDifs.logScoreDynamic / logDifs.logScoreEqual - 1.0
    logDifs['relDifLogScore__StatEW']  = logDifs.logScoreStatic  / logDifs.logScoreEqual - 1.0
   
    logDifs.to_parquet('./plotData/logDifs5.pq')
