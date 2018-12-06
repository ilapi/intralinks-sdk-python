import pytest
from intralinks.utils.data import *

def test_get_node():
    assert get_node(None, 'path') is None

    assert get_node({'path':336}, 'path') == 336

    assert get_node({'path':336}, ['path']) == 336

    assert get_node({'path1':{'path2':336}}, ['path1', 'path2']) == 336

    assert get_node({'path':336}, 'other_path') is None

    assert get_node({'path':336}, ['other_path']) is None

    assert get_node({'path':336}, ['path', 'other_path']) is None

    assert get_node({'path1':{'path2':336}}, ['other_path']) is None

    assert get_node({'path1':{'path2':336}}, ['other_path', 'other_subpath']) is None

    assert get_node({'path1':{'path2':336}}, ['path1', 'other_path']) is None



def test_as_list():
    pass

def test_get_node_as_list():
    pass