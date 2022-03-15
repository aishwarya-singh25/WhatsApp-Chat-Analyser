#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import string
import nltk
import pandas as pd
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.data.path.append('/Users/stlp/Downloads/')
nltk.download('stopwords')
nltk.download('vader_lexicon')


def nltk_sentiment(sentence):
    """
    To check the number of positive, negative and neutral words in the sentence

    Parameters:
    sentence (string): The message for which we need to generate sentiment

    Returns:
    pos, neg, neu (int) : The number of positive, negative and neutral words in the sentence

    """
    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(sentence)
    return score


# Function to judge whether a sentence is positive,negative or neutral in tone
def getResult(pos, neu, neg):
    """
    To check the overall sentiment of the sentence

    Parameters:
    pos, neg, neu (int) : The output from nltk_sentiment

    Returns:
    int: The overall sentiment of the sentence

    """
    if (pos > neu and pos > neg):
        return ("Positive")
    elif (neg > neu and neg > pos):
        return ("Negative")
    else:
        return('Neutral')


def sentiment_author(name, sentences, output_df):
    """
    To check the sentiment of each author

    Parameters:
    name (string) : The name of the author
    sentences (string) : Concatenated message from that author
    output_df (dataframe) : A pandas dataframe containing 

    Returns:
    int: The number of positive, negative and neutral words sent by that author

    """
   
    lstLines = sent_tokenize(sentences)  # tokenize sentences
    lstLines = [t.lower() for t in lstLines]
# Remove all the punctuations; 3rd argument in maketrans means it is mapped to None
    lstLines = [t.translate(str.maketrans('', '', string.punctuation)) for t in lstLines]
    SenScores = [nltk_sentiment(t) for t in lstLines]
  
    # create temp dataframe
    df_temp = pd.DataFrame(lstLines, columns=['Lines'])
    df_temp['Pos'] = [t['pos'] for t in SenScores]
    df_temp['Neu'] = [t['neu'] for t in SenScores]
    df_temp['Neg'] = [t['neg'] for t in SenScores]
 
    output_df['Pos'][output_df['Author'] == name] = df_temp['Pos'].mean()
    output_df['Neu'][output_df['Author'] == name] = df_temp['Neu'].mean()
    output_df['Neg'][output_df['Author'] == name] = df_temp['Neg'].mean()

    return output_df