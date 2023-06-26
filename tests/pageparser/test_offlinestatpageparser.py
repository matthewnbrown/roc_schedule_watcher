
from src.pageparser.offlinestatpageparser import OfflineStatPageParser

from option import Result
import unittest



class OfflinePageParserTest(unittest.TestCase):
    def test_when_invalid_html_should_err(self):
        parser = OfflineStatPageParser()
        
        result = parser.parse_offlinestat_page("<div> fsdfjnhfhg")
        
        self.assertTrue(result.is_err)
        error_message = result.err().expect("expected an error message")
        
        self.assertEqual(error_message, "Error parsing html")