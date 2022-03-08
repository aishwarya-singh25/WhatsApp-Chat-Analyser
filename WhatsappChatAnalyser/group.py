import pandas as pd
import datetime
import re
import numpy as np
import emoji
import nltk
from WhatsappChatAnalyser import whatsapp_chat_sentiment as wcs
nltk.data.path.append('/Users/stlp/Downloads/')
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from WhatsappChatAnalyser import whatsapp_chat_visualizer as wcv
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
    self.daysInGroup=(group_info[1]-group_info[0]+datetime.timedelta(days=1))
    return self.daysInGroup

  def get_stats(self,df):
    #leftjoin all data gathered
    Start_date,Last_date=self.get_startDate_endDate(df)
    Letter_count,Word_count=self.get_letters_words(df)
    author_buffer_details={'Days_texted': self.get_number_activeDays(df),'Start_date':Start_date,'Last_date':Last_date,'Letter_count':Letter_count,
    'Word_count':Word_count
    ,'Media_shared':self.get_number_mediasShared(df),'Messages_texted':self.get_number_textMessages(df),
    'Messages_Deleted':self.get_number_deletedMessges(df),'daysInGroup':self.get_number_daysInGroup(df)}
    #columns=['Days_texted','Start_date','Last_date','Letter_count','Word_count','Media_shared','Messages_texted','Messages_Deleted','daysInGroup']
    return pd.DataFrame(data=author_buffer_details,index=[0])

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

  def get_text_info(self,extra_StopWords=[],wordCloud=False):
    list=[self.name,self.Message],
    df=pd.DataFrame({'Author':self.name,'Message':self.Message},index=[0])
    author_buffer_details = A.Author().get_text_info(df,extra_StopWords=[],wordCloud=False)
    return author_buffer_details  
