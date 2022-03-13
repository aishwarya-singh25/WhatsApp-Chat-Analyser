# create functions for data cleaning of whatsapp chats

# import necessary libraries
import re
import pandas as pd


# Start defining functions
# load the text file.
# For this we would save the text in a location
# and input the file path into the function itself
# Function to check if the text is a new one or a continuation of old one.

def DateStart(s):
    patterns = ['([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]|[0-9]):([0-9][0-9])',
                '([0-2][0-9]|(3)[0-1])(\/)(((0)[0-9])|((1)[0-2]))(\/)(\d{2}|\d{4}), ([0-9][0-9]|[0-9]):([0-9][0-9])']
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False


# Function to check if there is any author of the text
def AuthorStart(s):
    patterns = [
        # First Name
        '([\w]+):',
        # First Name + Last Name
        '([\w]+[\s]+[\w]+):',
        # First Name + Middle Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+):',
        # First Name + Middle Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+):',
        # First Name + Middle Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+):',
        # First Name + Middle Name + Last Name
        '([\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+[\s]+[\w]+):',
        '([+]\d{2} \d{5} \d{5}):',  # Mobile Number (India)
        '([+]\d{1} [(]\d{3}[)] \d{3}[-]\d{4}):',  # Mobile Number (US)
        # '([+]\d{1} \S{5} \S{8}):',   # Mobile Number (US)
        # '([+]\d{1}[\s]\(\w{3}\)[\s]\w{3}-\w{4}):',
        '([+]\d{2} \d{4} \d{7}):'  # Mobile Number (Europe)
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
    # List to keep track of data so it can be used by a Pandas dataframe
    parsedData = []
    ChatPath = filepath
    with open(ChatPath, encoding="utf-8") as fp:
        # Skipping first line of the file
        # (usually contains information about end-to-end encryption)
        fp.readline()
        # Buffer to capture intermediate output for multi-line messages
        messageBuffer = []
        # Intermediate variables to keep track of the current message
        date, time, author = None, None, None
        while True:
            line = fp.readline()
            # print(line)# can read lines
            if not line:
                # Stop reading further if end of file has been reached
                break
            # Guarding against erroneous leading and trailing whitespaces
            line = line.strip()
            # print(line)#print lines properly
            if DateStart(line):
                # If a line starts with a Date Time pattern,
                # then this indicates the beginning of a new message
                # Check if the message buffer contains
                # characters from previous iterations
                if len(messageBuffer) > 0:
                    # print(messageBuffer)
                    parsedData.append(
                        [date, time, author, ' '.join(messageBuffer)])
                    # print(parsedData)
                    # Save the tokens from the previous message in parsedData
                # Clear the message buffer so that
                # it can be used for the next message
                messageBuffer.clear()
                # Identify and extract tokens from the line
                date, time, author, message = getDetails(line)
                messageBuffer.append(message)  # Append message to buffer

            else:
                # print('Entered else loop')#entering here
                # If a line doesn't start with a Date Time pattern,
                # then it is part of a multi-line message.
                # So, just append to buffer
                messageBuffer.append(line)

    df = pd.DataFrame(parsedData, columns=['Date', 'Time',
                                           'Author', 'Message'])
    return df


# Insert hours of the day in 24hrs format
def convert24(str1):
    # Checking if last two elements of time
    # is AM and first two elements are 12
    if (str1[-2:]).lower() == "am" and (str1[:2]).lower() == "12":
        return str(0)

        # remove the AM
    elif (str1[-2:]).lower() == "am":
        return str1[:2].replace(':', '')

        # Checking if last two elements of time
    # is PM and first two elements are 12
    elif (str1[-2:]).lower() == "pm" and (str1[:2]).lower() == "12":
        return str1[:2].replace(':', '')

    else:

        # add 12 to hours and remove PM
        return str(int(str1[:2].replace(':', '')) + 12)


def load_clean_dataframe(filepath):
    df = intial_dataframe(filepath)
    # converting date from string to date format
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df['Hours'] = df['Time'].apply(lambda x: convert24(x.strip()))
    return df
