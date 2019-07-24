#mcandrew

import numpy as np
from glob import glob
if __name__ == "__main__":
    fout = open('./componentModelForecasts.csv','w')
    for modelFile in glob('../_3_collect_and_process_individual_forecasts/aggregatedComponentForecasts/*.csv.gz'):
        fout.write('model={:s}\n'.format(modelFile))
    fout.close()
