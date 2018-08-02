import datetime

def data_generator(keys, data, func):
    i = 0
    while i < len(keys):
        key = keys[i]
        key_data = func(key, data)
        ts = datetime.datetime.now()
        yield (key, ts, key_data)
        i += 1

def row_reducer(row, indexer=[]):
    return [ row[i] for i in indexer ]

def data_indexer(data, index=0):
    return { row[index] : row for row in data }

def data_filter(data, column, val):
    return [ d for d in data if d[column] == val ]