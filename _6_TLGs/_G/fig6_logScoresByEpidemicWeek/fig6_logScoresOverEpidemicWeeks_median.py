#mcandrew

import sys
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns

def boldAnnot(ax,x,y,txt,ha='left',va='top',size=12):
    font0 = FontProperties()
    boldFont = font0.copy()
    boldFont.set_weight('bold')
    boldFont.set_size(size)
    ax.text(x,y,txt,transform=ax.transAxes,ha=ha,va=va,fontsize=size,fontproperties=boldFont)

def downloadWeightData():
    data = pd.read_csv('../../../_5_compute_and_score__ensembles/analysisData/allEnsembleWeights.csv')
    data = data.drop(['Unnamed: 0','Unnamed: 0.1'],1)
    data = data[data['CU-BMA']>=0]
    return data

def fromEW2Season(EW):
    year,week = int(str(EW)[:4]),int(str(EW)[4:])
    if 40<= week <=53:
        return "{:d}/{:d}".format(year,year+1)
    return "{:d}/{:d}".format(year-1,year)

def downloadData():
    return pd.read_csv('../../../_5_compute_and_score__ensembles/analysisData/allEnsembleScores.csv')

def meanLogScore(d):
    return pd.Series({'avgLogScore':d.logScore.mean()})

def meanLogScore5(d):
    return pd.Series({'avgLogScore':d.logScore5.mean()})

def addSeason(d):
    d['year'] = d.EWNum.astype(str).str.slice(0,4).astype(int)
    d['week'] = d.EWNum.astype(str).str.slice(4,6).astype(int)

    idx = (d.week >= 40) & (d.week<=53)
    d.loc[idx,'season'] = d[idx].apply( lambda x: "{:d}/{:d}".format(x['year'],x['year']+1),1 )
    d.loc[~idx,'season'] = d[~idx].apply( lambda x:  "{:d}/{:d}".format(x['year']-1,x['year']),1)
    return d

def add1stHalgVs2ndHalf(d):
    d['year'] = d.EWNum.astype(str).str.slice(0,4).astype(int)
    d['week'] = d.EWNum.astype(str).str.slice(4,6).astype(int)

    idx = (d.week >= 40) & (d.week<=53)
    d.loc[idx,'half'] = "First 1/2 of Season"
    d.loc[~idx,'half'] = "Second 1/2 of Season"
    return d


if __name__ == "__main__":
 
    # allWts = downloadWeightData()
    # dynamic, static = allWts[allWts.modelType=='dynamic'], allWts[allWts.modelType=='static']

    # dynamic['season'] = [fromEW2Season(x) for x in dynamic.week]
    # static['season']  = [fromEW2Season(x) for x in static.week]


    # static00 = static[static.prior==10**-5]
    # dynamic00 = dynamic[dynamic.prior==10**-5]

    # tDynamic = pd.melt(dynamic00, id_vars = ['season','week','modelType','prior'])
    # tDynamic['logValue'] = np.log(tDynamic.value)

    # tStatic = pd.melt(static00, id_vars = ['season','week','modelType','prior'])
    # tStatic['logValue'] = np.log(tStatic.value)
    

    # def endOfSeason(rows):
    #     return rows['value'].iloc[-1]
    # tStaticEndOfSeason = tStatic.groupby(['variable','season']).apply(endOfSeason).reset_index()


    # logDifs = pd.read_parquet('../plotDifferencesInLogScores/plotData/logDifs.pq')

    allLogScores = downloadData()
    allLogScores = addSeason(allLogScores)

    dynamic, static, equal = allLogScores[allLogScores.modelType=='dynamic'], allLogScores[allLogScores.modelType=='static'], allLogScores[allLogScores.modelType=='equal']
    dynamic = dynamic[dynamic.prior==0.08]
    static  = static[static.prior==0.0]

    dynamicByEW = dynamic.groupby(['season','target','EWNum']).mean().reset_index()
    def addModelWeeks(d):
        d['modelWeeks'] = np.arange(1,d.shape[0]+1)
        return d
    dynamicByEW = dynamicByEW.groupby(['season','target']).apply(addModelWeeks)
    dynamicByEW['model'] = 'adaptive'
    
    staticByEW = static.groupby(['season','target','EWNum']).mean().reset_index()
    staticByEW = staticByEW.groupby(['season','target']).apply(addModelWeeks)
    staticByEW['model'] = 'static'

    equalByEW = equal.groupby(['season','target','EWNum']).mean().reset_index()
    equalByEW = equalByEW.groupby(['season','target']).apply(addModelWeeks)
    equalByEW['model'] = 'equal'
    
    allModelsByEW = dynamicByEW.append(staticByEW)
    allModelsByEW = allModelsByEW.append(equalByEW)

    r,c,i=0,0,0
    fig,axs = plt.subplots(2,2)
    fAxs = [ c for r in axs for c in r ]
    letters = ['A.','B.','C.','D.']
    for n in np.arange(1,4+1):
        ax = fAxs[n-1]
        targetOnly = allModelsByEW[allModelsByEW.target=='{:d} wk ahead'.format(n)]

        if n ==1:
            sns.lineplot(x='modelWeeks', y='logScore', hue='model', style='model', data = targetOnly, ax=ax, legend=False,estimator=np.median)
            ax.legend(frameon=False,loc='lower right',fontsize=8, labels = ['Adaptive$_{\mathrm{opt}}$','Static','EW'])
        else:
            sns.lineplot(x='modelWeeks', y='logScore', hue='model', style='model', data = targetOnly, ax=ax, legend=False,estimator=np.median)
        boldAnnot(ax=ax,x=0.02,y=0.99,txt=letters[i],ha='left',va='top',size=12)
        i+=1

        if n in {1,2}:
            ax.set_xlabel('')
        else:
            ax.set_xlabel('Weeks from start of season')
        ax.tick_params(direction='in',length=2.)
        ax.text(x=0.02,y=0.02,s='{:d} week ahead'.format(n),transform=ax.transAxes,ha='left',va='bottom',fontsize=8)
        ax.set_ylim(-5.5,-1.0)
        ax.set_xlim(0.5,ax.get_xlim()[-1])
        
    fig.set_tight_layout(True)
    plt.savefig('./fig6_logScoresOverEpidemicWeeks_median.pdf')
    plt.savefig('./fig6_logScoresOverEpidemicWeeks_median.eps')
    plt.savefig('./fig6_logScoresOverEpidemicWeeks_median.png')
