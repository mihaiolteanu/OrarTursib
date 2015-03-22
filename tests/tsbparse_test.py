import unittest
import os
import tsbparse


class tsbparse_tests(unittest.TestCase):
    # Get the samples directory.
    samples_path = os.path.join(os.path.dirname('__file__'), 'tests/samples')

    def open_file(self, name):
        file = os.path.join(self.samples_path, name)
        return open(file, "r", encoding='utf-8', errors='ignore')

    def test_news_page_content(self):
        data = [
            {'input': 'news_160.htm',   # Valid tursib page containing news.
             'expected': {'publishdate': '12 Feb 2015','newscontent': 'Incepand cu data de 16.02.2015, se inchide circulatia'}},
            {'input': 'tursib_ro.htm',  # Tursib page that does not contain any news.
             'expected': {'publishdate': None, 'newscontent': None}},
            {'input': 'dummy_file.txt', # Invalid / random file.
             'expected': {'publishdate': None, 'newscontent': None}},
            {'input': 'news_160_missing_publishdate_header.htm', # Modified the remove the 'publishdate' field.
             'expected': {'publishdate': None, 'newscontent': None}},
        ]

        for entry in data:
             with self.open_file(entry['input']) as input_file:
                 parsed = tsbparse.news_page_content(input_file)
                 self.assertEqual(parsed['publishdate'], entry['expected']['publishdate'])
                 # If there is something to compare
                 if parsed['newscontent'] and entry['expected']['newscontent']:
                     # Only check part of the news, as these can get quite big.
                     self.assertTrue(entry['expected']['newscontent'] in parsed['newscontent'])
                 else:
                     # No news content, but is that what we expected?
                     self.assertEqual(entry['expected']['newscontent'], parsed['newscontent'])
                 

    def test_news_page_links(self):
        data = [
            {'input': 'tursib_ro.htm', # Valid tursib page containing links to news.
             'expected': ['http://tursib.ro/news/show/161', 'http://tursib.ro/news/show/160', 'http://tursib.ro/news/show/159']},

            {'input': 'dummy_file.txt', # Invalid / random file.
             'expected': []}
        ]

        for entry in data:
            with self.open_file(entry['input']) as input_file:
                parsed = tsbparse.news_page_links(input_file)
                self.assertEqual(entry['expected'], parsed)
       


#if __name__ == '__main__':
unittest.main()

