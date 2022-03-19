from tokenize import Ignore
import unittest
from WhatsappChatAnalyser import group
import pandas as pd
import warnings
warnings.filterwarnings("ignore")

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    def test_get_text_info(self):
        g=group.Group()
<<<<<<< HEAD:WhatsappChatAnalyser/tests/test_group.py
    
        df = pd.read_csv("/Users/stlp/Documents/GitHub/WhatsappChatAnalyser/WhatsappChatAnalyser/tests/Test_data.csv")
        g.update_info(df)
        result = g.get_text_info(wordCloud=False)
        self.assertTrue(len(result.columns), 1900)
=======
        df = pd.read_csv("Test_data.csv")
        result = g.get_text_info(df, ["are", "hi"], False)
        self.assertTrue(len(result.columns), 13)
>>>>>>> be32907d26afd0b5e21fe9487f40c1100b5da6f1:tests/test_group.py
        return None

if __name__ == '__main__':
    unittest.main()
