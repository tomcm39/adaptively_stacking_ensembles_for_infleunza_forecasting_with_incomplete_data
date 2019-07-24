#mcandrew

import sys
import pickle
import numpy as np
import pandas as pd

import seaborn as sns

import matplotlib as mpl
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.ticker import FormatStrFormatter

from glob import glob
import re

def separateIntoDynamicAndSeparate(d):
    dynamic = d[(d.modelType=='dynamic') & (d.prior!=-1)]
    static  = d[(d.modelType=='static') & (d.prior!=-1)]
    return dynamic,static

from matplotlib.font_manager import FontProperties
import matplotlib.ticker as ticker

font0 = FontProperties()
boldFont = font0.copy()

def ticksIn(ax,l=3.):
    ax.tick_params(direction='in',length=l)

def boldAnnot(ax,x,y,txt,ha='left',va='top',size=12):
    ax.text(x,y,txt,transform=ax.transAxes,ha=ha,va=va,fontsize=size)

def readData(s):
    return pd.read_parquet("{:s}".format(s))

def mm2Inch(mm):
    return mm/25.4

def plotLogScoresByPrior(FSN,ax):
    if FSN==1:
        dynamic,static   = readData("./plotData/dynamic.pq"), readData("./plotData/static.pq")
       
    ax.plot( list(100*dynamic.prior), list(dynamic.avgLogScore), 'r-', label = 'Adaptive')

    minRow = dynamic.sort_values('avgLogScore').iloc[0]
    maxRow = dynamic.sort_values('avgLogScore').iloc[-1]

    _0prior = dynamic[dynamic.prior==0.01]
    
    print(_0prior['prior'])
    print(_0prior['avgLogScore'])
    print('Min Dynamic: prior={:.3f} logScore={:.3f}'.format(minRow['prior'],minRow['avgLogScore']))
    print('Max Dynamic: prior={:.3f} logScore={:.3f}'.format(maxRow['prior'],maxRow['avgLogScore']))
    
    ax.plot(list(100*static.prior) , list(static.avgLogScore), 'b--', label = 'Static')

    minRow = static.sort_values('avgLogScore').iloc[0]
    maxRow = static.sort_values('avgLogScore').iloc[-1]
 
    print('Min Static: prior={:.3f} logScore={:.3f}'.format(minRow['prior'],minRow['avgLogScore']))
    print('Max Static: prior={:.3f} logScore={:.3f}'.format(maxRow['prior'],maxRow['avgLogScore']))
    
def anot(ax,x,y,txt,ha,va,fontsize):
    ax.text(x,y,txt,ha=ha,va=va,transform=ax.transAxes,fontsize=fontsize)

def computeEWAvgLogScore(FSN):
    if FSN:
        d = pd.read_csv('../../../_5_compute_and_score__ensembles/analysisData/ensembleScores__equalscore.csv')
    return d

def add1stHalgVs2ndHalf(d):
    d['year'] = d.EWNum.astype(str).str.slice(0,4).astype(int)
    d['week'] = d.EWNum.astype(str).str.slice(4,6).astype(int)

    idx = (d.week >= 40) & (d.week<=53)
    d.loc[idx,'half'] = "First 1/2 of Season"
    d.loc[~idx,'half'] = "Second 1/2 of Season"
    return d

def addSeason(d):
    d['year'] = d.EWNum.astype(str).str.slice(0,4).astype(int)
    d['week'] = d.EWNum.astype(str).str.slice(4,6).astype(int)

    idx = (d.week >= 40) & (d.week<=53)
    d.loc[idx,'season'] = d[idx].apply( lambda x: "{:d}/{:d}".format(x['year'],x['year']+1),1 )
    d.loc[~idx,'season'] = d[~idx].apply( lambda x:  "{:d}/{:d}".format(x['year']-1,x['year']),1)
    return d


if __name__ == "__main__":
   
    mpl.rcParams['ytick.labelsize'] = 8
    mpl.rcParams['xtick.labelsize'] = 8
    mpl.rcParams["axes.labelsize"] = 10

    fig,ax = plt.subplots()
    
    plotLogScoresByPrior(FSN=1,ax=ax)
    ax.set_yticklabels(['{:.2f}'.format(y) for y in ax.get_yticks()])

    dynamic= readData("./plotData/dynamic.pq")
    maxs = dynamic.sort_values('avgLogScore').iloc[-1]

    avgEWLogScore = computeEWAvgLogScore(FSN=1)['logScore'].mean()
    ax.plot([0,100],[avgEWLogScore,avgEWLogScore],'k-.',alpha=0.50,label = 'Equally-weighted')

    ax.legend(frameon=False,loc='upper right')

    ax.set_yticklabels([y for y in ax.get_yticks()])

    ticksIn(ax)
    ax.set(xlabel = 'Prior percent (%)', ylabel = 'Average log score')
    ax.set_xlim(-1,100)
    ax.yaxis.set_major_formatter(FormatStrFormatter('%0.2f'))
    
    fig.set_tight_layout(True)
    fig.set_size_inches(mm2Inch(183),mm2Inch(183)/1.6)
    plt.savefig('fig10_logScoresForAllEnsemble.pdf')
    plt.savefig('fig10_logScoresForAllEnsemble.png')
    plt.savefig('fig10_logScoresForAllEnsemble.eps')
    plt.close()
