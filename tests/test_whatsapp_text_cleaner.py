import unittest
from WhatsappChatAnalyser import whatsapp_text_cleaner as wtc

# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    def test_DateStart(self):
        res = wtc.DateStart("26/05/20, 12:59 pm")
        self.assertEqual(res, True)

    def test_AuthorStart(self):
        res = wtc.AuthorStart("Peter Win")
        self.assertEqual(res, False)

    def test_getDetails(self):
        date, time, author, message = wtc.getDetails("3/7/22, 23:23 - Aishwarya: Hi guys")
        self.assertEqual(author, "Aishwarya")

    def test_convert24(self):
        self.assertEqual("12:59 am", "12:59 am")

if __name__ == '__main__':
    unittest.main()