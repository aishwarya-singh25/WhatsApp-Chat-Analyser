# WhatsApp-Chat-Analyser
Create visualizations and identify sentiments from the WhatsApp chats.

## Installing Package
pip install -i https://test.pypi.org/simple/ whatsapp-chat-analyser

## Usage
This pacakge can be used to perform text clearning, text visualisation and sentiment analysis for the WhatsApp conversation between individuals and/or group.
Accepted file format includes chats exported as txt files.

```
import whatsapp_chat_visualizer as wcv
wcv.pie(param = , data = )
# code for wordcloud
# code for sentiment analysis
```
Please refer to the following notebook to see how to use this package.

## Package Structure
```
WhatsApp-Chat-Analyser/
  |- .ipynb_checkpoints
     |- WhatsApp_analyser_ver3-checkpoint.ipynb
  |- WhatsappChatAnalyser/
     |- __init__.py 
     |- Sentiment.py
     |- author.py
     |- chat.py
     |- whatsapp_chat_sentiment.py
     |- whatsapp_chat_visualizer.py
     |- whatsapp_text_cleaner.py
     |- WhatsApp_analyser.ipynb
     |- WhatsApp Chat with UW MSDS Fall21.txt
  |- tests/
     |- __init__.py 
     |- author_tests.py
     |- chat_test.py
     |- whatsapp_chat_visualizer.py
     |- whatsapp_text_cleaner_test.py
  |- LISCENCE
  |- README.md
  |- pyproject.toml
  |- setup.py
```


## Installed Libraries and dependencies
- python version 3.7 and above
- datetime 
- regex 
- nltk 3.6.1
- wordcloud 1.8.1 (pip install wordcloud)
- emoji (pip install emoji)
