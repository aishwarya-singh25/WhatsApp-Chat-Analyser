import unittest
import chat

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    # Each method in the class to execute a test
    def test_smoke_test(self):
        result = chat.clean_text("hi how are you doing today", ["are", "hi"])
        self.assertEqual(result, ["today"])

        return None


print("Bye!")

if __name__ == '__main__':
        unittest.main()