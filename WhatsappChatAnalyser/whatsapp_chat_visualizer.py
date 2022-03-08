# create functions for data visualization of whatsapp chats

# Importing Required Libraries
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import set_matplotlib_formats
import seaborn as sns
sns.set(style='darkgrid')
from wordcloud import WordCloud
from PIL import Image

#create a bar plot to display number of messages by each person
def bar_plot(df,title = None, max = None, sort = False): 
    if max == None:
        max_row = len(df)
    else:
        max_row=max
        
    x_label = str(df.columns[1])
    y_label = str(df.columns[0])
    df = df.sort_values(by=x_label,ascending=sort).head(max_row)
    labels = np.array(df.iloc[:,0])
    y_pos = np.arange(len(df))
    plt.rcdefaults() # reset matplotdefault parameters
    set_matplotlib_formats('retina', quality = 100)# increase the resolution of the plot
    fig,axes = plt.subplots() # use artist layer of matplotlib to create beautiful charts
    plt.rcParams['figure.figsize'] = (8, 5)
    fig.tight_layout()
    bars = axes.barh(y_pos,width = df.iloc[:,1],height = 0.8,color = 'rebeccapurple')
    
    # setting axis labels and title
    axes.set_yticks(y_pos)
    axes.set_yticklabels(labels)
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)
    axes.set_title(title)
    
    # Removing top, right and left spines
    axes.spines['top'].set_visible(False)
    axes.spines['right'].set_visible(False)
    axes.spines['left'].set_visible(False)
    axes.spines['bottom'].set_color('dimgray') # setting bottom spine gray
    axes.tick_params(bottom = False, left = False) # Removing the ticks
    
    # Adding a horizontal grid
    axes.set_axisbelow(True)
    axes.yaxis.grid(False)
    axes.xaxis.grid(True, color = '#EEEEEE')
    
    for i, v in enumerate(df.iloc[:,1]):
        axes.text(v + v/100, i , str(v), color=bars[0].get_facecolor(), fontweight='bold')
    plt.show()
<<<<<<< HEAD


#create a pie chart
=======
#Take dataframe with dimension :,2,explode: array length should be equal to max
# title: title of the chart,max: max number of rows to display,sort: True means descending
>>>>>>> fcbe6f4145ae43104ba30f3ad00f00804595adcf
def pie(df,explode,title=None,max=None,sort=False):
    if max==None:
        max_row=len(df)
    else:
        max_row=max
        
    x_label= str(df.columns[1])
    y_label= str(df.columns[0])
    df=df.sort_values(by=x_label,ascending=sort).head(max_row)
    labels = np.array(df.iloc[:,0])
    sizes = df.iloc[:,1]
    # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,explode=explode, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio to ensure pie is a circle
    plt.tight_layout()
    ax1.set_title(title,pad=25)
    plt.show()
    
# transform the wine mask to generate white background
def transform_format(val):
    if val == 0:
        return 255
    else:
        return val

# building a word cloud
def wordCloud(WordsFreqdf,maskpath=None):
    #prepare data to generate word_cloud
    #comment_mask = np.array(Image.open(maskpath))#download a wine mask
    #transformed_comment_mask = np.ndarray((comment_mask.shape[0],comment_mask.shape[1]), np.int32)#instantiate a new transformed with same size as the original one
    #for i in range(len(comment_mask)):
    #   transformed_comment_mask[i] = list(map(transform_format, comment_mask[i]))
    
    d = {'NA':1} #initial dictionary with NA
    for a, x in WordsFreqdf[0:20].values:
        d[a] = x

    #Use generate_word_cloud_from_frequency function  
    wordcloud = WordCloud(width = 1000, height = 1000, 
                background_color ='white', 
                #stopwords = stop, 
                min_font_size = 25, contour_width=3, contour_color='firebrick').generate_from_frequencies(d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
