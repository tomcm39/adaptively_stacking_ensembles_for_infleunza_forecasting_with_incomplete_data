#mcandrew

import sys
import numpy as np
from delphi_epidata import Epidata

def EpiCallForLag(year,week,region):
    if region == 'nat':
        return Epidata.fluview(['nat'], ['{:04d}{:02d}'.format(year,week)])
    region = int(region)
    return Epidata.fluview(['HHS{:d}'.format(region)], ['{:04d}{:02d}'.format(year,week)])

def EpiCallForData(year,week,region,lag):
    if region == 'nat':
        fluData = Epidata.fluview(regions = ['nat']
                                 ,epiweeks = ['{:04d}{:02d}'.format(year,week)]
                                 ,lag = lag
                                  )
    else:
        region = int(region)
        fluData = Epidata.fluview(regions = ['HHS{:d}'.format(region)]
                                 ,epiweeks = ['{:04d}{:02d}'.format(year,week)]
                                 ,lag = lag
                                  )
    return fluData

def downloadYearlyData(year,weeks,region):
    if region == 'nat':
        fout = open('./data/fluData_Nat__year{:d}_releaseDate_epiweek_ili_wili.csv'.format(year),'w')
    else:
        regionNum = int(region)
        fout = open('./data/fluData_HHS{:d}_year{:d}__releaseDate_epiweek_ili_wili.csv'.format(regionNum,year),'w')
    foutError = open('./data/fluData__year{:04d}.err'.format(year),'w')

    for week in weeks:
        #find maximum lag
        fluData = EpiCallForLag(year,week,region)
        maximumLag = fluData['epidata'][0]['lag']

        for lag in range(maximumLag+1):
            sys.stdout.write('\r{:04d}-{:04d}-{:04d}\r'.format(year,week,lag))
            sys.stdout.flush()
            fluData = EpiCallForData(year,week,region,lag)

            if fluData['result'] == -2:
                continue

            try:
                epiData = fluData['epidata'][0]
            except:
                foutError.write('{:04d},{:02d}'.format(year,week))
                continue
                
            epiweek     = epiData['epiweek']
            releaseDate = epiData['release_date']
            ili         = epiData['ili']
            wili        = epiData['wili']

            if region == 'nat':
                fout.write('{:s},Nat,{:06d},{:04d},{:.5f},{:.5f}\n'.format(releaseDate,epiweek,lag,ili,wili))
            else:
                regionNum = int(region)
                fout.write('{:s},HHS{:d},{:06d},{:04d},{:.5f},{:.5f}\n'.format(releaseDate,regionNum,epiweek,lag,ili,wili))
            fout.flush()
    fout.close()
if __name__ == "__main__":

    year   = int(sys.argv[1])
    region = sys.argv[2]
    
    weeks = np.arange(1,53+1)
    downloadYearlyData(year,weeks,region)
