#!/usr/bin/env python
# coding: utf-8


import unittest
from WhatsappChatAnalyser import whatsapp_chat_visualizer as vis
import pandas as pd


df= pd.read_csv("Test_data.csv")


# Define a class in which the tests will run
class UnitTests(unittest.TestCase):

    # Each method in the class to execute a test
    def test_bar_plot(self):
        result = vis.bar_plot(df[['Author', 'Message']])
        with patch("my.module.plt.show") as show_patch:
            code_in_my_module_that_plots()
        assert show_patch.called
        return None
    
    def test_pie(self):
        result = vis.pie(df[['Author', 'Message']])
        with patch("my.module.plt.show") as show_patch:
            code_in_my_module_that_plots()
        assert show_patch.called

    def test_Wordcloud(self):
        result = vis.Wordcloud(df[['Author', 'Message']])
        with patch("my.module.plt.show") as show_patch:
            code_in_my_module_that_plots()
        assert show_patch.called


if __name__ == '__main__':
    unittest.main()