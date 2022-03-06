print("hello user")
import author 
import chat
import whatsapp_text_cleaner as wtc
import pandas as pd
import warnings
import matplotlib.pyplot as plt
import numpy as np
from IPython.display import set_matplotlib_formats
warnings.filterwarnings("ignore")
import nltk
import whatsapp_chat_visualizer as wcv
explode=[0.1,0,0.1,0.2,0.4]
nltk.data.path.append('/Users/stlp/Downloads/')
extra_StopWords = ["thats","dont","<Media omitted>","media","Media","Omitted","omitted","also","like","https","from","all","also","and","any","are","but","can","cant","cry","due","etc","few","for","get","had","has","hasnt","have","her","here","hers","herself","him","himself","his","how","inc","into","its","ltd","may","nor","not","now","off","once","one","only","onto","our","ours","out","over","own","part","per","put","see","seem","she","than","that","the","their","them","then","thence","there","these","they","this","those","though","thus","too","top","upon","very","via","was","were","what","when","which","while","who","whoever","whom","whose","why","will","with","within","without","would","yet","you","your","yours","the"]
filepath='/Users/stlp/Downloads/WhatsApp Chat with UW MSDS Fall21.txt'
text_df=wtc.load_clean_dataframe(filepath)
A=author.Author()
C=chat.Chat()
A.update_info(text_df)
C.update_info(text_df)
#author_buffer_details=pd.DataFrame(data=A.name,columns=['Author'])
#author_buffer_details=author_buffer_details.merge(A.get_number_activeDays(text_df),on='Author',how='left')
#df_days_texted=pd.DataFrame(text_df.groupby('Author')['Date'].nunique()).rename(columns={'Date':'Days_texted'})
#df=A.get_metrics(text_df)
df_new=A.remove_null_authors(text_df)
df=A.get_frequency(text_df)

print(df)
#wcv.bar_plot(df,max=5,sort=False)
#wcv.pie(df,max=5,explode=explode)
df=A.get_author_text_info(df_new,extra_StopWords,wordCloud=True)
print(df.head())
print("code ran succesfully")

