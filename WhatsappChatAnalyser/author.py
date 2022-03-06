import pandas as pd
import datetime
import re
import numpy as np
import emoji
import chat
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class Author:
  def __init__(self, name=None, Date=None , Time=None , Message=None ,Hours=None):
    self.name = name
    self.Date = Date
    self.Time = Time
    self.Message = Message
    self.Hours = Hours

  # Update the attributes of the class using the dataframe created from text file
  def update_info(self,df):
    self.name = df['Author'].unique()
    self.Date = df['Date'].unique()
    self.Time = df['Time'].unique()
    self.Message = df['Message'].unique()
    self.Hours = df['Hours'].unique()
    
  #Remove authors with None value which could be because of some activities in the group like deleting a text or updating group description
  def remove_null_authors(self,df):
    null_authors=df[df['Author'].isnull()]
    df_new= df.drop(null_authors.index)
    return df_new

   #Find the most talkative person in the group 
  def get_number_textMessages(self,df):
    author_talkative=df['Author'].value_counts().sort_values(ascending=True)#count no. of messages per author
    author_talkative_df=pd.DataFrame({'Author':author_talkative.index,'Messages_texted':author_talkative})
    return author_talkative_df

  #Find no. of medias shared by each individual i.e spammer
  def get_number_mediasShared(self,df):
    media_messages = df[df['Message'] == '<Media omitted>']
    author_media_messages_value_counts = media_messages['Author'].value_counts().sort_values(ascending=True)
    author_media_messages_value_counts_df=pd.DataFrame({'Author':author_media_messages_value_counts.index,'Media_shared':author_media_messages_value_counts})
    return author_media_messages_value_counts_df

  #Find the most confused individual of the group
  def get_number_deletedMessges(self,df):
    deleted_messages_df=df[df['Message']=='You deleted this message']
    deleted_messages_df=deleted_messages_df.append(df[df['Message']=='This message was deleted'])
    deleted_messages_counts=deleted_messages_df['Author'].value_counts().sort_values(ascending=True)
    deleted_messages_counts_df=pd.DataFrame({'Author':deleted_messages_counts.index,'Messages_Deleted':deleted_messages_counts})
    return deleted_messages_counts_df

  #Group by Authors total no. of letters & total no. of words
  def get_letters_words(self,df):
    df['Letter_count']=df['Message'].apply(lambda s:len(s))
    df['Word_count']=df['Message'].apply(lambda s:len(s.split(' ')))
    group_df=df.groupby(['Author'])['Letter_count','Word_count'].sum().sort_values(by=['Word_count','Letter_count'],ascending=False)
    group_df.columns=['Letter_count','Word_count']
    return group_df

  def get_startDate_endDate(self,df):
    author_min_date=pd.DataFrame(df.groupby('Author')['Date'].min())#Find the first date of texting by the individual
    author_max_date=pd.DataFrame(df.groupby('Author')['Date'].max())#Find the last date of texting by the individual
    author_info=author_min_date.merge(author_max_date,on='Author', how='left')
    author_info.rename(columns={'Date_x':'Start_date','Date_y':'Last_date'},inplace=True)
    return author_info

  #No. of active days in the group
  def get_number_activeDays(self,df):
    df_days_texted=pd.DataFrame(df.groupby('Author')['Date'].nunique()).rename(columns={'Date':'Days_texted'})
    return df_days_texted

  #No. of days in the group
  def get_number_daysInGroup(self,df):
    author_info=self.get_startDate_endDate(df)
    author_info['Date_diff']=(author_info['Last_date']-author_info['Start_date']+datetime.timedelta(days=1)).dt.days.astype(int)
    df_daysInGroup=author_info.drop(['Last_date','Start_date'],axis=1).rename(columns={'Date_diff':'daysInGroup'})
    return df_daysInGroup

  def get_author_text_info(self, df,extra_StopWords):
    author_buffer_details=chat.Chat().text_info(self, df,extra_StopWords)
    return author_buffer_details


  def get_stats(self,df):
    self.update_info(df)
    author_buffer_details=pd.DataFrame(data=self.name,columns=['Author'])
    #leftjoin all data gathered
    author_buffer_details=author_buffer_details.merge(self.get_number_activeDays(df),on='Author',how='left')#No. of active days in the group
    author_buffer_details=author_buffer_details.merge(self.get_startDate_endDate(df),on='Author',how='left')#join first and Last texting date
    author_buffer_details=author_buffer_details.merge(self.get_letters_words(df),on='Author',how='left')#join letters and words count
    author_buffer_details=author_buffer_details.merge(self.get_number_mediasShared(df),on='Author',how='left')# join no. of media messages
    author_buffer_details=author_buffer_details.merge(self.get_number_textMessages(df),on='Author',how='left')#join most talkative data
    author_buffer_details=author_buffer_details.merge(self.get_number_deletedMessges(df),on='Author',how='left')#join deleted message data
    author_buffer_details=author_buffer_details.merge(self.get_number_daysInGroup(df),on='Author',how='left')#No. of days in the group
    return author_buffer_details


  def get_aggressiveness(self,df):
    author_buffer_details= self.get_stats(df)
    print("\033[1m" + "Average number of messages per day for active days" + "\033[0m")
    author_buffer_details['Agressiveness'] = (author_buffer_details['Messages_texted']/author_buffer_details['Days_texted']).round(2)
    return author_buffer_details[['Author','Agressiveness']].sort_values(by='Agressiveness',ascending=False)
   

  def get_consistency(self,df):
    author_buffer_details= self.get_stats(df)
    print("\033[1m" + "Percentage of time texted atleast once since the start date " + "\033[0m")
    author_buffer_details['Consistency'] = (100*author_buffer_details['Days_texted']/author_buffer_details['daysInGroup']).round()
    return author_buffer_details[['Author','Consistency']].sort_values(by='Consistency',ascending=False)

  def get_frequency(self,df):
    author_buffer_details= self.get_stats(df)
    print("\033[1m" + "Number of messages per day on whatsapp since the start date" + "\033[0m")
    author_buffer_details['Frequency'] = ((author_buffer_details['Messages_texted']+author_buffer_details['Media_shared'])/author_buffer_details['daysInGroup'])
    return author_buffer_details[['Author','Frequency']].sort_values(by='Frequency',ascending=False)

  def get_metrics(self,df):
    self.update_info(df)
    author_buffer_details=pd.DataFrame({'Author':self.name})
    print(author_buffer_details)
    #leftjoin all data gathered
    author_buffer_details=author_buffer_details.merge(self.get_consistency(df),on='Author',how='left')#consistency
    author_buffer_details=author_buffer_details.merge(self.get_frequency(df),on='Author',how='left')#Frequency
    author_buffer_details=author_buffer_details.merge(self.get_aggressiveness(df),on='Author',how='left')#Aggressiveness 
    return  author_buffer_details

  


  


  

    
        
      


    
