import unittest
import os
import parser


class parser_tests(unittest.TestCase):
    # Get the samples directory.
    samples = os.path.join(os.path.dirname('__file__'), 'tests/samples')

    def fileread(self, name):
        path = os.path.join(self.samples, name)
        f = open(path, "r", encoding='utf-8', errors='ignore')
        read = f.read()
        f.close()
        return read

    def test_news_content(self):
        data = [
            {'in': 'news_160.htm',   # Valid tursib page containing news.
             'exp': {'publishdate': '12 Feb 2015','newscontent': 'Incepand cu data de 16.02.2015, se inchide circulatia'}},
            {'in': 'tursib_ro.htm',  # Tursib page that does not contain any news.
             'exp': {'publishdate': None, 'newscontent': None}},
            {'in': 'dummy_file.txt', # Invalid / random file.
             'exp': {'publishdate': None, 'newscontent': None}},
            {'in': 'news_160_missing_publishdate_header.htm', # Modified the remove the 'publishdate' field.
             'exp': {'publishdate': None, 'newscontent': None}},
        ]
        for entry in data:
             f = self.fileread(entry['in'])
             parsed = parser.news_content(f)
             self.assertEqual(parsed['publishdate'], entry['exp']['publishdate'])
             # If there is something to compare
             if parsed['newscontent'] and entry['exp']['newscontent']:
                 # Only check part of the news, as these can get quite big.
                 self.assertTrue(entry['exp']['newscontent'] in parsed['newscontent'])
             else:
                 # No news content, but is that what we exp?
                 self.assertEqual(entry['exp']['newscontent'], parsed['newscontent'])
                 

    def test_news_links(self):
        data = [
            {'in': 'tursib_ro.htm', # Valid tursib page containing links to news.
             'exp': ['http://tursib.ro/news/show/161', 'http://tursib.ro/news/show/160', 'http://tursib.ro/news/show/159']},
            {'in': 'dummy_file.txt', # Invalid / random file.
             'exp': []}
        ]
        for entry in data:
            f = self.fileread(entry['in'])
            parsed = parser.news_links(f)
            self.assertEqual(entry['exp'], parsed)
       

    def test_update_string(self):
        data = [
            {'in': 'tursib_ro_trasee.htm', # Valid tursib page containing info regarding the last update.
             'exp': 'Program de circulatie incepand cu data de 23 martie 2015'},
            {'in': 'tursib_ro.htm', # Tursib page that does not contain the data of interest.
             'exp': ""},
            {'in': 'dummy_file.txt', # Invalid / random file.
             'exp': ""}
        ]
        for entry in data:
            f = self.fileread(entry['in'])
            parsed = parser.update_string(f)
            self.assertEqual(entry['exp'], parsed, entry['in'])


    def test_buses_list(self):
        data = [
            {'in': 'tursib_ro_trasee.htm', # Valid tursib page containing the data of interest.
             'exp_count': 21, # Number of buses.
             # Take a random entry from the list of returned buses.
             'exp_exists': {'number': '14', 'link': 'http://tursib.ro/traseu/14', 'name': 'Valea Aurie - Hotel Libra'}},
            {'in': 'tursib_ro.htm', # Tursib page that does not contain the data of interest.
             'exp_count': 0,
             'exp_exists': None},
            {'in': 'dummy_file.txt', # Invalid / random file.
             'exp_count': 0,
             'exp_exists': None}
        ]
        for entry in data:
            f = self.fileread(entry['in'])
            parsed = parser.buses_list(f)
            self.assertEqual(entry['exp_count'], len(parsed))
            # Go to the bus exp in the data list above.
            for item in parsed:
                if item['number'] == entry['exp_exists']['number']:
                    self.assertEqual(item, entry['exp_exists'])
                    

    def test_bus_stations(self):
        data = [
            {'in': 'tursib_ro_traseu_11.htm', # Valid page.
             'exp_dcount': 17, # Number of direct routes
             'exp_rcount': 24, # Number of reverse routes
             'exp_dentry': {'name': "MC DONALD'S", 'link': 'http://tursib.ro/traseu/11/program?statie=7&dir=dus'},
             'exp_rentry': {'name': 'BOSCH', 'link': 'http://tursib.ro/traseu/11/program?statie=8&dir=intors'}},
            {'in': 'tursib_ro.htm', # Tursib page that does not contain the data of interest.
             'exp_dcount': 0,
             'exp_rcount': 0,
             'exp_dentry': None, # Expected direct routes bus name / link dictionary entry
             'exp_rentry': None},# Same for reverse routes
            {'in': 'dummy_file.txt', # Invalid / random file.
             'exp_dcount': 0,
             'exp_rcount': 0,
             'exp_dentry': None,
             'exp_rentry': None}
        ]
        for entry in data:
            f = self.fileread(entry['in'])
            parsed = parser.bus_stations(f)
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
            {'in': 'tursib_ro_traseu_112_Bosch.htm', # Valid page.
             'exp': {'sunday': ['07:26', '19:26'], # Expected output.
                     'saturday': ['07:26', '19:26'], 
                     'weekdays': ['07:26', '08:31', '15:26', '16:31', '17:41', '23:26']}},
            {'in': 'tursib_ro.htm', # Tursib page that does not contain the data of interest.
             'exp': {'sunday': [], 'saturday': [], 'weekdays': []}},
            {'in': 'dummy_file.txt', # Invalid / random file
             'exp': {'sunday': [], 'saturday': [], 'weekdays': []}}
        ]
        for entry in data:
            f = self.fileread(entry['in'])
            parsed = parser.station_timetable(f)
            self.assertEqual(entry['exp'], parsed)
             

#if __name__ == '__main__':
unittest.main()

