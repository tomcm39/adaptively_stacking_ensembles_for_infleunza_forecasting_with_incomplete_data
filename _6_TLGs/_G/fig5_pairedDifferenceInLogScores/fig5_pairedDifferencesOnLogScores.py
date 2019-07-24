#mcandrew

import sys
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from matplotlib.font_manager import FontProperties


import seaborn as sns

def mm2Inch(mm):
    return mm/25.4

def boldAnnot(ax,x,y,txt,ha='left',va='top',size=12):
    font0 = FontProperties()
    boldFont = font0.copy()
    boldFont.set_weight('bold')
    boldFont.set_size(size)
    ax.text(x,y,txt,transform=ax.transAxes,ha=ha,va=va,fontsize=size,fontproperties=boldFont)

def quikStatsPrefix(d,var,prefix):
    difLogScore = d['{:s}'.format(var)]
    N = np.sqrt(len(difLogScore))
    
    m = np.mean(difLogScore)
    s = np.std(difLogScore)
    return pd.Series( {'{:s}mean'.format(prefix): m
                       ,'{:s}lcl'.format(prefix):m+s*2/N
                       ,'{:s}ucl'.format(prefix):m-s*2/N
                       })

def quikStats(d):
    difLogScore = d['difLogScore__dynStat']
    N = np.sqrt(len(difLogScore))
    
    m = np.mean(difLogScore)
    s = np.std(difLogScore)
    return pd.Series( {'mean': m
                       ,'lcl':m+s*2/N
                       ,'ucl':m-s*2/N
                       })
 
def ticksIn(ax,l=3.):
    ax.tick_params(direction='in',length=l)

def plotLogScoresBySeason(ax):

    hor = -1
    hors = []
    seasons = []

    mainStep = 0.2
    halfStep = 0.0


    deRandomEffectsData = pd.read_csv('../../_T/tab1_ensembleComparisons/tableData/deRslts.csv')
    seasonDE = deRandomEffectsData[deRandomEffectsData['Unnamed: 0'].str.contains('season')]
    seasonDE = seasonDE[['Unnamed: 0','means','lowerCI','upperCI']]
    seasonDE = seasonDE.rename(columns={'Unnamed: 0':'season','means':'DEmean','lowerCI':'DElcl','upperCI':'DEucl'})
    seasonDE['season'] = [ x.split('.')[-1] for x in seasonDE.season]
    
    dsRandomEffectsData = pd.read_csv('../../_T/tab1_ensembleComparisons/tableData/dsRslts.csv')
    seasonDS = dsRandomEffectsData[dsRandomEffectsData['Unnamed: 0'].str.contains('season')]
    seasonDS = seasonDS[['Unnamed: 0','means','lowerCI','upperCI']]
    seasonDS = seasonDS.rename(columns={'Unnamed: 0':'season','means':'DSmean','lowerCI':'DSlcl','upperCI':'DSucl'})
    seasonDS['season'] = [ x.split('.')[-1] for x in seasonDS.season]
    
    allLogDifs = seasonDS.merge( seasonDE, on = 'season')
    for (season,stats) in allLogDifs.groupby('season'):
        season,ds_mean,ds_lcl,ds_ucl,de_mean,de_lcl,de_ucl, = season,float(stats.DSmean),float(stats.DSlcl),float(stats.DSucl),float(stats.DEmean),float(stats.DElcl),float(stats.DEucl)

        #DS
        ax.plot( [ds_lcl, ds_ucl], [hor]*2, 'r-', alpha=0.6 )
        ax.scatter( [ds_mean], [hor], edgecolors='r', facecolors='none' , s=22.5, alpha=0.6 )
        hor-=halfStep
        hors.append(hor)

        #DE
        ax.plot( [de_lcl, de_ucl], [hor]*2, 'k-', alpha=0.6 )
        ax.scatter( [de_mean], [hor], c='k' , s=22.5, alpha=0.6 )
        hor-=halfStep

        hor-=mainStep

        seasons.append(season)

    ax.set_yticks(hors)
    ax.set_yticklabels(seasons)
    ax.set_xlabel(r'')
    ax.set_ylabel('')
    ticksIn(ax,2.)
       
def plotLogScoresByLocation(ax):
    hor = 0
    hors = []
    regions = []

    deRandomEffectsData = pd.read_csv('../../_T/tab1_ensembleComparisons/tableData/deRslts.csv')
    regionDE = deRandomEffectsData[deRandomEffectsData['Unnamed: 0'].str.contains('region')]
    regionDE = regionDE[['Unnamed: 0','means','lowerCI','upperCI']]
    regionDE = regionDE.rename(columns={'Unnamed: 0':'region','means':'DEmean','lowerCI':'DElcl','upperCI':'DEucl'})
    regionDE['region'] = [ x.split('.')[-1] for x in regionDE.region]
    
    dsRandomEffectsData = pd.read_csv('../../_T/tab1_ensembleComparisons/tableData/dsRslts.csv')
    regionDS = dsRandomEffectsData[dsRandomEffectsData['Unnamed: 0'].str.contains('region')]
    regionDS = regionDS[['Unnamed: 0','means','lowerCI','upperCI']]
    regionDS = regionDS.rename(columns={'Unnamed: 0':'region','means':'DSmean','lowerCI':'DSlcl','upperCI':'DSucl'})
    regionDS['region'] = [ x.split('.')[-1] for x in regionDS.region]

    allLogDifs = regionDS.merge( regionDE, on = 'region')
    for n in np.arange(1,10+1):
        region = 'HHS{:d}'.format(n)
        stats = allLogDifs.groupby('region').get_group(region)
        ds__mean,ds__lcl,ds__ucl,de__mean,de__lcl,de__ucl  = float(stats['DSmean']),float(stats['DSlcl']),float(stats['DSucl']),float(stats['DEmean']),float(stats['DElcl']),float(stats['DEucl'])

        ax.plot( [ds__lcl, ds__ucl], [hor]*2, 'r-', alpha=0.6 )
        ax.scatter( [ds__mean], [hor], edgecolors='r', facecolors='none' , s=22.5, alpha=0.6 )

        ax.plot( [de__lcl, de__ucl], [hor]*2, 'k-', alpha=0.6 )
        ax.scatter( [de__mean], [hor], c='k' , s=22.5, alpha=0.6 )

        regions.append(region)
        hors.append(hor)
        hor-=1

    stats = allLogDifs.groupby('region').get_group('Nat')
    region,ds__mean,ds__lcl,ds__ucl,de__mean,de__lcl,de__ucl = 'Nat', float(stats['DSmean']),float(stats['DSlcl']),float(stats['DSucl']),float(stats['DEmean']),float(stats['DElcl']),float(stats['DEucl'])

    ax.plot( [ds__lcl, ds__ucl], [hor]*2, 'r-', alpha=0.6 )
    ax.scatter( [ds__mean], [hor], edgecolors='r', facecolors='none' , s=22.5, alpha=0.6 )

    ax.plot( [de__lcl, de__ucl], [hor]*2, 'k-', alpha=0.6 )
    ax.scatter( [de__mean], [hor], c='k' , s=22.5, alpha=0.6 )

    regions.append(region)
    hors.append(hor)
    ticksIn(ax,2.)

    ax.set_yticks(hors)
    ax.set_yticklabels(regions)
    ax.set_xlabel(r'')
    ax.set_ylabel('')

def plotLogScoresByTarget(ax):
    hor = 0
    hors = []
    targets = []
    mainStep=0.2

    deRandomEffectsData = pd.read_csv('../../_T/tab1_ensembleComparisons/tableData/deRslts.csv')
    targetDE = deRandomEffectsData[deRandomEffectsData['Unnamed: 0'].str.contains('target')]
    targetDE = targetDE[['Unnamed: 0','means','lowerCI','upperCI']]
    targetDE = targetDE.rename(columns={'Unnamed: 0':'target','means':'DEmean','lowerCI':'DElcl','upperCI':'DEucl'})
    targetDE['target'] = [ x.split('.')[-1] for x in targetDE.target]
    
    dsRandomEffectsData = pd.read_csv('../../_T/tab1_ensembleComparisons/tableData/dsRslts.csv')
    targetDS = dsRandomEffectsData[dsRandomEffectsData['Unnamed: 0'].str.contains('target')]
    targetDS = targetDS[['Unnamed: 0','means','lowerCI','upperCI']]
    targetDS = targetDS.rename(columns={'Unnamed: 0':'target','means':'DSmean','lowerCI':'DSlcl','upperCI':'DSucl'})
    targetDS['target'] = [ x.split('.')[-1] for x in targetDS.target]

    allLogDifs = targetDS.merge( targetDE, on = 'target')
 
    for (target,stats) in allLogDifs.groupby('target'):
        ds_mean,ds_lcl,ds_ucl,de_mean,de_lcl,de_ucl, = float(stats.DSmean),float(stats.DSlcl),float(stats.DSucl),float(stats.DEmean),float(stats.DElcl),float(stats.DEucl)

        #DS
        ax.plot( [ds_lcl, ds_ucl], [hor]*2, 'r-', alpha=0.6 )
        ax.scatter( [ds_mean], [hor], edgecolors='r', facecolors='none' , s=22.5, alpha=0.6 )

        #DE
        ax.plot( [de_lcl, de_ucl], [hor]*2, 'k-', alpha=0.6 )
        ax.scatter( [de_mean], [hor], c='k' , s=22.5, alpha=0.6 )

        targets.append(target)
        hors.append(hor)
        hor-=1

    ax.set_yticks(hors)
    ax.set_yticklabels(targets)
    ax.set_xlabel(r'')
    ax.set_ylabel('')
    ticksIn(ax,2.)

def plotVert(ax,horiz):
    ax.plot([horiz]*2,[ax.get_ylim()[0],ax.get_ylim()[1]*1],'k--',alpha=0.1)
    
if __name__ == "__main__":

    mpl.rcParams['ytick.labelsize'] = 6
    mpl.rcParams['xtick.labelsize'] = 6
    mpl.rcParams["axes.labelsize"] = 8
    gs  = gridspec.GridSpec(1, 3)
    
    gs.update(wspace=0.450, hspace=0.30)

    #FSN

    ax = plt.subplot(gs[0,0])
    plotLogScoresBySeason(ax)
    plotVert(ax,0)
    ax.set_xlim(-0.35,0.35)
    boldAnnot(ax=ax,x=0.99,y=0.99,txt='A.',ha='right',va='top',size=12)   

    #ax.set_ylabel('FSN models',fontsize=12)
    ax.text(0.40,-0.085,'Eq./Stat. model better',ha='right',va='top',transform=ax.transAxes,fontsize=6.0)
    ax.text(0.55,-0.085,'Adaptive model better',ha='left',va='top',transform=ax.transAxes,fontsize=6.0)
    
    ax = plt.subplot(gs[0,1])
    plotLogScoresByLocation(ax)
    plotVert(ax,0)
    ax.set_xlabel(r'')

    ax.text(0.45,-0.085,'Eq./Stat. model better',ha='right',va='top',transform=ax.transAxes,fontsize=6.0)
    ax.text(0.55,-0.085,'Adaptive model better',ha='left',va='top',transform=ax.transAxes,fontsize=6.0)

    ax.scatter(10,0,edgecolor='r',facecolor='none',label='Adaptive vs. Static')
    ax.scatter(10,0,c='k',label='Adaptive vs. Equal')
    ax.legend(frameon=False,loc='upper center',ncol=2,fontsize=8,markerscale=1.0, handletextpad=0,mode='extended',bbox_to_anchor = (0.5,1.175))

    ax.set_xlim(-0.35,0.35)
    boldAnnot(ax=ax,x=0.99,y=0.99,txt='B.',ha='right',va='top',size=12)   

    ax = plt.subplot(gs[0,2])
    plotLogScoresByTarget(ax)
    plotVert(ax,0)
    ax.set_xlim(-0.35,0.35)
    boldAnnot(ax=ax,x=0.99,y=0.99,txt='C.',ha='right',va='top',size=12)   
   
    ax.text(0.45,-0.085,'Eq./Stat. model better',ha='right',va='top',transform=ax.transAxes,fontsize=6.0)
    ax.text(0.55,-0.085,'Adaptive model better',ha='left',va='top',transform=ax.transAxes,fontsize=6.0)
 
    fig = plt.gcf()
    
    fig.set_size_inches(mm2Inch(183),mm2Inch(183)/3.5)
    fig.set_tight_layout(True)
    
    plt.savefig('fig5_pairedDifferenceInLogScores.pdf')
    plt.savefig('fig5_pairedDifferenceInLogScores.png')
    plt.savefig('fig5_pairedDifferenceInLogScores.eps')
    plt.close()
