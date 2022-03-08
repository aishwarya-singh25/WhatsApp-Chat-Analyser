import unittest
from WhatsappChatAnalyser import group
import pandas as pd

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    def test_get_text_info(self):
        g=group.Group()
        df = pd.read_csv("Test_data.csv")
        result = g.get_text_info(df, ["are", "hi"], False)
        self.assertTrue(len(result.columns), 13)
        return None

if __name__ == '__main__':
    unittest.main()