#!/usr/bin/env python
# coding: utf-8

# In[2]:


print("hello user")
import author
import group
import whatsapp_text_cleaner as wtc
import warnings
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import set_matplotlib_formats
warnings.filterwarnings("ignore")
import nltk
nltk.data.path.append('/Users/stlp/Downloads/')
nltk.download('stopwords')
import whatsapp_chat_visualizer as wcv
maskpath='wordcloud trump.png'
explode=[0.1,0,0.1,0.2,0.4]
#nltk.data.path.append('/Users/stlp/Downloads/')
extra_StopWords = ["thats","dont","<Media omitted>","media","Media","Omitted","omitted","also","like","https","from","all","also","and","any","are","but","can","cant","cry","due","etc","few","for","get","had","has","hasnt","have","her","here","hers","herself","him","himself","his","how","inc","into","its","ltd","may","nor","not","now","off","once","one","only","onto","our","ours","out","over","own","part","per","put","see","seem","she","than","that","the","their","them","then","thence","there","these","they","this","those","though","thus","too","top","upon","very","via","was","were","what","when","which","while","who","whoever","whom","whose","why","will","with","within","without","would","yet","you","your","yours","the"]
filepath='/Users/stlp/Downloads/WhatsApp Chat with UW MSDS Fall21.txt'
text_df=wtc.load_clean_dataframe(filepath)
maskpath='/Users/stlp/Documents/wordcloud mask.jpg'
A=author.Author()
G=group.Group()
A.update_info(text_df)
G.update_info(text_df)
#author_buffer_details=pd.DataFrame(data=A.name,columns=['Author'])
#author_buffer_details=author_buffer_details.merge(A.get_number_activeDays(text_df),on='Author',how='left')
#df_days_texted=pd.DataFrame(text_df.groupby('Author')['Date'].nunique()).rename(columns={'Date':'Days_texted'})
#df=A.get_metrics(text_df)

#x=A.get_text_info(text_df)
y=G.get_text_info(extra_StopWords,wordCloud=True)
#wcv.pie(x[['Author','Pos']],max=1)
#wcv.bar_plot(df,max=5,sort=False)
#wcv.pie(df,max=5,explode=explode)
#df=C.get_text_info(df_new,extra_StopWords,wordCloud=True)
print(y)
print("code ran succesfully")




