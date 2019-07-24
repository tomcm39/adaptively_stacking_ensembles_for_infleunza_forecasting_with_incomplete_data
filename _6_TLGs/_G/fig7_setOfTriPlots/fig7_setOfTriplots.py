#mcandrew

import sys
import pickle
import numpy as np
import pandas as pd

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.cm     as cm
import mpl_toolkits.axes_grid1 as axgrid
from mpl_toolkits.axes_grid1.colorbar import colorbar
from matplotlib.font_manager import FontProperties
import seaborn as sns

import re
import ternary
from ternary import helpers
import matplotlib.gridspec as gridspec

def downloadWeightData():
    data = pd.read_csv('../../../_5_compute_and_score__ensembles/analysisData/allEnsembleWeights.csv')
    data = data.drop(['Unnamed: 0','Unnamed: 0.1'],1)
    data = data[data['CU-BMA']>=0]
    return data

def subset2Top2PlusRest(weightData,model1,model2):
    def sumTop2PlusRest(row,model1,model2):
        weight1 = float(row[model1])
        weight2 = float(row[model2])
        return pd.Series( {'weight1':weight1,'weight2':weight2, 'weight3': 1.- (weight1+weight2)})
    return  weightData.groupby('week').apply(lambda x: sumTop2PlusRest(x,model1,model2)).reset_index()

def fromWeightsDataFrame2List(top2PlusRest):
    weightList = []
    for idx,row in top2PlusRest.iterrows():
        if row[0] == -999:
            continue
        weightList.append( [row[0],row[1], row[2]] )
    return weightList

def addSeason(d):
    d['year'] = d.week.astype(str).str.slice(0,4).astype(int)
    d['week'] = d.week.astype(str).str.slice(4,6).astype(int)

    idx = (d.week >= 40) & (d.week<=53)
    d.loc[idx,'season'] = d[idx].apply( lambda x: "{:.0f}/{:.0f}".format(x['year'],x['year']+1),1 )
    d.loc[~idx,'season'] = d[~idx].apply( lambda x:  "{:.0f}/{:.0f}".format(x['year']-1,x['year']),1)
    return d

def setupPlot():
    gs = gridspec.GridSpec(1,1)
    fig = plt.gcf()
    fig.set_size_inches(8.0,8.0/1.75)
    
    ax = plt.subplot(gs[0])
    tax = ternary.TernaryAxesSubplot(ax=ax)
    
    tax.boundary(linewidth=1.0)
    tax.gridlines(color="black", multiple=0.2, linewidth = 0.10)
    tax.ticks(axis='lbr', linewidth=1, multiple=0.2,tick_formats='%.1f',fontsize=5)
    return tax

def mm2Inch(mm):
    return mm/25.4

def computePis(dynamic, prior, model1_model2):
    
    weightData = dynamic[dynamic.prior==prior]
    weightData = addSeason(weightData)
    weightData = weightData[weightData.season==season]
    
    model1,model2 = model1_model2
    top2PlusRest = subset2Top2PlusRest(weightData, model1, model2)
    top2PlusRest = top2PlusRest.sort_values('week')
    top2PlusRest['prior'] = prior

    correctWeekOrder = pd.DataFrame(list(np.arange(40,53+1)) + list(np.arange(1,20+1)))
    correctWeekOrder.rename(columns={0:'week'},inplace=True)
    
    top2PlusRest = correctWeekOrder.merge(top2PlusRest,on='week')
    
    pis = top2PlusRest[['weight1','weight2','weight3']]
    pis = fromWeightsDataFrame2List(pis)
    return pis

def computePisAndWeeks(dynamic, prior, model1_model2):
    
    weightData = dynamic[dynamic.prior==prior]
    weightData = addSeason(weightData)
    weightData = weightData[weightData.season==season]
    
    model1,model2 = model1_model2
    top2PlusRest = subset2Top2PlusRest(weightData, model1, model2)
    top2PlusRest = top2PlusRest.sort_values('week')
    top2PlusRest['prior'] = prior

    correctWeekOrder = pd.DataFrame(list(np.arange(40,53+1)) + list(np.arange(1,20+1)))
    correctWeekOrder.rename(columns={0:'week'},inplace=True)
    
    top2PlusRest = correctWeekOrder.merge(top2PlusRest,on='week')
    
    pis = top2PlusRest[['weight1','weight2','weight3']]
    pis = fromWeightsDataFrame2List(pis)
    return (top2PlusRest.week,pis)
    
def fromEW2Season(EW):
    year,week = int(str(EW)[:4]),int(str(EW)[4:])
    if 40<= week <=53:
        return "{:d}/{:d}".format(year,year+1)
    return "{:d}/{:d}".format(year-1,year)


def findHeaviestAverageWeight(x):
    justModels = x.iloc[:,:-4]
    top2Models = list(justModels.mean().sort_values()[-2:].index)
    return top2Models

def findMLEweight(x):
    sortedValues = x[x.prior==0.01].iloc[-1][:-4].sort_values()
    _2nd1st = list(sortedValues[-2:].index)
    _1st2nd = [_2nd1st[-1], _2nd1st[0]]
    return _1st2nd

def fromTern2Cart(triples):
    carts = []
    for triple in triples:
        a,b,c= triple
        carts.append( (0.5*(2*b+c)/(a+b+c), 0.5*np.sqrt(3)*c/(a+b+c)))
    return carts


def arrowplot(axes, x, y, nArrs=30, mutateSize=10, color='gray', markerStyle='o',LS='-',alpha=1.0): 
    '''arrowplot : plots arrows along a path on a set of axes
        axes   :  the axes the path will be plotted on
        x      :  list of x coordinates of points defining path
        y      :  list of y coordinates of points defining path
        nArrs  :  Number of arrows that will be drawn along the path
        mutateSize :  Size parameter for arrows
        color  :  color of the edge and face of the arrow head
        markerStyle : Symbol

        Bugs: If a path is straight vertical, the matplotlab FanceArrowPatch bombs out.
          My kludge is to test for a vertical path, and perturb the second x value
          by 0.1 pixel. The original x & y arrays are not changed

        MHuster 2016, based on code by 
    '''
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # recast the data into numpy arrays
    x = np.array(x, dtype='f')
    y = np.array(y, dtype='f')
    nPts = len(x)

    # Plot the points first to set up the display coordinates
    axes.scatter(x,y, marker=markerStyle, s=5.0, facecolors='none', color=color,alpha=alpha)

    # get inverse coord transform
    inv = ax.transData.inverted()

    # transform x & y into display coordinates
    # Variable with a 'D' at the end are in display coordinates
    xyDisp = np.array(axes.transData.transform([(x,y) for (x,y) in zip(x,y)]))
    xD = xyDisp[:,0]
    yD = xyDisp[:,1]

    # drD is the distance spanned between pairs of points
    # in display coordinates
    dxD = xD[1:] - xD[:-1]
    dyD = yD[1:] - yD[:-1]
    drD = np.sqrt(dxD**2 + dyD**2)

    # Compensating for matplotlib bug
    dxD[np.where(dxD==0.0)] = 0.1


    # rtotS is the total path length
    rtotD = np.sum(drD)

    # based on nArrs, set the nominal arrow spacing
    arrSpaceD = rtotD / nArrs

    # Loop over the path segments
    iSeg = 0
    while iSeg < nPts - 1:
        # Figure out how many arrows in this segment.
        # Plot at least one.
        nArrSeg = max(1, int(drD[iSeg] / arrSpaceD + 0.5))
        xArr = (dxD[iSeg]) / nArrSeg # x size of each arrow
        segSlope = dyD[iSeg] / dxD[iSeg]
        # Get display coordinates of first arrow in segment
        xBeg = xD[iSeg]
        xEnd = xBeg + xArr
        yBeg = yD[iSeg]
        yEnd = yBeg + segSlope * xArr
        # Now loop over the arrows in this segment
        for iArr in range(nArrSeg):
            # Transform the oints back to data coordinates
            xyData = inv.transform(((xBeg, yBeg),(xEnd,yEnd)))
            # Use a patch to draw the arrow
            # I draw the arrows with an alpha of 0.5
            p = patches.FancyArrowPatch( 
                xyData[0], xyData[1], 
                arrowstyle='simple',
                mutation_scale=mutateSize
                ,linestyle=LS,alpha=alpha,
                color=color)
            axes.add_patch(p)
            # Increment to the next arrow
            xBeg = xEnd
            xEnd += xArr
            yBeg = yEnd
            yEnd += segSlope * xArr
        # Increment segment number
        iSeg += 1

    
if __name__ == "__main__":

    allWts = downloadWeightData()
    dynamic, static = allWts[allWts.modelType=='dynamic'], allWts[allWts.modelType=='static']

    dynamic['season'] = [fromEW2Season(x) for x in dynamic.week]
    static['season']  = [fromEW2Season(x) for x in static.week]

    season2Models = {}
    for (season,data) in dynamic.groupby('season'):
        season2Models[season] = findMLEweight(data)
    
    mycmap = cm.viridis
    gs = gridspec.GridSpec(2,4)
    fig = plt.gcf()
    fig.set_size_inches(mm2Inch(183),mm2Inch(183)/1.5)

    r,c=0,0
    for season in ["2011/2012","2012/2013","2013/2014","2014/2015","2015/2016","2016/2017","2017/2018"]:

        #---------------------------------------------------------------------------
        ax = plt.subplot(gs[r,c])
        tax = ternary.TernaryAxesSubplot(ax=ax)

        tax.boundary(linewidth=1.0)
        tax.gridlines(color=".15", multiple=0.2, linewidth = 0.10)
        tax.ticks(axis='lbr', offset=0.03, linewidth=1, multiple=0.2,tick_formats='%.1f',fontsize=5)

        tax.set_axis_limits({'b':[0,1],'l':[0,1],'r':[0,1]})
        tax.set_title(season,fontsize=8)

        n=0
        clrs = []
        ticks = []
        priors = [0.01, 0.08,0.20]
        colors = ['r','b','g']
        alphas = [0.40,0.60,0.80]
        lStyles = ['-','--',':']
        mStyles = ['o','s','^']
        for (i,prior) in enumerate(priors):
            percent  = 100*prior

            epidemicWeeks,pis = computePisAndWeeks(dynamic,prior,season2Models[season])
            n+=1./len(priors)
            ticks.append(n)

            xs,ys = helpers.project_sequence(pis)
            ax=tax.ax

            if r==1 and c == 2:
                ax.plot(-1,-1,'{:s}{:s}'.format(colors[i],mStyles[i]),label='prior = {:.2f}'.format(prior),alpha=alphas[i])
            arrowplot(axes=ax,x=list(xs),y=list(ys), color=colors[i], mutateSize=1., nArrs= 0.10*(len(xs)-1), markerStyle=mStyles[i],LS='-',alpha=alphas[i] )
            
        even = [1./21,1./21,1*(1.-2./21)]
        tax.scatter([even],marker='p',color='black', label = 'Equal Weighting',s=20.0,facecolors='none')

        epidemicWeeks,staticPi = computePisAndWeeks(static,0.01,season2Models[season])
        tax.scatter([staticPi[-1]],marker='X',color='black', label = 'Static MLE', s=20.0,facecolors='none')

        tax.ax.set_aspect('equal', adjustable='box')
        
        fontsize=5
        ax=tax.get_axes()
        ax.text(0.5,-0.05
                    ,'Heaviest model weight'
                    , transform=ax.transAxes
                    ,ha='center'
                    ,va='center'
                    , fontsize=fontsize)

        ax.text(0.825,0.625
                    ,'2nd heaviest model weight'
                    , transform=ax.transAxes
                    ,ha='center'
                    ,va='center'
                    ,rotation=-60
                    , fontsize=fontsize)

        ax.text(0.175,0.625
                    ,'Sum of remaining weights'
                    , transform=ax.transAxes
                    ,ha='center'
                    ,va='center'
                    ,rotation=60
                    , fontsize=fontsize)
        tax._redraw_labels()
        
        if r==1 and c == 2:
            handles, labels = ax.get_legend_handles_labels()
            tax.legend(handles,labels
                       ,frameon=False
                       , bbox_to_anchor = [1.80,0.5]
                       , loc='center'
                       , ncol=1
                       , fontsize=6)
        
        tax.clear_matplotlib_ticks()
        sns.despine(left=True,top=True,bottom=True,right=True)
        
        if c == 3:
            c=0
            r+=1
        else:
            c+=1
        
        plt.subplots_adjust(hspace=0.0, wspace=0.2)
                
    plt.savefig("fig7_setOfTriplots.pdf")
    plt.savefig("fig7_setOfTriplots.png")
    plt.savefig("fig7_setOfTriplots.eps")
    plt.close()
