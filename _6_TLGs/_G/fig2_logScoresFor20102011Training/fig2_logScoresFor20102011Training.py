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
    if FSN:
        dynamic,static   = readData("./plotData/adapt.pq"), readData("./plotData/static.pq")
        dynamic5,static5 = readData("./plotData/adapt5.pq"), readData("./plotData/static5.pq")
        
    ax.plot(100*dynamic.prior, dynamic.avgLogScore, 'r-', label = 'Dynamic')
    ax.plot(100*static.prior , static.avgLogScore, 'b-', label = 'Static')

def anot(ax,x,y,txt,ha,va,fontsize):
    ax.text(x,y,txt,ha=ha,va=va,transform=ax.transAxes,fontsize=fontsize)

def computeEWAvgLogScore(FSN):
    if FSN:
        d = pd.read_csv('../scoreEnsembleModelsAgainstRealTimeRevisedData/analysisData/allSingleScores_ewModels_trueILI_-2.0000.csv')
    else:
        d = pd.read_csv('../scoreEnsembleModelsAgainstRealTimeRevisedData/cdc/analysisData/allSingleScores_ewModels_trueILI_-2.0000.csv')
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


def plotBySeason(FSN,col):
    
    if FSN:
        dynamicBySeason,staticBySeason   = readData("./plotData/dynamicBySeason.pq"), readData("./plotData/staticBySeason.pq")
        dynamicBySeason5,staticBySeason5 = readData("./plotData/dynamicBySeason5.pq"), readData("./plotData/staticBySeason5.pq")
    else:
        dynamicBySeason,staticBySeason   = readData("./plotData/cdc/dynamicBySeason.pq"), readData("./plotData/cdc/staticBySeason.pq")
        dynamicBySeason5,staticBySeason5 = readData("./plotData/cdc/dynamicBySeason5.pq"), readData("./plotData/cdc/staticBySeason5.pq")

    n=0
    EWLogScores = computeEWAvgLogScore(FSN=FSN)
    EWLogScores = addSeason(EWLogScores)
    EWLogScores = add1stHalgVs2ndHalf(EWLogScores)
    avgEWLogScore_bySeason = EWLogScores.groupby('season').apply(lambda x: float(x.logScore.mean())).reset_index()

    if FSN ==0:
        yTop = [-3.78,-3.25,-3.43]
        yBot = [-3.86, -3.5, -4.73]
        for (season,data) in dynamicBySeason.groupby('season'):
            if season not in {'2015/2016','2016/2017','2017/2018'}:
                continue
            ax = plt.subplot(gs[n,6:])
            ax.plot(100*data.prior, data.avgLogScore, label = '{:s}'.format(season), color = 'r')
            ax.text(0.98,0.98,'{:s}'.format(season),ha='right',va='top',transform=ax.transAxes,fontsize=8)
            ticksIn(ax,2.)

            #equal weighting
            avgEWLogScore_for1Season = avgEWLogScore_bySeason[avgEWLogScore_bySeason.season==season]
            ax.plot([0,100],[avgEWLogScore_for1Season]*2,'k-',alpha=0.50)

            if n<2:
                ax.set_xticklabels([])
            yticks = ax.get_yticks()
            ax.set_ylim([yBot[n], yTop[n]])
            ax.set_yticks([yticks[0],yticks[-1]])
            n+=1

    else:
        n=0
        for (season,data) in staticBySeason.groupby('season'):
            if season not in {'2015/2016','2016/2017','2017/2018'}:
                continue
            ax = plt.subplot(gs[n,2:3+1])
            ax.plot(100*data.prior, data.avgLogScore, label = '{:s}'.format(season), color = 'b')
            ax.text(0.98,0.98,'{:s}'.format(season),ha='right',va='top',transform=ax.transAxes,fontsize=8)

            ax.yaxis.set_major_locator(MaxNLocator(2))
            
            if n < 2:
                ax.set_xticklabels([])
            yticks = ax.get_yticks()
            ax.set_yticks([yticks[0],yticks[-1]])
            n+=1

        n=0
        for (season,data) in dynamicBySeason.groupby('season'):
            if season not in {'2015/2016','2016/2017','2017/2018'}:
                continue
            ax = plt.subplot(gs[n,2:3+1])
            ax.plot(100*data.prior, data.avgLogScore, label = '{:s}'.format(season), color = 'r')
            ax.text(0.98,0.98,'{:s}'.format(season),ha='right',va='top',transform=ax.transAxes,fontsize=8)
            ticksIn(ax,2.)

            #equal weighting
            avgEWLogScore_for1Season = avgEWLogScore_bySeason[avgEWLogScore_bySeason.season==season]
            ax.plot([0,100],[avgEWLogScore_for1Season]*2,'k-',alpha=0.50)

            if n<2:
                ax.set_xticklabels([])
            yticks = ax.get_yticks()
            ax.set_yticks([yticks[0],yticks[-1]])
            n+=1
            
    ticksIn(ax)
    ax.set(xlabel = 'Prior percent (%)', ylabel = '')
        
if __name__ == "__main__":
   
    mpl.rcParams['ytick.labelsize'] = 8
    mpl.rcParams['xtick.labelsize'] = 8
    mpl.rcParams["axes.labelsize"] = 10

    fig,ax = plt.subplots()
    
    dynamicData = pd.read_csv('../../../_5_compute_and_score__ensembles/analysisData_preSeason/allEnsembleScores.csv')
    
    dynamicDataGrouped = dynamicData.groupby(['prior']).apply(lambda x: pd.Series({'logScore':np.mean(x.logScore)})).reset_index()
    mnILI,mxILI = min(dynamicDataGrouped.logScore), max(dynamicDataGrouped.logScore)
    
    maxPrior = dynamicDataGrouped.sort_values('logScore').iloc[-1]['prior']
    avgLogScore = -3.0 

    dd=0.001
    ax.plot([100*maxPrior,100*maxPrior+10]
            ,[mxILI,mxILI],'k-')
    ax.text(100*maxPrior+11, mxILI
            ,'adaptive$_{\mathrm{opt}}$ (prior=8%)', ha = 'left', va='center')                    

    overPrior = 0.20
    overILI = float(dynamicDataGrouped[dynamicDataGrouped.prior==0.20]['logScore'])
    ax.plot([100*overPrior,100*overPrior+10]
            ,[overILI,overILI],'k-')
    ax.text(100*overPrior+11, overILI 
            ,'adaptive$_{\mathrm{over}}$ (prior=20%)', ha = 'left', va='center')                    

    nonPrior = 0.0
    nonILI = float(dynamicDataGrouped[dynamicDataGrouped.prior==0.0]['logScore'])
    ax.plot([100*nonPrior,100*nonPrior+8]
            ,[nonILI,nonILI-0.02],'k-')
    ax.text(100*nonPrior+8, nonILI - 0.02 
            ,'adaptive$_{\mathrm{non}}$\n (prior=0%)', ha = 'left', va='center')                    

    ax.plot( 100*dynamicDataGrouped.prior, dynamicDataGrouped.logScore,'r-',label='Adaptive (10/11 season)')
    ax.legend(frameon=False,loc='lower left')
    
    ax.set_yticklabels(['{:.2f}'.format(y) for y in ax.get_yticks()])
    
    ticksIn(ax)
    ax.set(xlabel = 'Prior percent (%)', ylabel = 'Average log score')
    ax.set_xlim(-1,100)
  
    fig.set_tight_layout(True)
    fig.set_size_inches(mm2Inch(183),mm2Inch(183)/1.6)
    plt.savefig('fig2_logScoresFor20102011Training.pdf')
    plt.savefig('fig2_logScoresFor20102011Training.png')
    plt.savefig('fig2_logScoresFor20102011Training.eps')
    plt.close()
