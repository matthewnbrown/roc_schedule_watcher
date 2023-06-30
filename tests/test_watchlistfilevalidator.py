from src.watchlistvalidator import WatchlistValidator

import mock
import unittest

@mock.patch('src.watchlistvalidator.Logger')
class WatchListValidatorTest(unittest.TestCase):
    def test_list_with_one_valid_id_should_be_valid(self, mocklogger):
        testdata = ["53"]
    
        sut = WatchlistValidator(mocklogger)
        
        result = sut.is_list_valid(testdata)
        
        self.assertTrue(result.is_none)
    
    def test_list_with_many_valid_ids_should_be_valid(self, mocklogger):
        testdata = ['32', '654', '332']
    
        sut = WatchlistValidator(mocklogger)
        
        result = sut.is_list_valid(testdata)
        
        self.assertTrue(result.is_none)
    
    def test_list_with_one_invalid_id_should_be_invalid(self, mocklogger):
        testdata = ['3dgag2']
    
        sut = WatchlistValidator(mocklogger)
        
        result = sut.is_list_valid(testdata)
        
        self.assertTrue(result.is_some)
        self.assertIn('User ID "3dgag2" not in valid format', result.value)
        
    def test_list_with_many_invalid_ids_should_be_invalid(self, mocklogger):
        testdata = ['3dgag2', 'abc123', 'def543']
    
        sut = WatchlistValidator(mocklogger)
        
        result = sut.is_list_valid(testdata)
        
        self.assertTrue(result.is_some)
        self.assertIn('User ID "3dgag2" not in valid format', result.value)
        self.assertIn('User ID "abc123" not in valid format', result.value)
        self.assertIn('User ID "def543" not in valid format', result.value)
        
        
    def test_nonlist_should_be_invalid(self, mocklogger):
        testdata = 43
        
        sut = WatchlistValidator(mocklogger)
        
        result = sut.is_list_valid(testdata)
        
        self.assertTrue(result.is_some)
        self.assertEqual(result.value, ["Id list must be a list"])
        
    def test_no_elements_should_be_invalid(self, mocklogger):
        testdata = []
        
        sut = WatchlistValidator(mocklogger)
        
        result = sut.is_list_valid(testdata)
        
        self.assertTrue(result.is_some)
        self.assertEqual(result.value, ["Id list must contain elements"])
    
    def test_listisnone_should_be_invalid(self, mocklogger):
        testdata = None
        
        sut = WatchlistValidator(mocklogger)
        
        result = sut.is_list_valid(testdata)
        
        self.assertTrue(result.is_some)
        self.assertEqual(result.value, ["Id list cannot be nothing"])
        
        