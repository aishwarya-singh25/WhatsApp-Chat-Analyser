import matplotlib.pyplot as plt
import numpy as np
from IPython.display import set_matplotlib_formats

#Take dataframe with dimension :,1
def bar_plot(df,title=None,max=None,sort=True): #create a bar plot to display results
    if max==None:
        max_row=len(df)
    else:
        max_row=max
    x_label= str(df.columns[1])
    y_label= str(df.columns[0])
    df=df.sort_values(by=x_label,ascending=sort).head(max_row)
    labels=np.array(df.iloc[:,0])
    y_pos=np.arange(len(df))
    plt.rcdefaults() #reset matplotdefault parameters
    set_matplotlib_formats('retina', quality=100)#increase the resolution of the plot
    fig,axes=plt.subplots() #use artist layer of matplotlib to create beautiful charts
    plt.rcParams['figure.figsize'] = (8, 5)
    fig.tight_layout()
    bars=axes.barh(y_pos,width=df.iloc[:,1],height=0.8,color='rebeccapurple')
    axes.set_yticks(y_pos)
    axes.set_yticklabels(labels)
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)
    axes.set_title(title)
    # First, let's remove the top, right and left spines (figure borders)
    # which really aren't necessary for a bar chart.
    # Also, make the bottom spine gray instead of black.
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_color('dimgray')
    # Second, remove the ticks as well.
    axes.tick_params(bottom=False, left=False)
    # Third, add a horizontal grid (but keep the vertical grid hidden).
    # Color the lines a light gray as well.
    axes.set_axisbelow(True)#Set whether axis ticks and gridlines are above or below most artists.
    axes.yaxis.grid(False)
    axes.xaxis.grid(True, color='#EEEEEE')
    # Grab the color of the bars so we can make the
    for i, v in enumerate(df.iloc[:,1]):
        #print(str(i)+" "+str(v))
        axes.text(v + v/100, i , str(v), color=bars[0].get_facecolor(), fontweight='bold')
    plt.show()