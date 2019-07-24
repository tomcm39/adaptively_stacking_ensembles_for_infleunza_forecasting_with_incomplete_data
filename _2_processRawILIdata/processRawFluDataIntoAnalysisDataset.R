#mcandrew;

require(epiforecast)
require(tidyverse)

allFluData <- read.csv('../_1_downloadRawData/data/allFluData_withHeader.csv')
allFluData <- allFluData %>% mutate( year = substr(EW,1,4)) %>% mutate( week = substr(EW,5,6))
                                    
season_modelWeek <- epiforecast::yearWeekToSeasonModelWeekDF(allFluData$year,allFluData$week,40L,3L)
allFluData <- allFluData %>% mutate( modelWeek = season_modelWeek$model.week )

write.csv(allFluData
         ,'./analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek.csv'
	 ,row.names=FALSE
          )
