
class Invalid:
    def __init__(self, msg):
        self._msg = msg
        self.invalid = True

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
def header(data, expected):
    header = data[0]
    assert header == expected
    return data[1:]

@dataset_validator
def unique(data, keyIndex):
    keys = [ d[keyIndex] for d in data ]
    unique = set(keys)
    assert len(keys) == len(unique)
    return [ d for d in data ]

@dataset_validator
def column_equality(data, col1Index, col2Index):
    col1 = { d[col1Index] for d in data }
    col2 = { d[col2Index] for d in data }
    assert col1 == col2
    return [ d for d in data ]