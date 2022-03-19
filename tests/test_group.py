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
        df = pd.read_csv('/Users/stlp/Documents/GitHub/WhatsappChatAnalyser/tests/Test_data.csv')
        g.update_info(df)
        result = g.get_text_info(wordCloud=False)
        self.assertEqual(len(result.columns), 13)
        return None

if __name__ == '__main__':
    unittest.main()
