# WhatsApp-Chat-Analyser
Create visualizations and identify sentiments from the WhatsApp chats. This package can be used to perform text clearning, text visualisation and sentiment analysis for the WhatsApp conversation between individuals and/or group.
Accepted file format includes chats exported as txt files.

## Installing Package
```
pip install -i https://test.pypi.org/simple/ whatsapp-chat-analyser==1.0.1
```

## Dependencies
The dependencies can be installed from the requirements.txt file using
```
python -m pip install -r requirements.txt
```

## Motivation
WhatsApp is one of the most commonly used mode of communication. It has more than 2 billion  users worldwide. An average user spends more than 195 minutes per week on WhatsApp. 
We aim to analyse WhatsApp chats to generate insights about the activity in group chats or 1:1 chats. The user is anyone who would like to create a clean dataframe from a WhatsApp text file or see information like the number of messages, participant activities, sentiment of the chat and various visualizations that help understand what is going on in the chat file. 

## Package Structure
```
WhatsApp-Chat-Analyser/
  |- WhatsappChatAnalyser/
     |- __init__.py 
     |- author.py
     |- group.py
     |- whatsapp_chat_sentiment.py
     |- whatsapp_chat_visualizer.py
     |- whatsapp_text_cleaner.py
  |- tests/
     |- __init__.py 
     |- test_group.py
     |- test_whatsapp_chat_sentiment.py
     |- Test_data.csv
  |- LICENSE
  |- README.md
  |- pyproject.toml
  |- setup.cfg
  |- requirements.txt
  
```
## Usage
```
from WhatsappChatAnalyser import whatsapp_text_cleaner as wtc
from WhatsappChatAnalyser import whatsapp_chat_visualizer as wcv
df = wtc.load_clean_dataframe('WhatsAppChatDemo.txt')
x = A.get_stats(df)
wcv.bar_plot(x[['Author','Media_shared']],max=5,sort=False)
wcv.pie(x[['Author','Media_shared']], max=7) 
```
Please refer to the sample notebook to see how to use this package.

## References
Our package is a one stop shop for cleaning, visualization, and performing sentiment analysis for a given input file. This has a lot of utility across multiple use-cases. The user does not have to perform the cleaning tasks manually and work on each individual aspect. Main requirement is package installation and the input text file. We have thus incorporated and built upon the functionalities from the following libraries:
* [NLTK](https://www.nltk.org/)
* [Matplotlib](https://matplotlib.org/)
* [Seaborn](https://seaborn.pydata.org/)
* [Regex](https://docs.python.org/3/library/re.html)

## Code Style

We have used PEP 8 Style Guide for Python code such as docstrings and indentation.

The design principles used are:
* Object oriented design using encapsulation and abstraction
* Modularization is implemented using deep modules and separation of concerns
* Test driven development using unittest framework

Version control is achieved using GitHub.

## Contributors

* [Khirod Sahoo](https://github.com/khirodsahoo93)
* [Anushka Singh](https://github.com/anushka-18)
* [Ananya Sharma](https://github.com/03ananya)
* [Aishwarya Singh](https://github.com/aishwarya-singh25)
