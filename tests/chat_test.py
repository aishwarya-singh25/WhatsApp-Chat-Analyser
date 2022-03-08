import unittest
import chat
import pandas as pd

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    # Each method in the class to execute a test
    def test_clean_text(self):
        c=chat.Chat()
        result = c.clean_text("hi how are you doing today anushka", ["are", "hi"])
        self.assertEqual(result, "today anushka")
        return None

    def test_get_text_info(self):
        c=chat.Chat()
        df = pd.read_csv("Test_data.csv")
        result = c.get_text_info(df, ["are", "hi"], False)
        self.assertTrue(len(result.columns), 13)
        return None

if __name__ == '__main__':
    unittest.main()