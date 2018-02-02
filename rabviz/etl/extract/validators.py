import re


class Invalid:
    def __init__(self, msg):
        self._msg = msg

def data_validator(validator_func):
    def wrapper(datum, *args, **kwargs):
        try:
            return validator_func(datum, *args, **kwargs)
        except:
            if isinstance(datum, Invalid):
                return datum
            else:
                return Invalid("Failed: " + validator_func.__name__)
    return wrapper

def dataset_validator(validator_func):
    def wrapper(dataset, *args, **kwargs):
        try:
            return validator_func(dataset, *args, **kwargs)
        except:
            if isinstance(dataset[0], Invalid):
                return dataset
            else:
                return [ Invalid("Failed: " + validator_func.__name__) ]
    return wrapper

@dataset_validator
def validate_header(data, expected):
    header = data[0]
    assert header == expected
    return data[1:]

@dataset_validator
def validate_unique(data, keyIndex):
    keys = [ d[keyIndex] for d in data ]
    unique = set(keys)
    assert len(keys) == len(unique)
    return [ d for d in data ]

@dataset_validator
def validate_column_equality(data, col1Index, col2Index):
    col1 = { d[col1Index] for d in data }
    col2 = { d[col2Index] for d in data }
    assert col1 == col2
    return [ d for d in data ]

@data_validator
def validate_required(row, required):
    for r in required:
        assert bool(row[r]) is True
    return [ r for r in row ]

@data_validator
def validate_shortid_uri(row, idx):
    uri_re = re.compile('^http://vivo.brown.edu/individual/[a-z0-9]{2,10}$')
    assert uri_re.match(row[idx])
    return [ r for r in row ]

@data_validator
def validate_rab_uri(row, idx):
    uri_re = re.compile('^http://vivo.brown.edu/individual/[a-z0-9\-]{2,}$')
    assert uri_re.match(row[idx])
    return [ r for r in row ]