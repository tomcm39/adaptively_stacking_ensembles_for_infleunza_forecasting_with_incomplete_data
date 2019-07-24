#mcandrew

import sys
import numpy as np
import pandas as pd
from glob import glob

sys.path.append('../_0_mixtureModelAlgorithms/')
from deviMM import *
from deEM import *

def subsetColumns2Models(logScores):
    return logScores.drop(['Unnamed: 0','region','season','target','EWNum','calendarEW','availWeek'],1)
    
def downloadLogScoreData(FSN):
    if FSN:
        return pd.read_csv('../_4_score_component_model_forecasts/analysisData/allFSNLogScores.csv.gz')
    return pd.read_csv('../_4_score_component_model_forecasts/analysisData/allCDCLogScores.csv.gz')

def computeSeason(logScores):
    logScores['year']   = logScores.EWNum.astype(str).str.slice(0,4).astype(int)
    logScores['week']   = logScores.EWNum.astype(str).str.slice(4,6).astype(int)

    logScores['SeasonUp']   = logScores.year.astype(str)+'/' + (logScores.year+1).astype(str) 
    logScores['SeasonDown'] = (logScores.year-1).astype(str) + '/' + logScores.year.astype(str) 

    logScores.loc[(logScores.week >= 40) & (logScores.week <=53),'season']     = logScores.loc[(logScores.week >= 40) & (logScores.week <=53),'SeasonUp']
    logScores.loc[~((logScores.week >= 40) & (logScores.week <=53)),'season'] = logScores.loc[~((logScores.week >= 40) & (logScores.week <=53)),'SeasonDown']

    logScores = logScores.drop(['SeasonUp','SeasonDown','year','week'],1)
    return logScores

def fromEW2Season(EW):
    year,week = int(str(EW)[:4]),int(str(EW)[4:])
    if 40<= week <=53:
        return "{:d}/{:d}".format(year,year+1)
    return "{:d}/{:d}".format(year-1,year)

def subset2MostRecentSeason(logScores,calendarEW):
    mostRecentSeason = fromEW2Season(calendarEW) 
    return logScores[logScores.season == mostRecentSeason]

def removeSeasonTargets(d):
    return d[~d.target.str.contains(('Season onset|Season peak percentage|Season peak week'))]
    
def computeEWEnsembleWeights(trainingData):
    modelsOnly = subsetColumns2Models(trainingData) 
    modelNames = modelsOnly.columns 
    
    modelPis = {name:0. for name in modelNames}

    modelsOnlyNoNA = modelsOnly.dropna(1)
    modelNamesNoNA = modelsOnlyNoNA.columns
    
    nObs,numModels = modelsOnlyNoNA.shape
    if nObs == 0:
        modelPis = pd.Series({modelName:1./numModels for modelName in modelNames})
        modelPis['N'] = nObs
    else:
        for model in modelNamesNoNA:
            modelPis[model] = 1./numModels
        modelPis['N'] = nObs
    return pd.Series(modelPis)

def computeAvailWeek(logScores):
    import re

    EWNums = sorted(logScores.EWNum.unique())
    wkAheads = {'EWNum':[],'1 wk ahead':[],'2 wk ahead':[],'3 wk ahead':[],'4 wk ahead':[]}
    for wk,wk1,wk2,wk3,wk4 in zip(EWNums,EWNums[1:],EWNums[2:],EWNums[3:],EWNums[4:]):
        wkAheads['EWNum'].append(wk)
        wkAheads['1 wk ahead'].append(wk1)
        wkAheads['2 wk ahead'].append(wk2)
        wkAheads['3 wk ahead'].append(wk3)
        wkAheads['4 wk ahead'].append(wk4)
    wkAheads = pd.DataFrame(wkAheads)
    wkAheads = wkAheads.melt('EWNum') 
    wkAheads = wkAheads.rename(columns = {'variable':'target','value':'availWeek'})

    logScores = logScores.merge(wkAheads,on=['EWNum','target'])
    return logScores


def downloadSingleComponentModel(modelFile):
    forecastData = pd.read_csv( modelFile 
                                ,dtype = {'model':np.str
                                          ,'year':np.int32
                                          ,'EW':np.int32
                                          ,'EWNum':np.int32
                                          ,'season':np.str
                                          ,'region':np.str
                                          ,'target':np.str
                                          ,'bin0':'object'
                                          ,'bin1':'object'
                                          ,'prob':np.float64
                                          ,'scoringWeek':np.float64}
    )
    return forecastData

def subset2SpecificWeek(data,EW):
    return data[data.EWNum==EW]

def subset2MostRecentData(iliData, calendarEpiWeek):
    availableData  = iliData.loc[iliData.calendarEW <= calendarEpiWeek]
    mostRecentData = availableData.groupby(['region','EW']).apply(lambda d: d.sort_values('calendarEW').iloc[-1])
    mostRecentData.set_index(np.arange(0,mostRecentData.shape[0]), inplace=True)
    return mostRecentData

def computeFinalWeekForEachSeason(mostRecentIliData):
    finalWeekForEachSeason = pd.DataFrame(mostRecentIliData.groupby('Season').apply(lambda x: pd.unique(x['EW'])[-1])).reset_index()
    finalWeekForEachSeason.rename(columns = {0:'finalWeek'},inplace=True)
    return finalWeekForEachSeason

def fromEW2Season(EW):
    EWstr = str(EW)
    year,ew = int(EWstr[:4]), int(EWstr[4:])
    if 40 <= ew <= 53:
        return '{:d}/{:d}'.format(year,year+1)
    return '{:d}/{:d}'.format(year-1,year) 

def importAndModifyEmpiricalFluData():
    iliData = pd.read_csv('../_2_processRawILIdata/analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW_Season.csv')
    iliData = iliData[~((iliData.week <40) & (iliData.year==2010))]
    iliData = iliData[~((iliData.week >28) & (iliData.year==2018))]
    return iliData

def defineEvalWeeks(logScores):
    return sorted(logScores[logScores.calendarEW==201902].availWeek.unique())
        
def computeFinalWeekPerSeason(logScores):
    return logScores.groupby('season').apply(lambda x: x.EWNum.max() ).to_dict()

def combineAllComponentForecastModels():
    allForecastData = pd.DataFrame()
    for modelFile in glob('../_3_collect_and_process_individual_forecasts/aggregatedComponentForecasts/*'):
        sys.stdout.write('\r{:100s}\r'.format(modelFile))
        sys.stdout.flush()
        forecastData = downloadSingleComponentModel(modelFile)
        forecastData = forecastData.drop(columns = ['year','EW','season'])
        forecastData = forecastData[forecastData.target.str.contains('wk ahead')]
        forecastData['bin0'] = forecastData['bin0'].astype(float)
        forecastData['bin1'] = forecastData['bin1'].astype(float)
        allForecastData = allForecastData.append(forecastData)
    return allForecastData

def computeWeightsFromTrainingData(trainingData, algorithm):
    weightDataForForecasting = algorithm(trainingData)
    weightDataForForecasting = weightDataForForecasting.to_frame().reset_index().rename(columns={'index':'model',0:'weight'})
    weightDataForForecasting = weightDataForForecasting[weightDataForForecasting.model!='N']

    weightDataForAppending = pd.pivot_table(weightDataForForecasting,columns='model')
    weightDataForAppending['week']  = week
    weightDataForAppending['prior'] = -2
    return weightDataForForecasting, weightDataForAppending

def computeLogScore(d,window):
    d['binNumber'] = np.arange(1,d.shape[0]+1)
    correctBin = int(d.loc[ d.wili==d.bin0 ,'binNumber'])

    first = max(correctBin-(window+1),0)
    last  = min(correctBin+window, d.shape[0]-1)
    d=d.iloc[ np.arange(first,last),:]
    logScore = np.log(np.sum(d.prob))
    return pd.Series({'logScore':logScore})

def computeMostRecentSeason(d):
    return sorted(d.season.unique())[-1]

def compute1WindowAnd5WindowLogScores(d):
    _1LogScore = d.groupby(['region','target','EWNum']).apply(lambda d: computeLogScore(d,0)).reset_index()
    _5LogScore = d.groupby(['region','target','EWNum']).apply(lambda d: computeLogScore(d,5)).reset_index()
    _5LogScore = _5LogScore.rename(columns={'logScore':'logScore5'})
    
    logScores = _1LogScore.merge(_5LogScore, on=['region','target','EWNum'])
    logScores = logScores.replace(-np.inf,-10.)
    return logScores

if __name__ == "__main__":

    logScores = downloadLogScoreData(FSN=1)
    logScores = computeSeason(logScores)   
    logScores = removeSeasonTargets(logScores) # adaptive models will never have access to weights
    logScores = logScores[logScores.target.str.contains('wk ahead')]

    logScores = computeAvailWeek(logScores)

    fromSeason2FinalWeek = { '2010/2011':201128
                            ,'2011/2012':201228
                            ,'2012/2013':201328
                            ,'2013/2014':201428
                            ,'2014/2015':201528
                            ,'2015/2016':201628
                            ,'2016/2017':201728
                            ,'2017/2018':201828
    }

    allForecastData = combineAllComponentForecastModels()
       
    iliData = importAndModifyEmpiricalFluData()
    finalWeekForEachSeason = computeFinalWeekForEachSeason(iliData)

    allLogScores = pd.DataFrame()
    allWtData = pd.DataFrame()
    evalWeeks = defineEvalWeeks(logScores) # only look at one season
    carryOverSeason  = '2010/2011'

    for week in evalWeeks:
        sys.stdout.write('\r{:d}\r'.format(week))
        sys.stdout.flush()

        logScoresForSpecificCalendarWeek = logScores[logScores.calendarEW==week]
        if logScoresForSpecificCalendarWeek.shape[0]==0:
            continue

        if fromEW2Season(week) == '2010/2011': #skip this season so we can train
            continue
       
        print(week)
        mostRecentSeason =  fromEW2Season(week)
        logScoresForSpecificCalendarWeek = logScoresForSpecificCalendarWeek[logScoresForSpecificCalendarWeek.season==mostRecentSeason]
        trainingData = logScoresForSpecificCalendarWeek[logScoresForSpecificCalendarWeek.availWeek<=week]
            
        N,cols = trainingData.shape

        weightDataForForecasting, weightDataForAppending = computeWeightsFromTrainingData(trainingData,  algorithm = computeEWEnsembleWeights)
        
        allWtData = allWtData.append(weightDataForAppending)

        # forecast
        componentForcasts  = subset2SpecificWeek(allForecastData,EW=week)
        forecastPlusWeight = componentForcasts.merge(weightDataForForecasting,on='model')
        forecastPlusWeight['ensembleProb'] = forecastPlusWeight['weight']*forecastPlusWeight['prob']
        
        ensembleForecast = forecastPlusWeight.groupby(['region','target','EWNum','bin0','bin1']).apply(lambda x: np.sum(x['ensembleProb']))
        ensembleForecast = ensembleForecast.reset_index()
        ensembleForecast = ensembleForecast.rename(columns = {0:'prob'})

        ensembleForecast['scoringWeek'] = ensembleForecast.target.str.replace('wk ahead','').astype(int) + ensembleForecast.EWNum 
        ensembleForecast.bin0 = ensembleForecast.bin0.astype(np.float64)
        ensembleForecast.bin1 = ensembleForecast.bin1.astype(np.float64)

        mostRecentIliData = subset2MostRecentData(iliData,calendarEpiWeek = fromSeason2FinalWeek[mostRecentSeason])
        ensembleForecast = ensembleForecast.merge( mostRecentIliData, left_on = ['region','scoringWeek'], right_on=['region','EW'] )
        ensembleForecast['wili'] = np.round(ensembleForecast.wili,1)

        if ensembleForecast.shape[0]==0:
            continue

        #logScores
        _1And5WindowLogScores = compute1WindowAnd5WindowLogScores(ensembleForecast)
        allLogScores = allLogScores.append(_1And5WindowLogScores)

    priorPercent=-2
    allWtData.to_csv('./analysisData/ensembleWeights__equalweight.csv'.format(priorPercent))
    allLogScores.to_csv('./analysisData/ensembleScores__equalscore.csv'.format(priorPercent))
