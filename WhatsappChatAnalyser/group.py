import datetime
import nltk
import numpy as np
import pandas as pd
from WhatsappChatAnalyser import author as A
import matplotlib.pyplot as plt

nltk.data.path.append('/Users/stlp/Downloads/')
nltk.download('stopwords')
maskpath = 'wordcloud trump.png'


class Group:
    def __init__(self, Name=None,
                 Number_of_Authors=None, 
                 Time=None, Message=None, Hours=None):
        """
        To create a bar plot to display results
        
        Parameters:
        self (class): ??
        Name (Mstring) : Name of auhtor
        Number_of_Authors (int) : No. of authors
        Time (Time) : Time of the message
        Message (string) : Message from the author
        Hours (Time) : ??

        Returns:
        Attributes of the class

        """
        self.Name = Name
        self.Number_of_Authors = Number_of_Authors
        self.Time = Time
        self.Message = Message
        self.Hours = Hours

    def update_info(self, df):
        """ 
        Updates the attributes of class
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        """
        df = self.__remove_null_authors(df)
        dstr = []
        self.name = 'Group'
        self.Number_of_Authors = df['Author'].nunique()
        self.minTime = df['Time'].min()
        self.maxTime = df['Time'].max()
        for msg in df['Message']:
            dstr = dstr + msg.split()
        self.Message = ' '.join(dstr)
        self.minHours = df['Hours'].min()
        self.maxHours = df['Hours'].max()
        self.totalHours = df['Hours'].value_counts()

    # Remove authors with None value which could be because
    # of some activities in the group like deleting a text 
    # or updating group description
    def __remove_null_authors(self, df):
        """
        Remove rows for authors with Null Author valun
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        dataframe: New dataframe with no missing values
        
        """
        null_authors = df[df['Author'].isnull()]
        df_new = df.drop(null_authors.index)
        return df_new

    # Find the most talkative person in the group
    def get_number_textMessages(self, df):
        """
        Calculate the count of text messages
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        int : Count of messages 
        
        """
        author_talkative = A.Author().get_number_textMessages(df)
        self.Messages_texted = author_talkative.Messages_texted.sum()
        return self.Messages_texted

    # Find no. of medias shared in the group
    def get_number_mediasShared(self, df):
        """
        
        Calculate the number of media shared by each author
        
        Parameters:
        df (dataframe): Dataframe created from text file
        
        Returns:
        int : Count of media shared
       """
        author_media_messages_value_counts_df = 
        A.Author().get_number_mediasShared(df)
        self.Media_shared = 
        author_media_messages_value_counts_df.Media_shared.sum()
        return self.Media_shared

    def get_number_deletedMessges(self, df):
        """
        
        Calculate the number of deleted messages
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        int : Count of media shared
        
        """
        deleted_messages_counts_df = 
        A.Author().get_number_deletedMessges(df)
        self.Messages_Deleted = 
        deleted_messages_counts_df.Messages_Deleted.sum()
        return self.Messages_Deleted

    # Total no. of letters & total no. of words
    def get_letters_words(self, df):
        """
        
        Calculate the number of letters and words
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        int: Count of letter and words
        
        """
        group_df = A.Author().get_letters_words(df)
        self.Letter_count = group_df.Letter_count.sum()
        self.Word_count = group_df.Word_count.sum()
        return [self.Letter_count, self.Word_count]

    def get_startDate_endDate(self, df):
        """
        
        Calculate the start date and end date of the chat
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        Date : start date and end date
        
        """
        group_df = A.Author().get_startDate_endDate(df)
        self.Start_date = group_df.Start_date.min()
        self.Last_date = group_df.Last_date.max()
        return [self.Start_date, self.Last_date]

    def get_number_activeDays(self, df):
        """
        
        Calculate the No. of active days in the group
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        int : No. of active days in the group
        
        """
        self.Days_texted = df.Date.nunique()
        return self.Days_texted

    def get_number_daysInGroup(self, df):
        """
        
        Calculate the No. of days in the group
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        int : No. of days in the group
        
        """
        group_info = self.get_startDate_endDate(df)
        self.daysInGroup = (group_info[1] - group_info[0] + 
                            datetime.timedelta(days=1))
        return self.daysInGroup

    def get_stats(self, df):
        """
        
        Leftjoin all data gathered into one dataframe
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        dataframe: New dataframe with no missing values
        
        """
        Start_date, Last_date = self.get_startDate_endDate(df)
        Letter_count, Word_count = self.get_letters_words(df)
        author_buffer_details = {'Days_texted': self.get_number_activeDays(df),
                                 'Start_date': Start_date, 'Last_date': Last_date,
                                 'Letter_count': Letter_count, 'Word_count': Word_count,
                                 'Media_shared': self.get_number_mediasShared(df),
                                 'Messages_texted': self.get_number_textMessages(df),
                                 'Messages_Deleted': self.get_number_deletedMessges(df),
                                 'daysInGroup': self.get_number_daysInGroup(df)}

        Hr_count = self.totalHours
        dfHFreqs = pd.DataFrame({'Hours': Hr_count.index,
                                 'Count': Hr_count})
        dfHFreqs = dfHFreqs.fillna(0)
        # title = 'Group Texting pattern'
        xlabel = 'Time in 24hr format'
        ylabel = 'Percentage of messages exchanged'
        dfHFreqs['Hours'] = dfHFreqs['Hours'].astype(int)
        dfHFreqs.sort_values(by='Hours', ascending=True,
                             inplace=True)
        plt.figure()
        ax = dfHFreqs.iloc[:, 1].plot(legend=True,
                                      figsize=(12, 6), color='r')
        ax.set(xlabel=xlabel, ylabel=ylabel)
        ax.set_xticks(ticks=np.arange(start=0,
                                      stop=24, step=1))
        ax.set_xticklabels(labels=np.array(dfHFreqs['Hours']))
        return pd.DataFrame(data=author_buffer_details,
                            index=[0])

    def get_aggressiveness(self, df):
        """
        
        Calculate average number of messages per day
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        int : Average number of messages per day
        
        """       
        author_buffer_details = self.get_stats(df)
        print("\033[1m" + "Average number of messages per day for active days" + "\033[0m")
        self.Agressiveness = (author_buffer_details['Messages_texted'] / author_buffer_details['Days_texted']).round(2)
        return self.Agressiveness

    def get_consistency(self, df):
        """
        
        Calculate average number of messages per day
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        int : Days texted/ days in group
        
        """
        author_buffer_details = self.get_stats(df)
        print("\033[1m" + "Percentage of time texted atleast once since the start date " + "\033[0m")
        self.Consistency = (100 * author_buffer_details['Days_texted'] / author_buffer_details['daysInGroup']).round()
        return self.Consistency

    def get_frequency(self, df):
        """
        
        Calculate frequency of messages and media
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        int : Frequency of messages and media
        
        """
        author_buffer_details = self.get_stats(df)
        print("\033[1m" + "Number of messages per day on whatsapp since the start date" + "\033[0m")
        self.Frequency = ((author_buffer_details['Messages_texted'] + author_buffer_details['Media_shared']) /
                          author_buffer_details['daysInGroup'])
        return self.Frequency

    def get_metrics(self, df):
        """
        
        Return all the metrices calculated by member functions in a dataframe
        
        Parameters:
        df (dataframe): dataframe created from text file
        
        Returns:
        dataframe : Dataframe with new columns
        
        """
        author_buffer_details = [self.get_consistency(df), self.get_frequency(df), self.get_aggressiveness(df)]
        columns = ['Consistency', 'Frequency', 'Aggressiveness']
        return pd.DataFrame(data=author_buffer_details, columns=columns)

    def get_text_info(self, extra_StopWords=[], wordCloud=False):
        """
        
        ??
        
        Parameters:
        df (dataframe): dataframe created from text file
        extra_StopWords (list): Extra stopwords for NLP
        wordCloud (boolean): Whether to create a wordcloud
        
        Returns:
        dataframe : Dataframe with columns to create wordcloud
        wordcloud
        
        """
        # need to figure out how to add maskpath
        df = pd.DataFrame({'Author': self.name, 'Message': self.Message}, index=[0])
        author_buffer_details = A.Author().get_text_info(df, extra_StopWords, wordCloud)
        return author_buffer_details
