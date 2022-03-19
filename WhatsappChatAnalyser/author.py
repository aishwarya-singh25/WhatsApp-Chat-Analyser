# importing required libraries
import pandas as pd
import numpy as np
import datetime
import re
import emoji
import nltk
import whatsapp_chat_sentiment as wcs
import whatsapp_chat_visualizer as wcv
from nltk.corpus import stopwords
nltk.data.path.append('/Users/stlp/Downloads/')
nltk.download('stopwords')


class Author:
    def __init__(self, name=None, Date=None, Time=None, Message=None, Hours=None):
        self.name = name
        self.Date = Date
        self.Time = Time
        self.Message = Message
        self.Hours = Hours

    # Update attributes of class using dataframe created from text file
    def update_info(self, df):
        """ Updates the attributes of class

        Parameters:
        df (dataframe): dataframe created from text file

       """
        df = self.__remove_null_authors(df)
        self.name = df['Author']
        self.Date = df['Date']
        self.Time = df['Time']
        self.Message = df['Message']
        self.Hours = df['Hours']

    # Remove authors with None value
    # This is a private method which will remove null authors from every method
    def __remove_null_authors(self, df):
        """Remove rows for authors with None in the message column

        Parameters:
        df (dataframe):  dataframe created from text file

        Returns:
        dataframe:Returning new dataframe with no missing values

       """
        null_authors = df[df['Author'].isnull()]
        df_new = df.drop(null_authors.index)
        return df_new

    # Find the most talkative person in the group
    def get_number_textMessages(self, df):
        """Calculate the count of text messages for each author

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning dataframe with count of messages per author

       """
        df = self.__remove_null_authors(df)
        # count no. of messages per author
        author_talkative = df['Author'].value_counts().sort_values(ascending=True)
        author_talkative_df = pd.DataFrame({'Author': author_talkative.index, 'Messages_texted': author_talkative})
        return author_talkative_df

    # Find no. of medias shared by each individual i.e spammer
    def get_number_mediasShared(self, df):
        """Calculate the number of media shared by each author

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning dataframe with count of media shared per author

       """
        df = self.__remove_null_authors(df)
        media_messages = df[df['Message'] == '<Media omitted>']
        author_media_messages_value_counts = media_messages['Author'].value_counts().sort_values(ascending=True)
        author_media_messages_value_counts_df = pd.DataFrame({'Author': author_media_messages_value_counts.index, 'Media_shared': author_media_messages_value_counts})
        return author_media_messages_value_counts_df

    # Find the most confused individual of the group
    def get_number_deletedMessges(self, df):
        """Calculate the number of deleted messages

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning dataframe with count of media shared per author

        """
        df = self.__remove_null_authors(df)
        deleted_messages_df = df[df['Message'] == 'You deleted this message']
        deleted_messages_df = deleted_messages_df.append(df[df['Message'] == 'This message was deleted'])
        deleted_messages_counts = deleted_messages_df['Author'].value_counts().sort_values(ascending=True)
        deleted_messages_counts_df = pd.DataFrame({'Author': deleted_messages_counts.index, 'Messages_Deleted': deleted_messages_counts})
        return deleted_messages_counts_df

    # Group by Authors total no. of letters & total no. of words
    def get_letters_words(self, df):
        """Calculate number of words and letters per author

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning dataframe with no letter count and word count columns

        """
        df = self.__remove_null_authors(df)
        df['Letter_count'] = df['Message'].apply(lambda s: len(s))
        df['Word_count'] = df['Message'].apply(lambda s: len(s.split(' ')))
        group_df = df.groupby(['Author'])['Letter_count', 'Word_count'].sum().sort_values(by=['Word_count', 'Letter_count'], ascending=False)
        group_df.columns = ['Letter_count', 'Word_count']
        return group_df

    # Get start and end date of authors
    def get_startDate_endDate(self, df):
        """Function to identify the start and end date for the author

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning start and end date for authors

        """
        df = self.__remove_null_authors(df)
        # Find the first date of texting by the individual
        author_min_date = pd.DataFrame(df.groupby('Author')['Date'].min())
        # Find the last date of texting by the individual
        author_max_date = pd.DataFrame(df.groupby('Author')['Date'].max())
        author_info = author_min_date.merge(author_max_date, on='Author', how='left')
        author_info.rename(columns={'Date_x': 'Start_date', 'Date_y': 'Last_date'}, inplace=True)
        return author_info

    # No. of active days in the group
    def get_number_activeDays(self, df):
        """Function to calculate the number of active days for each author

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning dataframe with author names and number of days texted

        """
        df = self.__remove_null_authors(df)
        df_days_texted = pd.DataFrame(df.groupby('Author')['Date'].nunique()).rename(columns={'Date': 'Days_texted'})
        return df_days_texted

    def get_stats(self, df):
        """Calculating the overall statistics at the author level

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning dataframe with author names and details
        including start and end date, number of active days, number of letters
        used, count of media files shared, count of messages send and delted

        """
        df = self.__remove_null_authors(df)
        # Left join all the data gathered
        author_buffer_details = pd.DataFrame(data=df.Author.unique(), columns=['Author'])
        # No. of active days in the group
        author_buffer_details = author_buffer_details.merge(self.get_number_activeDays(df), on='Author', how='left')
        # join first and Last texting date
        author_buffer_details = author_buffer_details.merge(self.get_startDate_endDate(df), on='Author', how='left')
        # join letters and words count
        author_buffer_details = author_buffer_details.merge(self.get_letters_words(df), on='Author', how='left')
        # join no. of media messages
        author_buffer_details = author_buffer_details.merge(self.get_number_mediasShared(df), on='Author', how='left')
        # join most talkative data
        author_buffer_details = author_buffer_details.merge(self.get_number_textMessages(df), on='Author', how='left')
        # join deleted message data
        author_buffer_details = author_buffer_details.merge(self.get_number_deletedMessges(df), on='Author', how='left')
        author_buffer_details.fillna(0, inplace=True)
        return author_buffer_details

    def get_aggressiveness(self, df):
        """Function to calculate the aggressiveness score using the
        number of messages sent and number of active days

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning sorted dataframe with author names aggressiveness score

        """
        df = self.__remove_null_authors(df)
        author_buffer_details = self.get_stats(df)
        print("\033[1m" + "Average number of messages per day for active days" + "\033[0m")
        author_buffer_details['Aggressiveness'] = (author_buffer_details['Messages_texted']/author_buffer_details['Days_texted']).round(2)
        return author_buffer_details[['Author', 'Aggressiveness']].sort_values(by='Aggressiveness', ascending=False)

    def get_frequency(self, df):
        """Function to calculate the number of messages sent
        per day since the start day of the author in chat or group

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning dataframe with author names and frequency

        """
        df = self.__remove_null_authors(df)
        author_buffer_details = self.get_stats(df)
        print("\033[1m" + "Number of messages per day on whatsapp since the start date" + "\033[0m")
        author_buffer_details['Frequency'] = ((author_buffer_details['Messages_texted'] + author_buffer_details['Media_shared'])/author_buffer_details['daysInGroup'])
        return author_buffer_details[['Author', 'Frequency']].sort_values(by='Frequency', ascending=False)

    # leftjoin all data gathered
    def get_metrics(self, df):
        """Building a dataframe with frquency and aggressiveness score of authors

        Parameters:
        df (dataframe): Cleaned dataframe created from text file

        Returns:
        dataframe: Returning dataframe with author names, frequency and aggressivenss

        """
        df = self.__remove_null_authors(df)
        author_buffer_details = pd.DataFrame(data=df.Author.unique(), columns=['Author'])
        # Frequency
        author_buffer_details = author_buffer_details.merge(self.get_frequency(df), on='Author', how='left')
        # Aggressiveness
        author_buffer_details = author_buffer_details.merge(self.get_aggressiveness(df), on='Author', how='left')
        return author_buffer_details

    # Remove stopwords and text coming from different sources
    def __clean_text(self, message, extra_StopWords):
        stop = stopwords.words('english')
        stop = stop + extra_StopWords
        # following set of codes are used to clean texts coming from different sources like html etc.
        msgbuffer = message.encode('ascii', 'ignore').decode('ascii')
        msgbuffer = re.sub(r'[`!?~@#$%^&*()_+-=<>,.:;]', '', msgbuffer)
        msgbuffer = re.sub(r'[–]', '', msgbuffer)
        msgbuffer = re.sub(r'[\[\]\(\)\{\}]', '', msgbuffer)
        msgbuffer = re.sub(r'[\t\"\'\/\\]', '', msgbuffer)
        lstAllWords = msgbuffer.split()

        # Remove those words which have a length less than or equal to 2
        lstTmpWords = []
        for Word in lstAllWords:
            if len(Word) > 2 and (Word not in stop):
                lstTmpWords.append(Word)
        lstAllWords = lstTmpWords
        del lstTmpWords

        # convert all the words to lower case
        for i in range(0, len(lstAllWords)):
            lstAllWords[i] = (lstAllWords[i]).lower()
        return ' '.join(lstAllWords)

    def get_text_info(self, df, extra_StopWords=[], wordCloud=None, maskpath=None):
        """Populating metrics, sentiments and wordcloud at the author level

        Parameters:
        df (dataframe): Cleaned dataframe created from text file
        extra_StopWords (list): (Optional) list of additional stopwords
        wordcloud (boolean): defualt = None, set True to generate wordcloud
        maskpath: setting mask for wordcloud

        Returns:
        dataframe: Returning dataframe with author names and details
        including, average words per message, min and max words per message,
        total emojis, top 5 emojis, vocab, top 5 words, Positive, negative and
        neutral sentiment. Returns optional wordcloud if wordCloud set to True
        """
        df = self.__remove_null_authors(df)
        # author_buffer_details=pd.DataFrame(data=self.name,columns=['Author'])
        dstr_grp = ''
        # dlist_grp = []
        df['avgWordspermessage'] = 0
        df['minWordspermessage'] = 0
        df['maxWordspermessage'] = 0
        df['emovocab'] = 0
        df['totalemojis'] = 0
        df['top5emojis'] = 0
        df['vocab'] = 0
        df['top5words'] = 0
        df['words'] = 0
        df['Neg'] = 0
        df['Pos'] = 0
        df['Neu'] = 0
        for name in df['Author'].unique():
            data1 = df[df['Author'] == name]
            # create a single string containing all the words from all the messages
            dstr = ' '.join(data1['Message'])
            # convert the df column into a list
            dlist = data1['Message'].to_list()
            dstr_grp = dstr_grp + dstr
            # names['avgTime'][names['Name']==name] = data1['Time'].mean().strftime("%I:%M %p")

            NW = []  # blank list to store no. of words in a message
            for n in dlist:
                # store number of words in each message
                NW.append(len(n.split()))

            # mean of length of all words
            df['avgWordspermessage'][df['Author'] == name] = np.mean(NW)
            # min number of words
            df['minWordspermessage'][df['Author'] == name] = np.min(NW)
            # max number of words
            df['maxWordspermessage'][df['Author'] == name] = np.max(NW)

            NE = []  # blank list to store emojis
            NE = [e for e in dstr if e in emoji.UNICODE_EMOJI]
            dfE = pd.DataFrame({'Emoji': NE})
            EmoFreqdf = pd.DataFrame(dfE.groupby(['Emoji'])['Emoji'].count())
            EmoFreqdf.columns = ['Freq']
            EmoFreqdf = EmoFreqdf.reset_index()
            EmoFreqdf.columns = ['Emoji', 'Freq']
            # store total number of unique emojis used
            df['emovocab'][df['Author'] == name] = len(EmoFreqdf)
            # store total number of emojis sent
            df['totalemojis'][df['Author'] == name] = EmoFreqdf['Freq'].sum()
            EmoFreqdf = EmoFreqdf.sort_values('Freq', ascending=False)
            # store top 5 emojis
            df['top5emojis'][df['Author'] == name] = ' '.join(EmoFreqdf['Emoji'][0:5])

            lstAllWords = self.__clean_text(dstr, extra_StopWords).split()

            # remove those words which are in stop and emojis
            Words_df = pd.DataFrame({'Words': lstAllWords})
            Words_df = Words_df[-Words_df['Words'].isin(emoji.UNICODE_EMOJI.keys())]
            WordsFreqdf = pd.DataFrame(Words_df.groupby(['Words'])['Words'].count())
            WordsFreqdf.columns = ['Freq']
            WordsFreqdf = WordsFreqdf.reset_index()
            WordsFreqdf.columns = ['Word', 'Freq']
            # total number of unique words
            df['vocab'][df['Author'] == name] = len(WordsFreqdf)
            WordsFreqdf = WordsFreqdf.sort_values('Freq', ascending=False)
            # Top 5 words
            df['top5words'][df['Author'] == name] = ' '.join(WordsFreqdf['Word'][0:5])
            # All words
            df['words'][df['Author'] == name] = ' '.join(WordsFreqdf['Word'][0:])
            df = wcs.sentiment_author(name, dstr, df)
            if wordCloud == True:
                wcv.wordCloud(WordsFreqdf, maskpath)
        author_buffer_details = pd.DataFrame(data=df.Author.unique(), columns=['Author'])
        author_buffer_details = author_buffer_details.merge(df[['Author', 'avgWordspermessage', 'minWordspermessage', 'maxWordspermessage', 'emovocab', 'totalemojis', 'top5emojis', 'vocab', 'top5words', 'words', 'Pos', 'Neg', 'Neu']].drop_duplicates(), on='Author', how='left')
        return author_buffer_details
