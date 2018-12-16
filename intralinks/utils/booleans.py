def convert_to_bool(o, f):
    if isinstance(o, list):
        for e in o:
            convert_to_bool(e, f)

    elif isinstance(o, dict):
        if f in o and o[f] in {'T', 'F'}:
            o[f] = o[f] == 'T'