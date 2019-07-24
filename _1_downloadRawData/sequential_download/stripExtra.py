#mcandrew

import sys

if __name__ == "__main__":
    string = ''.join(sys.argv[1:])
    year,region =string.split(',') 
    year = year.replace('year=','')
    region = region.replace('region=','')
    print("{:s} {:s}".format(year,region))
