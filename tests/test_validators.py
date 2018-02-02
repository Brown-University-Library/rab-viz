import unittest
import context

from rabviz.etl.extract import validators

class TestExtractValidators(unittest.TestCase):

    def test_validate_header(self):
        expected = [ 'foo', 'bar' ]
        dataset = [ [ 'foo', 'bar' ], [ 1,2 ], [ 3,4 ] ]
        valid = validators.validate_header(dataset, expected)
        self.assertEqual( len(valid), len(dataset)-1 )
        self.assertEqual( valid[0], dataset[1] )

        bad_data = [ [ 'bar', 'foo' ], [ 1,2 ], [ 3,4 ] ]
        invalid = validators.validate_header(bad_data, expected)
        self.assertEqual( len(invalid), 1)
        self.assertIsInstance( invalid[0], validators.Invalid )
        self.assertEqual( invalid[0]._msg, "Failed: validate_header")

    def test_validate_required(self):
        required = [ 0, 2 ]
        data = [ 'd', '', 'f' ]
        valid = validators.validate_required(data, required)
        self.assertEqual( len(valid), len(data) )
        self.assertEqual( valid[0], data[0] )
        
        required = [ 2, 0 ]
        valid = validators.validate_required(data, required)
        self.assertEqual( len(valid), len(data) )
        self.assertEqual( valid[0], data[0] )

        bad_data = ['a', 'b', '']
        invalid = validators.validate_required(bad_data, required)
        self.assertIsInstance( invalid, validators.Invalid)
        bad_data = ['a']
        invalid = validators.validate_required(bad_data, required)
        self.assertIsInstance( invalid, validators.Invalid)

    def test_validate_uri(self):
        data =  [ 'http://vivo.brown.edu/individual/steve' ]
        valid = validators.validate_uri(data, 0)
        self.assertEqual( valid, data )

        bad_data = [ 'http:/baduri' ]
        invalid = validators.validate_uri(bad_data,0)
        self.assertIsInstance(invalid, validators.Invalid)

    def test_validate_unique(self):
        dataset = [ [1, 'foo', 'bar'], [2, 'baz', 'bot'] ]
        valid = validators.validate_unique(dataset, 0)
        self.assertEqual( valid, dataset )

        bad_data = [ [3, 'beep'], [3, 'boop'] ]
        invalid = validators.validate_unique(bad_data, 0)
        self.assertEqual( len(invalid), 1 )
        self.assertIsInstance( invalid[0], validators.Invalid )

    def test_column_equality(self):
        dataset = [ [ 1, 2, 'foo'], [ 2, 1, 'bar'] ]
        valid = validators.validate_column_equality(dataset, 0, 1)
        self.assertEqual( valid, dataset )

        bad_data = [ [1, 2, 'foo'] , [ 2, 3, 'bar'] ]
        invalid = validators.validate_column_equality(bad_data, 0, 1)
        self.assertEqual( len(invalid), 1 )
        self.assertIsInstance( invalid[0], validators.Invalid )

if __name__ == "__main__":
    unittest.main()