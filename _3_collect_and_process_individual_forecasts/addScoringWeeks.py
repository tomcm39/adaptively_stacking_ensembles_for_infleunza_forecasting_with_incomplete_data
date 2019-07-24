#mcandrew

import sys
import numpy as np
import pandas as pd
from glob import glob

def computeScoringWeekForSeasonTargets(forecastData, iliData):
    finalWeekForEachSeason = pd.DataFrame(iliData.groupby('Season').apply(lambda x: pd.unique(x['EW'])[-1])).reset_index()
    finalWeekForEachSeason.rename(columns={0:'finalWeek', 'Season':'season'},inplace=True)

    forecastData = forecastData.merge(finalWeekForEachSeason, on = ['season'] )

    peaks = ~forecastData.target.str.contains('ahead')
    forecastData.loc[peaks,'seasonal_scoringWeek'] = forecastData.finalWeek[peaks]
    forecastData.drop(['finalWeek'],1,inplace=True)
    return forecastData

def generateScoringWeekDataFrame():
    ewTargetScoringWeek={'EWNum':[],'target':[],'weekAhead_scoringWeek':[]}
    for ew0,ew1,ew2,ew3,ew4 in zip(allEWS,allEWS[1:],allEWS[2:],allEWS[3:],allEWS[4:]):
        for (n,scoringWeek) in enumerate([ew1,ew2,ew3,ew4]):
            ewTargetScoringWeek['EWNum'].append(ew0)
            ewTargetScoringWeek['target'].append('{:d} wk ahead'.format(n+1))
            ewTargetScoringWeek['weekAhead_scoringWeek'].append(scoringWeek)
    ewTargetScoringWeek = pd.DataFrame(ewTargetScoringWeek)
    return ewTargetScoringWeek

def computeScoringWeekForWeekAheadTargets(forecastData,ewTargetScoringWeek):
    return forecastData.merge(ewTargetScoringWeek,on=['EWNum','target'],how='left')

def createScoringWeekVar(forecastData):
    forecastData['scoringWeek'] = forecastData['seasonal_scoringWeek'].fillna(0) + forecastData['weekAhead_scoringWeek'].fillna(0)
    return forecastData.drop(['seasonal_scoringWeek','weekAhead_scoringWeek'],1)

if __name__ == "__main__":

    iliData = pd.read_csv('../_2_processRawILIdata/analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW_Season.csv')
    allEWS  = [ int(x) for x in pd.read_csv('./allPossibleEpidemicWeeks.csv',header=None).values]
    allEWS  = allEWS + [201821,201822,201823,201824,201825,201826,201827,201828]

    ewTargetScoringWeek = generateScoringWeekDataFrame()
    models = glob('./aggregatedComponentForecasts/*.csv')
    N = len(models)
    for n,model in enumerate(models):
        sys.stdout.write("\033[K")
        sys.stdout.write('\r{:s} - {:d}/{:d}\r'.format(model,n+1,N))
        sys.stdout.flush()

        forecastData = pd.read_csv(model,low_memory=False)
        if 'scoringWeek' in forecastData:
            print('scoring week already generate for {:s}'.format(model))
            
        forecastData = computeScoringWeekForSeasonTargets(forecastData,iliData)
        forecastData = computeScoringWeekForWeekAheadTargets(forecastData,ewTargetScoringWeek)
        forecastData = createScoringWeekVar(forecastData)
        forecastData.to_csv(model,index=False)
