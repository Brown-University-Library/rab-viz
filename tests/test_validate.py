import unittest
import context

from rabviz.etl.validate import validate_data, validate_dataset

class TestDataSetValidators(unittest.TestCase):

    def test_validate_Invalid(self):
        invalid = validate_dataset.Invalid('test')
        self.assertEqual(invalid._msg, 'test')
        self.assertTrue(invalid.invalid)

    def test_validate_header(self):
        expected = [ 'foo', 'bar' ]
        dataset = [ [ 'foo', 'bar' ], [ 1,2 ], [ 3,4 ] ]
        valid = validate_dataset.header(dataset, expected)
        self.assertEqual( len(valid), len(dataset)-1 )
        self.assertEqual( valid[0], dataset[1] )

        bad_data = [ [ 'bar', 'foo' ], [ 1,2 ], [ 3,4 ] ]
        invalid = validate_dataset.header(bad_data, expected)
        self.assertEqual( len(invalid), 1)
        self.assertIsInstance( invalid[0], validate_dataset.Invalid )
        self.assertEqual( invalid[0]._msg, "Failed: header")

    def test_validate_unique(self):
        dataset = [ [1, 'foo', 'bar'], [2, 'baz', 'bot'] ]
        valid = validate_dataset.unique(dataset, 0)
        self.assertEqual( valid, dataset )

        bad_data = [ [3, 'beep'], [3, 'boop'] ]
        invalid = validate_dataset.unique(bad_data, 0)
        self.assertEqual( len(invalid), 1 )
        self.assertIsInstance( invalid[0], validate_dataset.Invalid )

    def test_column_equality(self):
        dataset = [ [ 1, 2, 'foo'], [ 2, 1, 'bar'] ]
        valid = validate_dataset.column_equality(dataset, 0, 1)
        self.assertEqual( valid, dataset )

        bad_data = [ [1, 2, 'foo'] , [ 2, 3, 'bar'] ]
        invalid = validate_dataset.column_equality(bad_data, 0, 1)
        self.assertEqual( len(invalid), 1 )
        self.assertIsInstance( invalid[0], validate_dataset.Invalid )

class TestDataValidators(unittest.TestCase):

    def test_validate_Invalid(self):
        invalid = validate_data.Invalid('test')
        self.assertEqual(invalid._msg, 'test')
        self.assertTrue(invalid.invalid)
    
    def test_validate_required(self):
        required = [ 0, 2 ]
        data = [ 'd', '', 'f' ]
        valid = validate_data.required(data, required)
        self.assertEqual( len(valid), len(data) )
        self.assertEqual( valid[0], data[0] )
        
        required = [ 2, 0 ]
        valid = validate_data.required(data, required)
        self.assertEqual( len(valid), len(data) )
        self.assertEqual( valid[0], data[0] )

        bad_data = ['a', 'b', '']
        invalid = validate_data.required(bad_data, required)
        self.assertIsInstance( invalid, validate_data.Invalid)
        bad_data = ['a']
        invalid = validate_data.required(bad_data, required)
        self.assertIsInstance( invalid, validate_data.Invalid)

    def test_validate_shortid_uri(self):
        data =  [ 'http://vivo.brown.edu/individual/steve' ]
        valid = validate_data.shortid_uri(data, 0)
        self.assertEqual( valid, data )

        bad_data = [ 'http:/baduri' ]
        invalid = validate_data.shortid_uri(bad_data,0)
        self.assertIsInstance(invalid, validate_data.Invalid)


if __name__ == "__main__":
    unittest.main()