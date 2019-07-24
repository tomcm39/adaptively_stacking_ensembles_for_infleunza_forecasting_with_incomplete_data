#mcandrew

import os
import sys
import pandas as pd
from glob import glob

def listDirectories():
    return [x for x in glob('separateComponentModelForecasts/*') if os.path.isdir(x)  ]

def extractModelName(path):
    return path.split('/')[-1]

def mapModelName2ModelID():
    modelLabels = pd.read_csv('./separateComponentModelForecasts/model-id-map.csv')
    return  modelLabels.set_index('model-dir').to_dict()['model-id'] 

def pickEWandYRFromFileName(fileName):
    EW,YR = fileName.split('/')[-1].split('-')[:2]
    EW = int(EW[2:])
    YR = int(YR)
    return EW,YR

def fromYearEW2season(yr,ew):
    if 40<=ew<=53:
        return '{:04d}/{:04d}'.format(yr,yr+1)
    return '{:04d}/{:04d}'.format(yr-1,yr)

def addHeader(fout):
    fout.write('model,year,EW,EWNum,season,region,target,bin0,bin1,prob\n')

if __name__ == "__main__":

    fromFolder2ModelId = mapModelName2ModelID()
    
    dirs = listDirectories()
    N = len(dirs)
    for n,model in enumerate(dirs):
        modelName = extractModelName(model)
        sys.stdout.write("\033[K")
        sys.stdout.write('\r{:s}-({:d}/{:d})\r'.format(modelName,n+1,N))
        sys.stdout.flush()
        
        fout = open('./aggregatedComponentForecasts/{:s}Forecasts.csv'.format(modelName),'w')
        addHeader(fout)
        
        for individualFile in glob(model+'/*'):
            if 'meta' in individualFile:
                continue

            EW,YR = pickEWandYRFromFileName(individualFile)
            EWNum = int('{:04d}{:02d}'.format(YR,EW))
            season = fromYearEW2season(YR,EW)

            f = open(individualFile)
            next(f)
            for line in f:
                location,targetType,targetData,timeFrame,bin_start_incl,bin_end_notincl,prob = line.replace('"','').strip().split(',')

                if targetData == 'Point':
                    continue

                try:
                    prob = float(prob)
                except ValueError:
                    continue
                
                currentModel = fromFolder2ModelId[modelName]
                fout.write('{:s},{:d},{:d},{:d},{:s},{:s},{:s},{:s},{:s},{:f}\n'.format(currentModel,YR,EW,EWNum,season,location,targetType,bin_start_incl,bin_end_notincl,prob))
        fout.close()
