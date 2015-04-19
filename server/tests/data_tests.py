import unittest
import data
import tests.utils_mock as utils_mock
import os

# Return html files from local storage.
tsb.htmlget = utils_mock.htmlget

class tsb_tests(unittest.TestCase):

    def test_news(self):
        res = data.news()
        self.assertEqual(len(res), 3)
        self.assertEqual(res[0]['publishdate'], "12 Feb 2015")
        self.assertTrue('Incepand cu data de 16.02.2015' in res[0]['newscontent'])
 

#if __name__ == '__main__':
unittest.main()
