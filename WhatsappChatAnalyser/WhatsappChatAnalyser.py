import whatsapp_text_cleaner as wtc
filepath='/Users/stlp/Downloads/WhatsApp Chat with UW MSDS Fall21.txt'
df=wtc.load_df(filepath)
class text:
    def __init__(self,filepath,df=None):
       self.filepath=filepath
    def clean_text(self):
        return wtc.load_df(self.filepath)

print(df.head())