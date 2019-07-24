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
    if FSN==1:
        dynamic,static   = readData("./plotData/dynamic.pq"), readData("./plotData/static.pq")
        dynamic5,static5 = readData("./plotData/dynamic5.pq"), readData("./plotData/static5.pq")
       
    ax.plot( list(100*dynamic.prior), list(dynamic.avgLogScore), 'r-', label = 'Dynamic')

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

    gs = gridspec.GridSpec(4,2)
    fig = plt.gcf()

    
    ax = plt.subplot(gs[0:,0])
    plotLogScoresByPrior(FSN=1,ax=ax)
    ax.set_yticklabels(['{:.2f}'.format(y) for y in ax.get_yticks()])

    
    dynamic= readData("./plotData/dynamic.pq")
    maxs = dynamic.sort_values('avgLogScore').iloc[-1]

    #ax.plot(100*maxs.prior,maxs.avgLogScore,'ro')
    
    
    avgEWLogScore = computeEWAvgLogScore(FSN=1)['logScore'].mean()
    ax.plot([0,100],[avgEWLogScore,avgEWLogScore],'k-.',alpha=0.50,label = 'Equal-weighted')

    ax.legend(frameon=False,loc='upper right')

    ax.set_yticklabels([y for y in ax.get_yticks()])

    ticksIn(ax)
    ax.set(xlabel = 'Prior percent (%)', ylabel = 'Average log score')
    #anot(ax,0.99,0.99,txt='FSN',ha='right',va='top',fontsize=12)

    
    # dynamicByTargetSeason  = readData("./plotData/dynamicByTargetSeason.pq")
    # dynamicByTargetSeason5 = readData("./plotData/dynamicByTargetSeason5.pq")
    
    # priorData = {'season':[],'target':[],'prior':[]}
    # oldSeason = '2009/2010'
    # n=0
    # colors = {'1 wk ahead':'r','2 wk ahead':'b','3 wk ahead':'k','4 wk ahead':'g'}
    # for (seasonAndTarget,data) in dynamicByTargetSeason.groupby(['season','target']):
    #     season,target = seasonAndTarget
    #     mx = data.sort_values('avgLogScore').iloc[-1]['prior']
    #     priorData['season'].append(season)
    #     priorData['target'].append(target)
    #     priorData['prior'].append(mx)
        
    #     if season != oldSeason:
    #         n+=1
    #         oldSeason = season
    # priorData = pd.DataFrame(priorData)

    
    
    dynamicByTargetSeasonRegion  = readData("./plotData/dynamicByTargetSeasonRegion.pq")
    dynamicByTargetSeasonRegion5 = readData("./plotData/dynamicByTargetSeasonRegion5.pq")
    
    priorData = {'season':[],'target':[],'region':[],'prior':[]}
    oldSeason = '2009/2010'
    n=0
    colors = {'1 wk ahead':'r','2 wk ahead':'b','3 wk ahead':'k','4 wk ahead':'g'}
    for (seasonAndTargetAndRegion,data) in dynamicByTargetSeasonRegion.groupby(['season','target','region']):
        season,target,region = seasonAndTargetAndRegion
        mx = data.sort_values('avgLogScore').iloc[-1]['prior']
        priorData['season'].append(season)
        priorData['target'].append(target)
        priorData['region'].append(region)
        priorData['prior'].append(mx)
        
        if season != oldSeason:
            n+=1
            oldSeason = season
    priorData = pd.DataFrame(priorData)

    


    print("Average Prior = {:.3f}".format(priorData.prior.mean()))
    print("Std. Prior = {:.3f}".format(priorData.prior.std()))
    
    n=0
    for target in ['1 wk ahead','2 wk ahead','3 wk ahead','4 wk ahead']:
        ax = plt.subplot(gs[n,1])
        n+=1
        
        seasonData = priorData[priorData.target=='{:s}'.format(target)]
        sns.boxplot(  x = 'season' ,y= 'prior',data = seasonData ,ax=ax, fliersize=0, color = 'green',boxprops=dict(alpha=.5))
        sns.stripplot(x = 'season' ,y= 'prior',data = seasonData ,ax=ax, color='.25',jitter=True,dodge=True,size=4)
        #ax.plot([-1,-1],[-1,-1],color='green',alpha=0.30,label='Regions')

        #ax.plot(seasonData.season,seasonData.prior,color = colors[target],alpha=0.50)
        #ax.scatter(seasonData.season,seasonData.prior,s=5,color = colors[target],alpha=0.50)

        ax.text(0.99,0.99,'{:s}'.format(target), ha= 'right', va='top',transform=ax.transAxes,fontsize=10)    
        ax.tick_params(direction='in',size=2)
        ax.set_ylabel('peak prior',fontsize=8)

        if n==1:
            from matplotlib.patches import Patch
            legend_elements = [Patch(facecolor='green',edgecolor='k',alpha=0.50,label='Region')]
            ax.legend(handles = legend_elements,frameon=False,loc='upper left',bbox_to_anchor = (0,1.135))
        
        if n <=3:
            ax.set_xticklabels([])

        ax.set_yticklabels(["{:d}".format(int(100*y)) for y in ax.get_yticks()])
        
        ax.set_ylim(-0.05,1.25)
        ax.set_xlabel('')
    ax.set_xticklabels([ x.replace('20','') for x in seasonData.season.unique()])
    
    fig.set_tight_layout(True)
    #plt.subplots_adjust(hspace=0.25,wspace=1.25,top=0.90,bottom=0.10,right=0.90,left=0.10)
    fig.set_size_inches(mm2Inch(183),mm2Inch(183)/1.6)
    plt.savefig('fig2_logScoresByPriorAndSeasonJustFSN.pdf')
    plt.savefig('fig2_logScoresByPriorAndSeasonJustFSN.png')
    plt.savefig('fig2_logScoresByPriorAndSeasonJustFSN.eps')
    plt.close()
