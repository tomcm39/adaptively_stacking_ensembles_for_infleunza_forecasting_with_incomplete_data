#mcandrew

import sys
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

from matplotlib.font_manager import FontProperties
import matplotlib.ticker as ticker

from matplotlib.collections import PatchCollection
from matplotlib.patches import Circle
from matplotlib.patches import Rectangle
from matplotlib.patches import ConnectionPatch
from matplotlib.patches import Patch

import seaborn as sns


def ticksIn(ax,l=3.):
    ax.tick_params(direction='in',length=l)
    
def mm2Inch(mm):
    return mm/25.4

def boldAnnot(ax,x,y,txt,ha='left',va='top',size=12):
    font0 = FontProperties()
    boldFont = font0.copy()
    boldFont.set_weight('bold')
    boldFont.set_size(size)
    ax.text(x,y,txt,transform=ax.transAxes,ha=ha,va=va,fontsize=size,fontproperties=boldFont)

def computeOnset(d):
    baselinesByRegionAndSeason = pd.read_csv('../../_4_score_component_model_forecasts/wiliBaselineDataByRegionAndYear/wILI_Baseline.csv')

    def fromLoc2Reg(row):
        import re
        if 'Region' in row:
            num = int(re.search('[0-9]+',row).group(0))
            return 'HHS{:d}'.format(num)
        return 'Nat'
    baselinesByRegionAndSeason['region'] = baselinesByRegionAndSeason.location.apply(fromLoc2Reg)

    season,region = d.Season.values[-1], d.region.values[-1]

    baselinesByRegionAndSeason = baselinesByRegionAndSeason[baselinesByRegionAndSeason['region']==region]
    d = d.merge(baselinesByRegionAndSeason, on = ['year'] )
    d['consec'] = np.arange(0,d.shape[0])

    aboveBaseline = d[d.wili> d.value]
    if aboveBaseline.shape[0]==0:
        return pd.Series({"Season onset":-1})

    oldModelWeek = aboveBaseline.iloc[0]['consec']
    onset = aboveBaseline.iloc[0]['week']
    inArow=0
    for (index,row) in aboveBaseline.iloc[1:].iterrows():
        modelWeek = row['consec']
        epiWeek   = row['week']
        if modelWeek - oldModelWeek > 1:
            onset = epiWeek
        else:
            inArow+=1
        if inArow==3:
            return pd.Series({"Season onset":onset})
        oldModelWeek = modelWeek
    return pd.Series({"Season onset":-1})

from matplotlib.collections import PatchCollection
from matplotlib.patches import Rectangle

def downloadIliData():
    return pd.read_csv('../../_2_processRawILIdata/analysisData/allFluData__releaseDate_location_EW_lag_ili_wili_year_week_modelWeek_calendarEW_Season.csv')

def diagonal(ax,color,downUp):
    if downUp:
        slope=-1
    else:
        slope=1
    xs = np.linspace(-1,1,10)
    for b0 in np.linspace(-1,2,10):
        ax.plot(xs, b0+slope*xs,"{:s}".format(color)+'-',lw=2.0, alpha=0.50, transform=ax.transAxes)

if __name__ == "__main__":

    mpl.rcParams['ytick.labelsize'] = 6
    mpl.rcParams['xtick.labelsize'] = 6
    mpl.rcParams["axes.labelsize"] = 8
    
    gs = gridspec.GridSpec(5,9,height_ratios=[10,1,1,1,1])
    
    iliData = downloadIliData()
    
    axes = []
    column2Season = {0:"2009/2010",1:"2010/2011",2:"2011/2012",3:"2012/2013",4:"2013/2014",5:"2014/2015",6:"2015/2016",7:"2016/2017",8:"2017/2018"}
    for column in range(9):
        axes.append([])
        for row in np.arange(2,4+1):
            ax = plt.subplot(gs[row,column])
            axes[column].append(ax)

            subsetIli = iliData[iliData.Season==column2Season[column]]
            mostRecentIli = subsetIli.groupby(['region','EW']).apply( lambda x: x.iloc[-1]  ) 
            avgIli = mostRecentIli.groupby(['EW']).apply( lambda x: pd.Series({'wili':np.mean(x.wili)}) ).reset_index()
            ax.plot(avgIli.wili.values,'k-')
            
            ax.set_yticks([])
            ax.set_xticks([])

            if column == 2 and row ==4:
                l = [Patch(facecolor='white',hatch="////",edgecolor='green',label='Train')]
                ax.legend(handles=l,frameon=False,loc='center left', bbox_to_anchor = (0.0,-1.5),fontsize=8.0)
                
            if column == 4 and row ==4: 
                l=[Patch(facecolor='white',edgecolor='red',hatch="\\\\",label='Predict')]
                ax.legend(handles=l,frameon=False,loc='center left', bbox_to_anchor = (0.00,-1.5),fontsize=8.0)
                
            if column == 6 and row ==4:
                l=[Patch(facecolor='white',edgecolor='brown',hatch=r"xxxx",label='Train & Predict')]
                ax.legend(handles=l,frameon=False,loc='center left', bbox_to_anchor = (0.00,-1.5),fontsize=8.0)

            if column == 0:
                if row == 2:
                    ax.text(-0.1,0.50,'Equal',ha='right',va='center',transform=ax.transAxes)
                if row == 3:
                    ax.text(-0.1,0.50,'Static',ha='right',va='center',transform=ax.transAxes)
                if row == 4:
                    ax.text(-0.1,0.50,'Adaptive',ha='right',va='center',transform=ax.transAxes)
            if row==2:
                if column < 8:
                    ax.set_facecolor('white')
                elif column ==8:
                    diagonal(ax,'r',1)

                else:
                    ax.set_facecolor('white')
            if row ==3:
                if column < 8:
                    diagonal(ax,'g',0)
                elif column ==8:
                    diagonal(ax,'r',1)
                else:
                    ax.set_facecolor('white')
            if row ==4:
                ax.set_xlabel(column2Season[column].replace('20',''))
                if column < 8:
                    ax.set_facecolor('white')
                elif column ==8:
                    diagonal(ax,'r',1)
                    diagonal(ax,'g',0)
                else:
                    ax.set_facecolor('white')

                   
    ax = plt.subplot(gs[0,:])
    d = downloadIliData()
    season20152016 = d.loc[(d.Season=='2015/2016') & ( d.calendarEW==201640) & (d.EW <= 201620) & (d.region=='Nat') ]
    
    ax.plot( season20152016.modelWeek, season20152016.wili, 'k-', label ='' )
    ax.set_ylabel('Weighted ILI, as of 2016-10-07 (%)')
    
    timePoint = 53
    _1wk = float(season20152016.loc[ season20152016.modelWeek == timePoint-1, 'wili' ])
    ax.text( timePoint-1, _1wk+0.35, '1 wk ahead', ha='right', va='center' )
    ax.plot([ timePoint-1, timePoint-1.45 ],[_1wk, _1wk+0.25],'k-')
    
    _2wk = float(season20152016.loc[ season20152016.modelWeek == timePoint-0, 'wili' ])
    ax.text(  timePoint-0.5, _2wk+1.5, '2 wk ahead', ha='center', va='center' )
    ax.plot([ timePoint-0, timePoint-0.65 ],[_2wk, _2wk+1.4],'k-')

    _3wk = float(season20152016.loc[ season20152016.modelWeek == timePoint+1, 'wili' ])
    ax.text(  timePoint+2.05, _3wk+0.85, '3 wk ahead', ha='center', va='center' )
    ax.plot([ timePoint+1, timePoint+1 ],[_3wk, _3wk+0.7],'k-')

    _4wk = float(season20152016.loc[ season20152016.modelWeek == timePoint+2, 'wili' ])
    ax.text(  timePoint+2.35, _4wk+0.45, '4 wk ahead', ha='left', va='center' )
    ax.plot([ timePoint+2, timePoint+2.5 ],[_4wk, _4wk+0.30],'k-')

    ax.plot(timePoint+4.3, _4wk+0.490,'wo',ms=10,fillstyle='full')

    peaks = season20152016.sort_values('wili').iloc[-1]
    peakWeek, peakWili = peaks.modelWeek, peaks.wili
    
    ax.plot([peakWeek, peakWeek+0.8], [1.30,1.5], 'k-')
    ax.plot(peakWeek,1.30, 'ro')
    ax.text(peakWeek+0.9, 1.5, 'Peak week', fontsize=10)
    
    ax.plot([peakWeek, peakWeek+0.8], [peakWili,peakWili+0.1], 'k-')
    ax.text(peakWeek+0.9, peakWili, 'Peak wILI', fontsize=10)
    
    times    = [52,53,54,55]
    wkAheads = [_1wk,_2wk,_3wk,_4wk]
    ax.plot( times, wkAheads, 'ro'  )
    ax.plot(peakWeek, peakWili, 'ro')

    availableWeeks = np.arange(40,timePoint-1)
    wilis = list(season20152016.loc[season20152016.modelWeek<timePoint-1,'wili'])
    ax.fill_between(availableWeeks , [min(wilis)]*len(availableWeeks), wilis, color='k',alpha=0.30  )
    ax.text(timePoint-2, 1.35, 'Available ILI data', ha='right',va='center', fontsize=10 )
    
    ax.set_xticks([40,45, 52, 53 ,54,55,56,60,65,70, peakWeek])
    ax.set_xticklabels(['201540','201545','201552',"","201602",'','201604','201608','201613','201619','201610'])

    
    ax.set_ylim(min(wilis),4.0)
    ticksIn(ax,2.)

    wili = float(season20152016.loc[season20152016.modelWeek==timePoint,'wili'])
    ax.plot([timePoint, timePoint], [1.30,_2wk-0.073], 'b--')
    ax.text(timePoint+0.2, 1.65, 'Calendar week', color = 'b', fontsize=10)

    seasonOnset = float(computeOnset(season20152016))
    modelWeekOnset = float(season20152016.loc[season20152016['week']==seasonOnset,'modelWeek'])
    ax.plot( [modelWeekOnset, modelWeekOnset], [1.3]*2, 'ro', label = 'Forecasting targets')
    ax.plot( [modelWeekOnset+0.275, modelWeekOnset+0.95], [1.35,1.45], 'k-' )
    ax.text(modelWeekOnset+1, 1.45, 'Season onset', ha='left', va='center')

    ax.legend(frameon=False,loc='upper left')
    ax.set_xlim(40,72)

    #zoom
    con = ConnectionPatch( xyA = (0.5,0.5) ,xyB = (0.5,0.5)
                           ,coordsA = "figure fraction" , coordsB = "figure fraction"
                           ,axesA= axes[5][0] ,  axesB = ax)
    ax.add_artist(con)
    
    plt.subplots_adjust(wspace=0.0)
    fig = plt.gcf()
    fig.set_size_inches(mm2Inch(183),mm2Inch(183)/1.6)

    plt.savefig('./fig1_conceptDiagram.pdf')
    plt.savefig('./fig1_conceptDiagram.png')
    plt.savefig('./fig1_conceptDiagram.eps')
    plt.close()
