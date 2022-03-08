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
maskpath='wordcloud trump.png'
class Chat:
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
      df = sentiment.sentiment_author(name,dstr,df)
      if wordCloud== True:
            #print("start ", name, " end")
            print('\U0001F923'+name)
            wcv.wordCloud(WordsFreqdf,maskpath)

    author_buffer_details=pd.DataFrame(data=self.name,columns=['Author'])
    author_buffer_details=author_buffer_details.merge(df[['Author','avgWordspermessage','minWordspermessage',
    'maxWordspermessage','emovocab','totalemojis','top5emojis','vocab','top5words','words','Pos', 'Neg', 'Neu']].drop_duplicates(),on='Author',how='left')
    return author_buffer_details  


  


  

    
        
      


    
