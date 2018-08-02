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

def data_indexer(data, index=0, pop=False):
    if pop:
        return { row[index] : row[:index] + row[index+1:]
            for row in data }
    return { row[index] : row for row in data }

def data_filter(data, column, val):
    return [ d for d in data if d[column] == val ]

def data_labeller(data, labels):
    return { labels[data.index(d)] : d for d in data }

def unique_on_fields(data, fields=[]):
    wrapped = [ (frozenset([ row[field] for field in fields ]), row)
                    for row in data ]
    checked = set()
    filtered = []
    for w in wrapped:
        if w[0] in checked:
            continue
        else:
            filtered.append(w[1])
            checked.add(w[0])
    return filtered