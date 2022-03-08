import unittest
import sentiment
import pandas as pd

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    # Each method in the class to execute a test
    def test_getResultNegative(self):
        result = sentiment.getResult(0.4,0.2,0.5)
        self.assertEqual(result, "Negative")
        return None

    def test_getResultPositive(self):
        result = sentiment.getResult(0.5,0.4,0.2)
        self.assertEqual(result, "Positive")
        return None

    def test_getResultNeutral(self):
        result = sentiment.getResult(0.2,0.5,0.3)
        self.assertEqual(result, "Neutral")
        return None

if __name__ == '__main__':
    unittest.main()