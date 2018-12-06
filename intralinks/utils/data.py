def get_node(data, path):
    assert path is not None

    if data is None:
        return None
        
    if isinstance(path, str):
        path = [path]

    for k in path:
        if data is not None:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return None
        else:
            return None
    
    return data

def as_list(data):
    if data is None:
        return []

    elif isinstance(data, list):
        return data

    else:
        return [data]

def get_node_as_list(data, path):
    return as_list(get_node(data, path))

def get_node_as_item(data, path):
    l = get_node_as_list(data, path)
    assert len(l) <= 1
    return l[0] if len(l) == 1 else None

def strip_dict(d):
    return {k:v for k,v in d.items() if v is not None}

def entity_to_dict(entity):
    return strip_dict(entity._asdict()) if isinstance(entity, tuple) else entity.copy()

def filter_dict(d, keep_fields=None, remove_fields=None):
    if keep_fields is None:
        keep_fields = list(d.keys())
    
    if remove_fields is None:
        remove_fields = set()
    
    return {k:d[k] for k in keep_fields if k in d and k not in remove_fields}

def chunks(l, n):
    """
    Yield successive n-sized chunks from l.
    
    https://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks
    """
    for i in range(0, len(l), n):
        yield l[i:i + n]