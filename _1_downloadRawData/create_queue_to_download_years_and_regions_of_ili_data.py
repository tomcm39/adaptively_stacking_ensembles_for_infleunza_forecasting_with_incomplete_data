#mcandrew

import argparse
import numpy as np
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--beginYear"  , help="The first year to begin downloading ILI data", nargs='?', type=int, default=2010)
    parser.add_argument("--endYear"    , help="The last year to begin downloading ILI data" , nargs='?', type=int, default=2019)
    parser.add_argument("--regions"    , help="python-style list of HHS region numbers to downlaod (ex. [1,2,3,])", nargs='?', type=str, default=[1,2,3,4,5,6,7,8,9,10])
    parser.add_argument("--nat"        , help="nat=1 downlaods national data, 0 does not", nargs='?', type=int, default=1)

    args = parser.parse_args()

    fout = open('./queueOfYearsAndRegions2download.csv','w')
    
    years = np.arange(args.beginYear,args.endYear+1)
    regions = args.regions
    
    for year in years:
        for region in regions:
            fout.write('year={:d},region={:d}\n'.format(year,region))
    for year in years:
        fout.write('year={:d},region=nat\n'.format(year))
    fout.close()
