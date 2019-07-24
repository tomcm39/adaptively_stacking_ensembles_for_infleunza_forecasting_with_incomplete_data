Download raw ILI data from Delphi Epicast
==========

## Brief Description
We download all raw ILI data---including all revisions---using Delphi Epicast's EpiData python api, available at [Delphi Epidata](https://github.com/cmu-delphi/delphi-epidata).
Users can download the Delphi tools for python with the command `pip install delphi-epidata`.

All Influenza-like illness data is collected through the EpiData system.
Users that want to download raw data can do so two ways: (i) sequentially or (ii) using a cluster computer.
For sequential download to your local machine, run `make downloadDataOnLocal`. For downloading on a cluster (only supporting a BFS scheduler) `make downloadDataOnCluster`.
After downloading all the Epicast influenza data, running `make` will aggregate the separate infleunza data into a single file called *./data/allFluData_withHeader.csv*
The final aggregated influenza-like illness dataset, every row corresponds to a ILI data (ili and wili) the CDC released ILI data (releaseDate) corresponding to a specific HHS region's (region) epidemic week (EW). For example, the row `2010-01-15,HHS4,201001,0000,2.2,1.9` means on 2010-01-15, the CDC released ILI data for HHS region 4 for epidemic week 2010-01. The ILI values on that date were 2.2 and 1.9 weighted ILI. 
