import re

class Invalid:
    def __init__(self, msg):
        self._msg = msg
        self.invalid = True

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

@data_validator
def required(row, required):
    for r in required:
        assert bool(row[r]) is True
    return [ r for r in row ]

@data_validator
def shortid_uri(row, idx):
    uri_re = re.compile('^http://vivo.brown.edu/individual/[a-z0-9]{2,10}$')
    assert uri_re.match(row[idx])
    return [ r for r in row ]

@data_validator
def rab_uri(row, idx):
    uri_re = re.compile('^http://vivo.brown.edu/individual/[a-z0-9-]{2,}$')
    assert uri_re.match(row[idx])
    return [ r for r in row ]