import matplotlib.pyplot as plt
import numpy as np
from IPython.display import set_matplotlib_formats
import seaborn as sns
from wordcloud import WordCloud
from PIL import Image
sns.set(style='darkgrid')


def bar_plot(df, title=None, max=None, sort=False):
    """
    To create a bar plot to display results
    
    Paraneters:
    df (datafrane) : dataframe with dimension :,2
    Title (String) : Title of the bar chart
    max (int) : max number of rows to display
    sort (Boolean) : True means descending
    
    Returns:
    bar chart
    """
    if max == None:
        max_row = len(df)
    else:
        max_row = max
    x_label = str(df.columns[1])
    y_label = str(df.columns[0])
    df = df.sort_values(by=x_label, ascending=sort).head(max_row)
    labels = np.array(df.iloc[:, 0])
    y_pos = np.arange(len(df))
    plt.rcdefaults()
    # reset matplotdefault parameters
    set_matplotlib_formats('retina', quality=100)
    # increase the resolution of the plot
    fig, axes = plt.subplots()
    # use artist layer of matplotlib to create beautiful charts
    plt.rcParams['figure.figsize'] = (8, 5)
    fig.tight_layout()
    bars = axes.barh(y_pos, width=df.iloc[:, 1],
                     height=0.8, color='rebeccapurple')
    axes.set_yticks(y_pos)
    axes.set_yticklabels(labels)
    axes.set_xlabel(x_label)
    axes.set_ylabel(y_label)
    axes.set_title(title)
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
    axes.set_axisbelow(True)
    # Set whether axis ticks and gridlines are above or below most artists.
    axes.yaxis.grid(False)
    axes.xaxis.grid(True, color='#EEEEEE')
    # Grab the color of the bars so we can make the
    for i, v in enumerate(df.iloc[:, 1]):
        # print(str(i)+" "+str(v))
        axes.text(v + v / 100, i, str(v), color=bars[0].get_facecolor(), fontweight='bold')
    plt.show()



def pie(df, title=None, max=None, sort=False):
    """
    To create a pie chart to display results
    
    Paraneters:
    df (datafrane) : dataframe with dimension :,2
    Title (String) : Title of the pie chart
    max (int) : max number of rows to display
    sort (Boolean) : True means descending
    
    Returns:
    Pie chart
    """
    if max == None:
        max_row = len(df)
    else:
        max_row = max
    explode = np.arange(0, max_row * 0.1, 0.1)
    x_label = str(df.columns[1])
    y_label = str(df.columns[0])
    df = df.sort_values(by=x_label, ascending=sort).head(max_row)
    labels = np.array(df.iloc[:, 0])
    sizes = df.iloc[:, 1]
    # only "explode" the 2nd slice (i.e. 'Hogs')
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels,
            autopct='%1.1f%%',startangle=90)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis('equal')
    plt.tight_layout()
    ax1.set_title(title, pad=25)
    plt.show()


def transform_format(val):
    """
    Transform the wine mask to generate white background
    
    """
    if val == 0:
        return 255
    else:
        return val


def wordCloud(WordsFreqdf, maskpath=None):
    """
    To create a wordclous
    
    Paraneters:
    WordsFreqdf (datafrane) : dataframe with dimension :,2
    maskpath (String) : path of masking image
    
    
    Returns:
    Wordcloud
    """
    # prepare data to generate word_cloud
    transformed_comment_mask = None
    if maskpath != None:
        comment_mask = np.array(Image.open(maskpath))
        # download a wine mask
        transformed_comment_mask = np.ndarray((comment_mask.shape[0],
                                               comment_mask.shape[1]), np.int32)
        # instantiate a new transformed with same size as the original one
        for i in range(len(comment_mask)):
            transformed_comment_mask[i] = list(map(transform_format,
                                                   comment_mask[i]))

    d = {'NA': 1}  # initial dictionary with NA
    for a, x in WordsFreqdf[0:20].values:
        d[a] = x

    # Use generate_word_cloud_from_frequency function
    wordcloud = WordCloud(width=1000, height=1000,
                          background_color='white',
                          mask=transformed_comment_mask,
                          # stopwords = stop,
                          min_font_size=25, contour_width=3,
                          contour_color='firebrick').generate_from_frequencies(d)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()
