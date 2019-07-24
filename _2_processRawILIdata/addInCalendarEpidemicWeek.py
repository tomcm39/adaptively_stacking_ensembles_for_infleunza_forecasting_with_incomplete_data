#mcandrew

import sys
import numpy as np
import pandas as pd
import pymmwr

def importILIDataAndAddCalendarEW():
    data = pd.read_csv('./analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek.csv')
    data['releaseDate'] = pd.to_datetime(data.releaseDate, format = '%Y-%m-%d').dt.date
    
    def fromReleaseDate2calendarEpiWeek(row):
        calendarEW  = pymmwr.date_to_epiweek(row.releaseDate)
        calendarEW  = "{:04d}{:02d}".format(calendarEW.year,calendarEW.week) 
        row['calendarEW'] = calendarEW
        return row
    data = data.apply(fromReleaseDate2calendarEpiWeek,1) 
    return data

if __name__ == "__main__":

    data = importILIDataAndAddCalendarEW()
    data.to_csv('./analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW.csv',index=False)
