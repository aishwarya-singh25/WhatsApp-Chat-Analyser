# create functions for data cleaning of whatsapp chats

# Importing Required Libraries
import re
import numpy as np
import pandas as pd
import datetime

# Function to check if the text is a new one or a continuation of old one based on datetime.
def DateStart(s):
    patterns = ['([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]|[0-9]):([0-9][0-9])',
    '([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]|[0-9]):([0-9][0-9])']
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

# Function checking if there is any author of the text
def AuthorStart(s):
    patterns = [
        '([\w]+):',                        # First Name
        '([\w]+[\s]+[\w]+):',              # First Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+):',    # First Name + Middle Name + Last Name
        '([+]\d{2} \d{5} \d{5}):',         # Mobile Number (India)
        '([+]\d{2} \d{3} \d{3} \d{4}):',   # Mobile Number (US)
        '([+]\d{2} \d{4} \d{7})'           # Mobile Number (Europe)
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False

# Function to fetch details a single line of text: date,time,author,message
def getDetails(line):
    splitLine = line.split(' - ')  
    dateTime = splitLine[0]
    date, time = dateTime.split(', ')  
    message = ' '.join(splitLine[1:])  
    if AuthorStart(message):  
        splitMessage = message.split(': ')  
        author = splitMessage[0]  
        message = ' '.join(splitMessage[1:])  
    else:
        author = None
    return date, time, author, message


def intial_dataframe(filepath):
    parsedData = [] 
    ChatPath = filepath
    with open(ChatPath, encoding="utf-8") as fp:
        fp.readline()
        messageBuffer = []  # Buffer to capture intermediate output for multi-line messages
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            if not line:  # Stop reading further if end of file has been reached
                break
            line = line.strip()  # Guarding against erroneous leading and trailing whitespaces
            if DateStart(line):  # Line starting with a Date Time pattern, indicates beginning of a new message
                # Check if the message buffer contains characters from previous iterations
                if len(messageBuffer) > 0:
                    parsedData.append(
                        [date, time, author, ' '.join(messageBuffer)])
                messageBuffer.clear() # Clear the message buffer so that it can be used for the next message
                # Identify and extract tokens from the line
                date, time, author, message = getDetails(line)
                messageBuffer.append(message)  # Append message to buffer

            else:
                # If line doesn't start with a Date Time pattern, then it is a multi-line message.
                messageBuffer.append(line) # Append message to buffer

    df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message'])
    return df

#Insert hours of the day in 24hrs format
def convert24(str1): 
      
    # Checking if last two elements of time is AM and first two elements are 12 
    if (str1[-2:]).lower() == "am" and (str1[:2]).lower() == "12": 
        return str(0) 
          
    # remove the AM     
    elif (str1[-2:]).lower() == "am": 
        return str1[:2].replace(':','') 
      
    # Checking if last two elements of time is PM and first two elements are 12    
    elif (str1[-2:]).lower() == "pm" and (str1[:2]).lower() == "12": 
        return str1[:2].replace(':','')  
  
    # add 12 to hours and remove PM 
    else:
        return str(int(str1[:2].replace(':','')) + 12) 
          

def load_clean_dataframe(filepath):
    df=intial_dataframe(filepath)
    # converting date from string to date format
    df['Date']=pd.to_datetime(df['Date'],dayfirst=True)
    df['Hours']=df['Time'].apply(lambda x : convert24(x.strip()))
    return df
