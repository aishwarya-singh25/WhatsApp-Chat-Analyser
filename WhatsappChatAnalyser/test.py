print("hello user")
import author 
import whatsapp_text_cleaner as wtc
import pandas as pd

filepath='/Users/stlp/Downloads/WhatsApp Chat with UW MSDS Fall21.txt'
text_df=wtc.load_clean_dataframe(filepath)
A=author.Author()
A.update_info(text_df)
df=A.get_number_textMessages(text_df)
print(text_df.tail())
print("code ran succesfully")