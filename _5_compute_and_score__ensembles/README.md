# Score ensemble models

There are 4 different training-prior analyses, with two options for training, dynamic or static, and two options for priors, no prior or prior percent.
All models, component and ensemble, are scored on the ILI data with revisions. Week by week, the most recent ILI data is generated, component models are scored, and then fed to our ensemble models. This means as a season progresses, and epidemic weeks receive updated data, the ensemble trains on more recent data that reflects component models' true performance for predicting week ahead ILI.

We wrote four programs below to runs these scenarios; models without a prior report a prior value of *-1*.

1. computeWeightAndLogScoresForEnsembleForecast\_\_staticModels\_TrueILI_withPrior.py  ${prior}
2. computeWeightAndLogScoresForEnsembleForecast\_\_staticModels\_TrueILI\_noPrior.py
3. computeWeightAndLogScoresForEnsembleForecast\_\_dynamicScores\_withPrior.py ${prior}
4. computeWeightAndLogScoresForEnsembleForecast\_\_dynamicScores\_noPrior.py
