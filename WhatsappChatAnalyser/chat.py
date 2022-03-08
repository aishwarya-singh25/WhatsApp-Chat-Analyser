import pandas as pd
import datetime
import re
import numpy as np
import emoji
import nltk
import sentiment
nltk.data.path.append('/Users/stlp/Downloads/')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import whatsapp_chat_visualizer as wcv
maskpath='/Users/stlp/Downloads/wordcloud trump.png'
class Chat:
  def __init__(self,message=None,name=None):
    self.message = message
    self.name = name

  def update_info(self,df):
    self.name = df['Author'].unique()
    self.Message = df['Message'].unique()

  #Remove stopWords and text coming from different sources
  def clean_text(self,message,extra_StopWords):

    stop = stopwords.words('english')
    stop = stop + extra_StopWords
    #following set of codes are used to clean texts coming from different sources like html etc.
    msgbuffer = message.encode('ascii', 'ignore').decode('ascii')
    msgbuffer = re.sub(r'[`!?~@#$%^&*()_+-=<>,.:;]', '', msgbuffer)
    msgbuffer = re.sub(r'[–]', '', msgbuffer)
    msgbuffer = re.sub(r'[\[\]\(\)\{\}]', '', msgbuffer)
    msgbuffer = re.sub(r'[\t\"\'\/\\]', '', msgbuffer)
    lstAllWords = msgbuffer.split()

  #Remove those words which have a length less than or equal to 2
    lstTmpWords=[]
    for Word in lstAllWords:
        if len(Word)>2 and (Word not in stop):
            lstTmpWords.append(Word)
    lstAllWords = lstTmpWords
    del lstTmpWords

    #convert all the words to lower case
    for i in range(0,len(lstAllWords)):
        lstAllWords[i] = (lstAllWords[i]).lower()
    return ' '.join(lstAllWords) 

  def get_text_info(self, df,extra_StopWords,wordCloud=False):
    
    self.update_info(df)
    #author_buffer_details=pd.DataFrame(data=self.name,columns=['Author'])
    dstr_grp=''
    dlist_grp=[]
    df['avgWordspermessage'] = 0
    df['minWordspermessage'] = 0
    df['maxWordspermessage'] = 0
    df['emovocab'] = 0
    df['totalemojis'] = 0
    df['top5emojis'] = 0
    df['vocab'] = 0
    df['top5words'] = 0
    df['words']=0
    df['Neg']=0
    df['Pos']=0
    df['Neu']=0
    for name in df['Author'].unique():
      data1 = df[df['Author']==name]
      dstr = ' '.join(data1['Message'])# create a single string containing all the words from all the messages
      dlist = data1['Message'].to_list()# convert the df column into a list
      dstr_grp=dstr_grp+dstr
      #names['avgTime'][names['Name']==name] = data1['Time'].mean().strftime("%I:%M %p")

      NW = []#blank list to store no. of words in a message
      for n in dlist:
        NW.append(len(n.split()))#store number of words in each message

      df['avgWordspermessage'][df['Author']==name] = np.mean(NW)#mean of length of all words
      df['minWordspermessage'][df['Author']==name] = np.min(NW)#min number of words
      df['maxWordspermessage'][df['Author']==name] = np.max(NW)#max number of words

      NE = []#blank list to store emojis
      NE = [e for e in dstr if e in emoji.UNICODE_EMOJI]
      dfE = pd.DataFrame({'Emoji':NE})
      EmoFreqdf = pd.DataFrame(dfE.groupby(['Emoji'])['Emoji'].count())
      EmoFreqdf.columns = ['Freq']
      EmoFreqdf = EmoFreqdf.reset_index()
      EmoFreqdf.columns = ['Emoji','Freq']
      df['emovocab'][df['Author']==name] = len(EmoFreqdf)#store total number of unique emojis used
      df['totalemojis'][df['Author']==name] = EmoFreqdf['Freq'].sum()#store total number of emojis sent
      EmoFreqdf = EmoFreqdf.sort_values('Freq',ascending=False)
      df['top5emojis'][df['Author']==name] = ' '.join(EmoFreqdf['Emoji'][0:5])#store top 5 emojis

      lstAllWords=self.clean_text(dstr,extra_StopWords).split()

      #remove those words which are in stop and emojis
      Words_df = pd.DataFrame({'Words':lstAllWords})
      Words_df = Words_df[-Words_df['Words'].isin(emoji.UNICODE_EMOJI.keys())]
      WordsFreqdf = pd.DataFrame(Words_df.groupby(['Words'])['Words'].count())
      WordsFreqdf.columns = ['Freq']
      WordsFreqdf = WordsFreqdf.reset_index()
      WordsFreqdf.columns = ['Word','Freq']
      df['vocab'][df['Author']==name] = len(WordsFreqdf)#total number of unique words
      WordsFreqdf = WordsFreqdf.sort_values('Freq',ascending=False)
      df['top5words'][df['Author']==name] = ' '.join(WordsFreqdf['Word'][0:5])#Top 5 words
      df['words'][df['Author']==name] = ' '.join(WordsFreqdf['Word'][0:])#All words
      df = Sentiment.sentiment_author(name,dstr,df)
      if wordCloud== True:
            #print("start ", name, " end")
            print('\U0001F923'+name)
            wcv.wordCloud(WordsFreqdf,maskpath)

    author_buffer_details=pd.DataFrame(data=self.name,columns=['Author'])
    author_buffer_details=author_buffer_details.merge(df[['Author','avgWordspermessage','minWordspermessage',
    'maxWordspermessage','emovocab','totalemojis','top5emojis','vocab','top5words','words','Pos', 'Neg', 'Neu']].drop_duplicates(),on='Author',how='left')
    return author_buffer_details    
