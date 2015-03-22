import unittest
import os
import tsbparse


class tsbparse_tests(unittest.TestCase):
    # Get the samples directory.
    samples_path = os.path.join(os.path.dirname('__file__'), 'tests/samples')

    def open_file(self, name):
        file = os.path.join(self.samples_path, name)
        return open(file, "r", encoding='utf-8', errors='ignore')

        ### News Page Contents ###
    def test_news_page_content_valid_html(self):
        with self.open_file("news_160.htm") as valid_news_page:
            parsed = tsbparse.news_page_content(valid_news_page)
            self.assertTrue("12 Feb 2015" in parsed['publishdate'], parsed)
            self.assertTrue("Incepand cu data de 16.02.2015" in parsed['newscontent'], parsed)

    def test_news_page_content_not_news_page(self):
        # Load a different tursib page that does not contain a news section.
        with self.open_file("tursib_ro.htm") as not_news_page:
            parsed = tsbparse.news_page_content(not_news_page)
            self.assertIsNone(parsed['publishdate'])
            self.assertIsNone(parsed['newscontent'])

    def test_news_page_content_not_html_page(self):
        # Load a random file.
        with self.open_file("dummy_file.txt") as not_html_page:
            parsed = tsbparse.news_page_content(not_html_page)
            self.assertIsNone(parsed['publishdate'])
            self.assertIsNone(parsed['newscontent'])

    def test_news_page_content_missing_publishdate_header(self):
        # Load a news html file but without the <h2> header specifying the publish date.
        with self.open_file("news_160_missing_publishdate_header.htm") as invalid_news_page:
            parsed = tsbparse.news_page_content(invalid_news_page)
            self.assertIsNone(parsed['publishdate'], None)
            self.assertTrue("Incepand cu data de 16.02.2015" in parsed['newscontent'], parsed)

        ### News Page Links ###
    def test_news_page_links_valid_html(self):
        with self.open_file("tursib_ro.htm") as valid_page:
            parsed = tsbparse.news_page_links(valid_page)
            expected = ['http://tursib.ro/news/show/161', 'http://tursib.ro/news/show/160', 'http://tursib.ro/news/show/159']
            self.assertEqual(expected, parsed)

    def test_news_page_links_not_links_page(self):
        # Load a different tursib pabge that does not contain news links
        with self.open_file("tursib_ro_trasee.htm") as not_links_page:
            parsed = tsbparse.news_page_links(not_links_page)
            self.assertEqual([], parsed)
            


#if __name__ == '__main__':
unittest.main()

