import pandas as pd
import datetime
import re
import numpy as np
import emoji
import nltk
import whatsapp_chat_sentiment as Sentiment
nltk.data.path.append('/Users/stlp/Downloads/')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import whatsapp_chat_visualizer as wcv
import author as A
maskpath='wordcloud trump.png'

class Group:
  def __init__(self, Name=None ,Number_of_Authors=None, Time=None , Message=None ,Hours=None):
    self.Name = Name
    self.Number_of_Authors=Number_of_Authors
    self.Time = Time
    self.Message = Message
    self.Hours = Hours

  # Update the attributes of the class using the dataframe created from text file
  def update_info(self,df):
    df= self.__remove_null_authors(df)
    dstr=[]
    self.name = 'Group'
    self.Number_of_Authors = df['Author'].nunique()
    self.minTime = df['Time'].min()
    self.maxTime = df['Time'].max()
    for msg in df['Message']:
        dstr=dstr + msg.split()
    self.Message = ' '.join(dstr)
    self.minHours = df['Hours'].min()
    self.maxHours = df['Hours'].max()
    
  #Remove authors with None value which could be because of some activities in the group like deleting a text or updating group description
  def __remove_null_authors(self,df):
    null_authors=df[df['Author'].isnull()]
    df_new= df.drop(null_authors.index)
    return df_new

   #Find the most talkative person in the group 
  def get_number_textMessages(self,df):
    author_talkative = A.Author().get_number_textMessages(df)
    self.Messages_texted=author_talkative.Messages_texted.sum()
    return self.Messages_texted

  #Find no. of medias shared by each individual i.e spammer
  def get_number_mediasShared(self,df):
    author_media_messages_value_counts_df = A.Author().get_number_mediasShared(df)
    self.Media_shared=author_media_messages_value_counts_df.Media_shared.sum()
    return self.Media_shared

  #Find the most confused individual of the group
  def get_number_deletedMessges(self,df):
    deleted_messages_counts_df = A.Author().get_number_deletedMessges(df)
    self.Messages_Deleted=deleted_messages_counts_df.Messages_Deleted.sum()
    return self.Messages_Deleted

  #Group by Authors total no. of letters & total no. of words
  def get_letters_words(self,df):
    group_df = A.Author().get_letters_words(df)
    self.Letter_count=group_df.Letter_count.sum()
    self.Word_count=group_df.Word_count.sum()
    return [self.Letter_count,self.Word_count]


  def get_startDate_endDate(self,df):
    group_df = A.Author().get_startDate_endDate(df)
    self.Start_date=group_df.Start_date.min()
    self.Last_date=group_df.Last_date.max()
    return [self.Start_date,self.Last_date]  

  #No. of active days in the group
  def get_number_activeDays(self,df):
    self.Days_texted=df.Date.nunique()
    return self.Days_texted

  #No. of days in the group
  def get_number_daysInGroup(self,df):
    group_info=self.get_startDate_endDate(df)
    self.daysInGroup=group_info[1]-group_info[1]+1
    return self.daysInGroup

  def get_stats(self,df):
    #leftjoin all data gathered
    Start_date,Last_date=self.get_startDate_endDate(df)
    Letter_count,Word_count=self.get_letters_words(df)
    author_buffer_details=[self.get_number_activeDays(df),Start_date,Last_date,Letter_count,Word_count
    ,self.get_number_mediasShared(df),self.get_number_textMessages(df),
    self.get_number_deletedMessges(df),self.get_number_daysInGroup(df)]
    columns=['Days_texted','Start_date','Last_date','Letter_count','Word_count','Media_shared','Messages_texted','Messages_Deleted','daysInGroup']
    return pd.DataFrame(data=author_buffer_details,columns=columns)

  def get_aggressiveness(self,df):
    author_buffer_details= self.get_stats(df)
    print("\033[1m" + "Average number of messages per day for active days" + "\033[0m")
    self.Agressiveness = (author_buffer_details['Messages_texted']/author_buffer_details['Days_texted']).round(2)
    return self.Agressiveness
   

  def get_consistency(self,df):
    author_buffer_details= self.get_stats(df)
    print("\033[1m" + "Percentage of time texted atleast once since the start date " + "\033[0m")
    self.Consistency = (100*author_buffer_details['Days_texted']/author_buffer_details['daysInGroup']).round()
    return self.Consistency

  def get_frequency(self,df):
    author_buffer_details= self.get_stats(df)
    print("\033[1m" + "Number of messages per day on whatsapp since the start date" + "\033[0m")
    self.Frequency = ((author_buffer_details['Messages_texted']+author_buffer_details['Media_shared'])/author_buffer_details['daysInGroup'])
    return self.Frequency

  def get_metrics(self,df):
    author_buffer_details=[self.get_consistency(df),self.get_frequency(df),self.get_aggressiveness(df)]
    columns=['Consistency','Frequency','Agressiveness']
    return pd.DataFrame(data=author_buffer_details,columns=columns)

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
