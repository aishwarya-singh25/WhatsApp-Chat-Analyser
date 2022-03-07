#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import string
import nltk
nltk.data.path.append('/Users/stlp/Downloads/')
nltk.download('stopwords')
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

def nltk_sentiment(sentence):
    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(sentence)
    return score
      
    #Function to judge whether a sentence is positive,negative or neutral in tone
def getResult(pos, neu, neg):
    if (pos > neu and pos > neg):
        return ("Positive")
    elif (neg > neu and neg > pos):
        return ("Negative")
    else:
        return('Neutral')

def sentiment_author(name,sentences,output_df):
    
    lstLines = sent_tokenize(sentences) #tokenize sentences
    lstLines = [t.lower() for t in lstLines]
    #Remove all the punctuations; 3rd argument in maketrans means it is mapped to None
    lstLines = [t.translate(str.maketrans('','',string.punctuation)) for t in lstLines]
    SenScores = [nltk_sentiment(t) for t in lstLines]
    
    # create temp dataframe
    df_temp = pd.DataFrame(lstLines, columns=['Lines'])
    df_temp['Pos']=[t['pos'] for t in SenScores]
    df_temp['Neu']=[t['neu'] for t in SenScores]
    df_temp['Neg']=[t['neg'] for t in SenScores]
    
    output_df['Pos'][output_df['Author']==name] = df_temp['Pos'].mean()
    output_df['Neu'][output_df['Author']==name] = df_temp['Neu'].mean()
    output_df['Neg'][output_df['Author']==name] = df_temp['Neg'].mean() 
    
    return output_df

