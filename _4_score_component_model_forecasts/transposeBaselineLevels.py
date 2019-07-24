#mcandrew

import sys
import pandas as pd

def processFile(d):
    d = d.rename(columns = {'Unnamed: 0':'location'})
    d = pd.melt(d,id_vars=['location'])
    d = d.rename(columns={'variable':'year'})

    d['year']     = d['year'].str.replace('[/].*','')
    d['location'] = d['location'].str.replace('National', 'US National')
    d['location'] = d['location'].str.replace('Region', 'HHS Region ')
    return d

if __name__ == "__main__":

    d = pd.read_csv(sys.stdin)
    d = processFile(d)
    d.to_csv('./wiliBaselineDataByRegionAndYear/wILI_Baseline.csv',index=False)
        
