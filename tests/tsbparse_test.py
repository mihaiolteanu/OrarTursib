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
             with self.open_file(entry['input']) as f:
                 parsed = tsbparse.news_page_content(f)
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
            with self.open_file(entry['input']) as f:
                parsed = tsbparse.news_page_links(f)
                self.assertEqual(entry['expected'], parsed)
       

    def test_update_string(self):
        data = [
            {'input': 'tursib_ro_trasee.htm', # Valid tursib page containing info regarding the last update.
             'expected': 'Program de circulatie incepand cu data de 23 martie 2015'},
            {'input': 'tursib_ro.htm', # Tursib page that does not contain the data of interest.
             'expected': ""},
            {'input': 'dummy_file.txt', # Invalid / random file.
             'expected': ""}
        ]
        for entry in data:
            with self.open_file(entry['input']) as f:
                parsed = tsbparse.update_string(f)
                self.assertEqual(entry['expected'], parsed, entry['input'])


    def test_buses_info(self):
        data = [
            {'input': 'tursib_ro_trasee.htm', # Valid tursib page containing the data of interest.
             'expected_count': 21, # Number of buses.
             # Take a random entry from the list of returned buses.
             'expected_exists': {'number': '14', 'link': 'http://tursib.ro/traseu/14', 'name': 'Valea Aurie - Hotel Libra'}},
            {'input': 'tursib_ro.htm', # Tursib page that does not contain the data of interest.
             'expected_count': 0,
             'expected_exists': None},
            {'input': 'dummy_file.txt', # Invalid / random file.
             'expected_count': 0,
             'expected_exists': None}
        ]
        for entry in data:
            with self.open_file(entry['input']) as f:
                parsed = tsbparse.buses_info(f)
                self.assertEqual(entry['expected_count'], len(parsed))
                # Go to the bus expected in the data list above.
                for item in parsed:
                    if item['number'] == entry['expected_exists']['number']:
                        self.assertEqual(item, entry['expected_exists'])
                    

    def test_bus_stations(self):
        data = [
            {'input': 'tursib_ro_traseu_11.htm', # Valid page.
             'exp_dcount': 17, # Number of direct routes
             'exp_rcount': 24, # Number of reverse routes
             'exp_dentry': {'name': "MC DONALD'S", 'link': 'http://tursib.ro/traseu/11/program?statie=7&dir=dus'},
             'exp_rentry': {'name': 'BOSCH', 'link': 'http://tursib.ro/traseu/11/program?statie=8&dir=intors'}},
            {'input': 'tursib_ro.htm', # Tursib page that does not contain the data of interest.
             'exp_dcount': 0,
             'exp_rcount': 0,
             'exp_dentry': None, # Expected direct routes bus name / link dictionary entry
             'exp_rentry': None},# Same for reverse routes
            {'input': 'dummy_file.txt', # Invalid / random file.
             'exp_dcount': 0,
             'exp_rcount': 0,
             'exp_dentry': None,
             'exp_rentry': None}
        ]
        for entry in data:
             with self.open_file(entry['input']) as f:
                 parsed = tsbparse.bus_stations(f)
                 self.assertEqual(entry['exp_dcount'], len(parsed['directroutes']))
                 self.assertEqual(entry['exp_rcount'], len(parsed['reverseroutes']))
                 exp_dentry = entry['exp_dentry']
                 exp_rentry = entry['exp_rentry']
                 if not exp_dentry or not exp_rentry:
                     # We've already checked the count.
                     continue
                 self.assertTrue(exp_dentry in parsed['directroutes'])
                 self.assertTrue(exp_rentry in parsed['reverseroutes'])


    def test_station_timetable(self):
        data = [
            {'input': 'tursib_ro_traseu_112_Bosch.htm', # Valid page.
             'exp': {'sunday': ['07:26', '19:26'], # Expected output.
                     'saturday': ['07:26', '19:26'], 
                     'weekdays': ['07:26', '08:31', '15:26', '16:31', '17:41', '23:26']}},
            {'input': 'tursib_ro.htm', # Tursib page that does not contain the data of interest.
             'exp': {'sunday': [], 'saturday': [], 'weekdays': []}},
            {'input': 'dummy_file.txt', # Invalid / random file
             'exp': {'sunday': [], 'saturday': [], 'weekdays': []}}
        ]
        for entry in data:
             with self.open_file(entry['input']) as f:
                 parsed = tsbparse.station_timetable(f)
                 self.assertEqual(entry['exp'], parsed)
             




#if __name__ == '__main__':
unittest.main()

