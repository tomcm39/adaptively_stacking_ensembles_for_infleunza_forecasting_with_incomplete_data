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
        dynamic,static   = readData("./plotData/dynamic.pq"), readData("./plotData/static.pq")
        dynamic5,static5 = readData("./plotData/dynamic5.pq"), readData("./plotData/static5.pq")
    else:
        dynamic,static   = readData("./plotData/cdc/dynamic.pq"), readData("./plotData/cdc/static.pq")
        dynamic5,static5 = readData("./plotData/cdc/dynamic5.pq"), readData("./plotData/cdc/static5.pq")
        
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
        yTop = [-3.75,-3.20,-3.2]
        yBot = [-3.80, -3.5, -4.9]
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

    #gridof scores
    fig, ax = plt.subplots()


    overallAverage = readData('./plotData/averagedOverAll.pq')
    
    FSNdynBySeas,FSNstaBySeas = readData("./plotData/dynamicBySeason.pq"), readData("./plotData/staticBySeason.pq")
    FSNdynBySeasPrior08 = FSNdynBySeas.loc[FSNdynBySeas.prior==0.08,['season','avgLogScore']]
    FSNdynBySeasPrior08['model'] = r"Adaptive$_{\mathrm{opt}}$"
    
    average = overallAverage[(overallAverage.modelType=='dynamic') & (overallAverage.prior==0.08)].avgLogScore
    FSNdynBySeasPrior08 = FSNdynBySeasPrior08.append(pd.DataFrame({'model':r'Adaptive$_{\mathrm{opt}}$','season':'Overall','avgLogScore':average}))

    
    FSNdynBySeasPrior01 = FSNdynBySeas.loc[FSNdynBySeas.prior==0.0,['season','avgLogScore']]
    FSNdynBySeasPrior01['model'] = r"Adaptive$_{\mathrm{non}}$"
    
    average = overallAverage[(overallAverage.modelType=='dynamic') & (overallAverage.prior==0.0)].avgLogScore
    FSNdynBySeasPrior01 = FSNdynBySeasPrior01.append(pd.DataFrame({'model':r'Adaptive$_{\mathrm{non}}$','season':'Overall','avgLogScore':average}))


    FSNdynBySeasPrior20 = FSNdynBySeas.loc[FSNdynBySeas.prior==0.20,['season','avgLogScore']]
    FSNdynBySeasPrior20['model'] = r"Adaptive$_{\mathrm{over}}$"
    
    average = overallAverage[(overallAverage.modelType=='dynamic') & (overallAverage.prior==0.20)].avgLogScore
    FSNdynBySeasPrior20 = FSNdynBySeasPrior20.append(pd.DataFrame({'model':r'Adaptive$_{\mathrm{over}}$','season':'Overall','avgLogScore':average}))

    
    FSNstaBySeasPrior08 = FSNstaBySeas.loc[FSNstaBySeas.prior==0.00,['season','avgLogScore']]
    FSNstaBySeasPrior08['model'] = "Static"

    average = overallAverage[(overallAverage.modelType=='static') & (overallAverage.prior==0.00)].avgLogScore
    FSNstaBySeasPrior08 = FSNstaBySeasPrior08.append(pd.DataFrame({'model':'Static','season':'Overall','avgLogScore':average}))
    
    
    FSNEWBySeas = computeEWAvgLogScore(FSN=1)
    FSNEWBySeas = addSeason(FSNEWBySeas).groupby('season').apply(lambda x: pd.Series({'avgLogScore':np.mean(x.logScore)})).reset_index()
    FSNEWBySeas['model'] = 'EW'
 
    FSNEWOverall = computeEWAvgLogScore(FSN=1)
    average = pd.Series({'avgLogScore':np.mean(FSNEWOverall.logScore)})
    FSNEWBySeas = FSNEWBySeas.append(pd.DataFrame({'model':'EW','season':'Overall','avgLogScore':average}))

    
    heatMapData = FSNdynBySeasPrior08
    for d in [FSNstaBySeasPrior08,FSNEWBySeas,FSNdynBySeasPrior01,FSNdynBySeasPrior20]:
        heatMapData = heatMapData.append(d)

    heatMapData = heatMapData.set_index('model')
    heatMapData = heatMapData.pivot_table(columns='season',index='model')
    heatMapData = heatMapData.iloc[[3,4,0,1,2]]
    sns.heatmap(heatMapData 
                ,ax=ax, annot=True
                ,xticklabels = ['2011/2012','2012/2013','2013/2014','2014/2015','2015/2016','2016/2017','2017/2018','Overall']
                ,cmap = 'viridis'
                ,cbar_kws = {'fraction':0.05}
                ,annot_kws={"size": 10, "va":'center','ha':'center'}
                ,fmt='.2f'
                ,linewidth=0.50)
    ax.set_ylabel('')
    ax.set_xticklabels(ax.get_xticklabels(),fontsize=7,rotation=0)
    ax.set_yticklabels(ax.get_yticklabels(),va='center',ha='center',rotation=90)

    
    sns.despine(left=False)
    ax.set_xlabel('')
    
    fig.set_tight_layout(True)
    fig.set_size_inches(mm2Inch(183),mm2Inch(183)/1.6)
    plt.savefig('fig4_logScoreGrid.pdf')
    plt.savefig('fig4_logScoreGrid.png')
    plt.savefig('fig4_logScoreGrid.eps')
    plt.close()
