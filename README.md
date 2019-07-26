# adaptively_stacking_ensembles_for_infleunza_forecasting_with_incomplete_data

Running the command `make build` will generate all needed figures and datasets needed for publication.

## Description of Folders

\_0\_mixtureModelAlgorithms ->
Ensemble algorithms for static and adaptive ensembles.

\_1\_downloadRawData ->
Code to download Raw influenza data from the CDC, through Epicast.

\_2\_processRawILIdata ->
Aggregate all raw influenza data into one file.

\_3\_collect\_and\_process\_individual\_forecasts ->
Combine component model forecasts together.

\_4\_score\_component\_model\_forecasts ->
Score component model forecasts

\_5\_compute\_and\_score\_\_ensembles ->
Score ensemble model forecasts

\_6\_TLGs ->
Create tables and figures for publication

\_7\_manuscript ->
Code for generating manuscript

## abstract
  Seasonal influenza infects between 10 and 50 million people in the United States every year, overburdening hospitals during weeks of peak incidence.
  Named by the CDC as an important tool to fight the damaging effects of these epidemics, accurate forecasts of influenza and influenza-like illness (ILI) forewarn public health officials about when, and where, seasonal influenza outbreaks will hit hardest.
   
Multi-model ensemble forecasts---weighted combinations of component models---have shown positive results in forecasting. 
Ensemble forecasts of influenza outbreaks have been static, training on all past ILI data at the beginning of a season, generating a set of optimal weights for each model in the ensemble, and keeping the weights constant.
We propose an adaptive ensemble forecast that (i) changes model weights week-by-week throughout the influenza season, (ii) only needs the current influenza season's data to make predictions, and (iii) by introducing a prior distribution, shrinks weights toward the reference equal weighting approach and adjusts for observed ILI percentages that are subject to future revisions.

We investigate the prior's ability to impact adaptive ensemble performance and, after finding an optimal prior via a cross-validation approach, compare our adaptive ensemble’s performance to equal-weighted and static ensembles.
Applied to forecasts of short-term ILI incidence at the regional and national level in the US, our adaptive model outperforms a na\"ive equal-weighted ensemble, and has similar or better performance to the static ensemble, which requires multiple years of training data.

Adaptive ensembles are able to quickly train and forecast during epidemics, and provide a practical tool to public health officials looking for forecasts that can conform to unique features of a specific season.


## additional data needed

Data needed for this project can be found at the Harvard Dataverse.
 
allFSNLogScores.csv.gz (https://doi.org/10.7910/DVN/YUYFUF) can be downloaded `wget https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/YUYFUF` and placed in the folder \_4\_score\_component\_model\_forecasts/analysisData/

analysisData/allEnsembleScores.csv (https://doi.org/10.7910/DVN/RJE9PT) can be downloaded `wget https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/RJE9PT -O allEnsembleScores.csv` and placed in the folder \_5\_compute\_and\_score\_\_ensembles/analysisData

analysisData/allEnsembleWeights.csv (https://doi.org/10.7910/DVN/A9YZOV) can be downloaded `wget https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/A9YZOV -O allEnsembleWeights.csv` and placed in the folder \_5\_compute\_and\_score\_\_ensembles/analysisData

analysisData_preSeason/allEnsembleScores.csv (https://doi.org/10.7910/DVN/GH3C1U) can be downloaded `wget https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/GH3C1U -O allEnsembleScores.csv` and placed in the folder \_5\_compute\_and\_score\_\_ensembles/analysisData

 \_2\_processRawILIdata/analysisData/allFluData\_\_releaseDate\_location\_EW_lag\_ili\_wili\_year\_week_modelWeek\_calendarEW\_Season.csv (https://doi.org/10.7910/DVN/BNVXN6) can be downloaded `wget https://dataverse.harvard.edu/api/access/datafile/:persistentId?persistentId=doi:10.7910/DVN/BNVXN6/Q56PMZ -O allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW_Season.csv` and placed in the folder \_2\_processRawILIdata/analysisData/

