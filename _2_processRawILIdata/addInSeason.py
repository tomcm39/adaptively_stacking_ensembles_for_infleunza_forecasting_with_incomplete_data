#mcandrew

import sys
import numpy as np
import pandas as pd
import pymmwr

def importILIDataAndAddSeason():
    data = pd.read_csv('./analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW.csv')
    data['SeasonUp']   = data.year.astype(str)+'/' + (data.year+1).astype(str) 
    data['SeasonDown'] = (data.year-1).astype(str) + '/' + data.year.astype(str) 

    data.loc[(data.week >= 40) & (data.week <=53),'Season']     = data.loc[(data.week >= 40) & (data.week <=53),'SeasonUp']
    data.loc[~((data.week >= 40) & (data.week <=53)),'Season'] = data.loc[~((data.week >= 40) & (data.week <=53)),'SeasonDown']
    data.drop(['SeasonUp','SeasonDown'],1,inplace=True)
 
    return data

if __name__ == "__main__":

    data = importILIDataAndAddSeason()
    data.to_csv('./analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW_Season.csv',index=False)
