
from src.offlinestatpageparser import OfflineStatPageParser

from option import Result
import unittest

class OfflinePageParserTest(unittest.TestCase):
    def _load_offline_commandchain_officers(self) -> str:
        with open("./tests/testpages/offlineofficers.html", "r") as file:
            data = file.read()
        return data
    
    def _load_online_commandchain_noofficers(self) -> str:
        with open("./tests/testpages/online.html", "r") as file:
            data = file.read()
        return data

    def _load_no_command_chain(self) -> str:
        with open("./tests/testpages/no_command_chain.html", "r") as file:
            data = file.read()
        return data
    
    def _load_no_alliance(self) -> str:
        with open("./tests/testpages/no_alliance.html", "r") as file:
            data = file.read()
        return data
    
    def test_when_invalid_html_should_err(self):
        parser = OfflineStatPageParser()
        
        result = parser.parse_offlinestat_page("<div> fsdfjnhfhg")
        
        self.assertTrue(result.is_err)
        error_message = result.err().expect("expected an error message")
        
        self.assertEqual(error_message, "Error parsing html")
        
    def test_user_with_all_fields_offline(self):
        parser = OfflineStatPageParser()
        
        pagehtml = self._load_offline_commandchain_officers()
        
        result = parser.parse_offlinestat_page(pagehtml)
        
        page = result.expect("should have value")
        
        self.assertEqual(page.username, 'k')
        self.assertEqual(page.rank, 36)
        self.assertEqual(page.alliance_id.unwrap(), 4690)
        self.assertEqual(page.tff, 2593069)
        self.assertEqual(page.tff_type, "Humans")
        self.assertEqual(page.commandchain_top_id.unwrap(), 31164)
        self.assertEqual(page.commander_id.unwrap(), 30228)
        self.assertEqual(len(page.officers), 4)
        self.assertEqual(page.officers, [14, 31123, 31143, 25638])
        self.assertFalse(page.is_online)
        
    def test_when_user_no_officers_online(self):
        parser = OfflineStatPageParser()
        
        pagehtml = self._load_online_commandchain_noofficers()
        
        result = parser.parse_offlinestat_page(pagehtml)
        
        page = result.expect("should have value")
        
        self.assertTrue(page.is_online)
        self.assertEqual(page.rank, 54)
        self.assertEqual(page.commander_id.unwrap(), 29428)
        self.assertEqual(page.officers, [])
    
    def test_when_user_no_alliance(self):
        parser = OfflineStatPageParser()
        
        pagehtml = self._load_no_alliance()
        
        result = parser.parse_offlinestat_page(pagehtml)
        
        page = result.expect("should have value")
        
        self.assertTrue(page.commander_id.unwrap(), 10847)
        self.assertTrue(page.commandchain_top_id.unwrap(), 31015)
        self.assertTrue(page.alliance_id.is_none)
        
    def test_when_user_no_command_chain(self):
        parser = OfflineStatPageParser()
        
        pagehtml = self._load_no_command_chain()
        
        result = parser.parse_offlinestat_page(pagehtml)
        
        page = result.expect("should have value")
        
        self.assertTrue(page.commander_id.is_none)
        self.assertTrue(page.alliance_id.is_none)
        self.assertTrue(page.commandchain_top_id.is_none)
        