def data_generator(keys, data, func):
    i = 0
    while i < len(keys):
        key = keys[i]
        key_data = func(key, data)
        yield (key, key_data)
        i += 1

def row_reducer(row, indexer=[]):
    return [ row[i] for i in indexer ]

def data_indexer(data, index=0):
    return { row[index] : row for row in data }