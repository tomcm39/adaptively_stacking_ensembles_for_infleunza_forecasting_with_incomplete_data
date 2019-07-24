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
    averagedOverAll.to_parquet("{:s}/averagedOverAll.pq".format(fldr))

    averagedOverAll5 = allLogScores.groupby(['modelType','prior']).apply(meanLogScore5).reset_index() 
    averagedOverAll5.to_parquet("{:s}/averagedOverAll5.pq".format(fldr))
    
    dynamic,static   = separateIntoDynamicAndSeparate(averagedOverAll)
    dynamic.to_parquet('{:s}/dynamic.pq'.format(fldr))
    static.to_parquet('{:s}/static.pq'.format(fldr))
    
    dynamic5,static5 = separateIntoDynamicAndSeparate(averagedOverAll5)
    dynamic5.to_parquet('{:s}/dynamic5.pq'.format(fldr))
    static5.to_parquet('{:s}/static5.pq'.format(fldr))
 
    
    averagedBySeason,averagedBySeason5  = computeBy(allLogScores,"season")
    averagedBySeason.to_parquet('{:s}/averagedBySeason.pq'.format(fldr))
    averagedBySeason5.to_parquet('{:s}/averagedBySeason5.pq'.format(fldr))

    dynamicBySeason,staticBySeason = separateIntoDynamicAndSeparate(averagedBySeason)
    dynamicBySeason.to_parquet('{:s}/dynamicBySeason.pq'.format(fldr))
    staticBySeason.to_parquet('{:s}/staticBySeason.pq'.format(fldr))

    dynamicBySeason5,staticBySeason5 = separateIntoDynamicAndSeparate(averagedBySeason5)
    dynamicBySeason5.to_parquet('{:s}/dynamicBySeason5.pq'.format(fldr))
    staticBySeason5.to_parquet('{:s}/staticBySeason5.pq'.format(fldr))
   
 
    averagedByTarget, averagedByTarget5 = computeBy(allLogScores,"target")
    averagedByTarget.to_parquet('{:s}/averagedByTarget.pq'.format(fldr))
    averagedByTarget5.to_parquet('{:s}/averagedByTarget5.pq'.format(fldr))
    
    dynamicByTarget,staticByTarget = separateIntoDynamicAndSeparate(averagedByTarget)
    dynamicByTarget.to_parquet('{:s}/dynamicByTarget.pq'.format(fldr))
    staticByTarget.to_parquet('{:s}/staticByTarget.pq'.format(fldr))
    
    dynamicByTarget5,staticByTarget5 = separateIntoDynamicAndSeparate(averagedByTarget5)
    dynamicByTarget5.to_parquet('{:s}/dynamicByTarget5.pq'.format(fldr))
    staticByTarget5.to_parquet('{:s}/staticByTarget5.pq'.format(fldr))
 

    averagedByTargetSeason, averagedByTargetSeason5 = computeBy2(allLogScores,"target","season")
    averagedByTargetSeason.to_parquet('{:s}/averagedByTargetSeason.pq'.format(fldr))
    averagedByTargetSeason5.to_parquet('{:s}/averagedByTargetSeason5.pq'.format(fldr))
    
    dynamicByTargetSeason,staticByTargetSeason = separateIntoDynamicAndSeparate(averagedByTargetSeason)
    dynamicByTargetSeason.to_parquet('{:s}/dynamicByTargetSeason.pq'.format(fldr))
    staticByTargetSeason.to_parquet('{:s}/staticByTargetSeason.pq'.format(fldr))
    
    dynamicByTargetSeason5,staticByTargetSeason5 = separateIntoDynamicAndSeparate(averagedByTargetSeason5)
    dynamicByTargetSeason5.to_parquet('{:s}/dynamicByTargetSeason5.pq'.format(fldr))
    staticByTargetSeason5.to_parquet('{:s}/staticByTargetSeason5.pq'.format(fldr))

    averagedByTargetSeasonRegion, averagedByTargetSeasonRegion5 = computeBy3(allLogScores,"target","season",'region')
    averagedByTargetSeasonRegion.to_parquet('{:s}/averagedByTargetSeasonRegion.pq'.format(fldr))
    averagedByTargetSeasonRegion5.to_parquet('{:s}/averagedByTargetSeasonRegion5.pq'.format(fldr))
    
    dynamicByTargetSeasonRegion,staticByTargetSeasonRegion = separateIntoDynamicAndSeparate(averagedByTargetSeasonRegion)
    dynamicByTargetSeasonRegion.to_parquet('{:s}/dynamicByTargetSeasonRegion.pq'.format(fldr))
    staticByTargetSeasonRegion.to_parquet('{:s}/staticByTargetSeasonRegion.pq'.format(fldr))
    
    dynamicByTargetSeasonRegion5,staticByTargetSeasonRegion5 = separateIntoDynamicAndSeparate(averagedByTargetSeasonRegion5)
    dynamicByTargetSeasonRegion5.to_parquet('{:s}/dynamicByTargetSeasonRegion5.pq'.format(fldr))
    staticByTargetSeasonRegion5.to_parquet('{:s}/staticByTargetSeasonRegion5.pq'.format(fldr))

if __name__ == "__main__":
    createData(FSN=1)
