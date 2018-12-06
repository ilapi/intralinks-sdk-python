
import hashlib
import base64
import math

def hash_file(file_name, buffer_size=64*1024):
    """
    From https://gist.github.com/formido/821003
    From https://stackoverflow.com/questions/22058048/hashing-a-file-in-python
    """
    hasher = hashlib.sha1()
    
    with open(file_name, 'rb') as f:
        while True:
            data = f.read(buffer_size)
            if not data:
                break
            hasher.update(data)
    
    return base64.b64encode(hasher.digest()).decode('ascii')

def count_pages(document):
    return document['pageCount'] if document['pageCount'] > 0 else math.ceil(document['fileSize'] / (65 * 1024))