#mcandrew

import sys
import numpy as np
import pandas as pd
from glob import glob

import dask
from dask import dataframe as ddf


def importAndModifyEmpiricalFluData():
    iliData = pd.read_csv('../_2_processRawILIdata/analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW_Season.csv')
    iliData = iliData[~((iliData.week <40) & (iliData.year==2010))]
    iliData = iliData[~((iliData.week >28) & (iliData.year==2018))]
    return iliData

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

def grabAllEpiWeeks():
    allEWS = pd.read_csv('../_3_collect_and_process_individual_forecasts/allPossibleEpidemicWeeks.csv',header=None)
    allEWS = sorted(list(allEWS[0]))
    return allEWS

def subset2MostRecentData(iliData, calendarEpiWeek):
    availableData  = iliData.loc[iliData.calendarEW <= calendarEpiWeek]
    mostRecentData = availableData.groupby(['region','EW']).apply(lambda d: d.sort_values('calendarEW').iloc[-1])
    mostRecentData.set_index(np.arange(0,mostRecentData.shape[0]), inplace=True)
    return mostRecentData

def computeScoringWeekForSeasonTargets(seasonalData, data):
    finalWeekForEachSeason = pd.DataFrame(data.groupby('Season').apply(lambda x: pd.unique(x['EW'])[-1])).reset_index()

    seasonalData = seasonalData.merge(finalWeekForEachSeason, on = ['season'] )

    peaks = ~seasonalData.target.str.contains('ahead')
    seasonalData.loc[peaks,'scoringWeek'] = seasonalData.finalWeek[peaks]
    seasonalData.drop(['finalWeek'],1,inplace=True)
    return seasonalData

def computeOnset(d):
    baselinesByRegionAndSeason = pd.read_csv('./wiliBaselineDataByRegionAndYear//wILI_Baseline.csv')

    def fromLoc2Reg(row):
        import re
        if 'Region' in row:
            num = int(re.search('[0-9]+',row).group(0))
            return 'HHS{:d}'.format(num)
        return 'Nat'
    baselinesByRegionAndSeason['region'] = baselinesByRegionAndSeason.location.apply(fromLoc2Reg)

    season,region = d.name

    baselinesByRegionAndSeason = baselinesByRegionAndSeason[baselinesByRegionAndSeason['region']==region]
    d = d.merge(baselinesByRegionAndSeason, on = ['year'] )
    d['consec'] = np.arange(0,d.shape[0])

    aboveBaseline = d[d.wili> d.value]
    if aboveBaseline.shape[0]==0:
        return pd.Series({"Season onset":-1})

    oldModelWeek = aboveBaseline.iloc[0]['consec']
    onset = aboveBaseline.iloc[0]['week']
    inArow=0
    for (index,row) in aboveBaseline.iloc[1:].iterrows():
        modelWeek = row['consec']
        epiWeek   = row['week']
        if modelWeek - oldModelWeek > 1:
            onset = epiWeek
        else:
            inArow+=1
        if inArow==3:
            return pd.Series({"Season onset":onset})
        oldModelWeek = modelWeek
    return pd.Series({"Season onset":-1})


def findSeasonPeakWeeks(d):
    d['wili'] = np.round(d['wili'],1)
    peakWili = d.sort_values('wili').iloc[-1]['wili']

    peakWeeks = pd.DataFrame(d[d.wili==peakWili]['week'])
    peakWeeks['Season peak week number'] = np.arange(0,peakWeeks.shape[0])
    peakWeeks.rename(columns = {'week':'Season peak week'},inplace=True)
    return peakWeeks

def findSeasonPeakWili(d):
    d['wili'] = np.round(d['wili'],1)
    peakWili = d.sort_values('wili').iloc[-1]['wili']
    return pd.Series({"Season peak percentage":peakWili})

def addInEndSeasonData(scoringData):
    _1stHalf = list(np.arange(40.,53))
    _2ndHalf = list(np.arange(0.,25))
    fromEW2SortingWeek = { x:n for (n,x) in enumerate(_1stHalf+_2ndHalf)}

    scoringData = scoringData[scoringData.bin0!=-999.0]
    scoringData['sortingWeek'] = 0

    peaks = scoringData.target.str.contains('Season onset|Season peak week')
    for n,sortingWeek in fromEW2SortingWeek.items():
        scoringData.loc[peaks & (scoringData.bin0==n),'sortingWeek'] = sortingWeek
    scoringData = scoringData.sort_values(['model','target','region','EWNum','sortingWeek'])

    scoringData.rename(columns = {'season':'Season'},inplace=True)
    scoringData = scoringData.merge(seasonsData
                                    ,left_on = ['Season','region']
                                    ,right_on= ['Season','region']
    )
    return scoringData

def computeFinalWeekForEachSeason(mostRecentIliData):
    finalWeekForEachSeason = pd.DataFrame(mostRecentIliData.groupby('Season').apply(lambda x: pd.unique(x['EW'])[-1])).reset_index()
    finalWeekForEachSeason.rename(columns = {0:'finalWeek'},inplace=True)
    return finalWeekForEachSeason


#@profile
def computeLogScoreWithWindow(d,window,truth):
    nRows = d.shape[0]
    peaks = d['Season peak week'].unique()
    d = d[ d['Season peak week number']==0 ]
    #d = d.drop_duplicates(['bin0'])
    
    if truth == 'Season onset':
        try:
            targetRows = [int(np.where(d['bin0'] == d["{:s}".format(truth)])[-1])]
        except TypeError:
            return -999
    elif truth  == "Season peak week":
        try:
            targetRows = []
            for week in peaks:
                targetRows.append(int(np.where(d['bin0'] == week)[-1]))
        except TypeError:
            return -999
    else:
        targetRows = [int(np.where((d['bin0'] <= d["{:s}".format(truth)]) & (d['bin1'] > d["{:s}".format(truth)]))[-1])]
    allTargetRows = targetRows.copy()
    
    for centerRow in targetRows:
        for e in np.arange(-window,window+1,1):
            row = centerRow+e
            row = max(0,row)
            row = min(nRows-1,row)
            if row not in allTargetRows:
                allTargetRows.append(row)
    return np.log(sum(d.iloc[allTargetRows].prob))

def keepPeaksPastFinalWeek(logScores, finalWeekForEachSeason, calendarEpiWeek):
    L = logScores.merge(finalWeekForEachSeason, on = 'Season')
    return L[(L.target.str.contains('ahead')) | (L.finalWeek < L.calendarEW)]


def buildSeasonOnsetPeakAndPeakPct(mostRecentIliData):
    seasonOnsets        = pd.DataFrame(mostRecentIliData.groupby(['Season','region']).apply(computeOnset))
    seasonPeakPercents  = pd.DataFrame(mostRecentIliData.groupby(['Season','region']).apply(findSeasonPeakWili))
    seasonPeakWeeks     = pd.DataFrame(mostRecentIliData.groupby(['Season','region']).apply(findSeasonPeakWeeks)).reset_index(['Season','region']).set_index(['Season','region'])

    seasonsData  = seasonOnsets.merge(seasonPeakPercents,left_index=True, right_index=True)
    seasonsData  = seasonsData.merge(seasonPeakWeeks,left_index=True, right_index=True).reset_index()
    return seasonsData

def grabModelName(modelFile):
    return modelFile.split('/')[-1].replace('.csv','')

def fromYearEW2Season(YR,EW):
    if EW <40:
        return '{:d}/{:d}'.format(YR-1,YR)
    return '{:d}/{:d}'.format(YR,YR+1)

if __name__ == "__main__":
   
    iliData = importAndModifyEmpiricalFluData()
    finalWeekForEachSeason = computeFinalWeekForEachSeason(iliData)

    allLogScores = pd.DataFrame()

    modelFile = sys.argv[1] 
    forecastData = downloadSingleComponentModel(modelFile)   

    allEWS =      grabAllEpiWeeks()
    allCalendarWeeks = sorted(iliData.calendarEW.unique())
    N = len(allCalendarWeeks)
    for n,calendarEpiWeek in enumerate(allCalendarWeeks[1:]): # no data during the very first calendar week
        sys.stdout.write('\rCalendar Week: {:d}-({:d}/{:d})\r'.format(calendarEpiWeek,n,N))
        sys.stdout.flush()

        mostRecentIliData = subset2MostRecentData(iliData,calendarEpiWeek)
        scoringData    = forecastData.merge(mostRecentIliData[['region','EW','wili']]
                                        , left_on =['region','scoringWeek']
                                        , right_on=['region','EW']
        )
        scoringData['bin0'] = scoringData.bin0.astype(np.float64)
        scoringData['bin1'] = scoringData.bin1.astype(np.float64)

        seasonsData = buildSeasonOnsetPeakAndPeakPct(mostRecentIliData)
        scoringData = addInEndSeasonData(scoringData)

        keepVars = ['model','Season','EWNum','scoringWeek','region','target','bin0','bin1','prob','wili','Season onset', 'Season peak week', 'Season peak week number', 'Season peak percentage']
        availScoringData = scoringData[keepVars]

        def roundPercentages2FirstDecimal(d,truth):
            d['{:s}'.format(truth)] = np.round(d['{:s}'.format(truth)],1)
            return d
        availScoringData = roundPercentages2FirstDecimal(availScoringData,'wili')

        def computeLogScores(d):
            region,target,model,Season,EWNum = d.name
            if target in {'1 wk ahead','2 wk ahead','3 wk ahead','4 wk ahead','Season peak percentage'}:
                logScore = computeLogScoreWithWindow(d,window=5,truth="wili")
            else:
                logScore = computeLogScoreWithWindow(d,window=1,truth=target)
            return logScore

        logScores = availScoringData.groupby(['region','target','model','Season','EWNum']).apply(computeLogScores).reset_index(name = 'logScore')
        logScores['calendarEW'] = calendarEpiWeek
        logScores['logScore'] = logScores['logScore'].clip(-999,0)
        logScores = keepPeaksPastFinalWeek(logScores, finalWeekForEachSeason, calendarEpiWeek)

        allLogScores = allLogScores.append(logScores)

    modelName = grabModelName(modelFile)
    allLogScores.to_csv('./analysisData/scoringData_{:s}.csv'.format(modelName))
