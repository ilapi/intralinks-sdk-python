import pytest
import json
import intralinks.tools.login_manager
import intralinks

def load_intralinks_client_from_session_data(file_path):
    il = intralinks.IntralinksClient()
    login_manager = intralinks.tools.login_manager.LoginManager(il)
    session_data = login_manager.load_session_data(file_path)
    login_manager.set_api_client(session_data)
    return il

@pytest.fixture(scope="module")
def v1_client():
    return load_intralinks_client_from_session_data('data/unittest_v1_session.json')

@pytest.fixture(scope="module")
def v2_client():
    return load_intralinks_client_from_session_data('data/unittest_v2_session.json')

@pytest.fixture(scope="module")
def test_data():
    try:
        with open('unit_test_data.json', 'r') as f:
            data = json.load(f)
    except:
        data = {
            'exchange.id': 1111111111,
            'exchange.owner.email': 'donald.trup@whitehouse.com',
            'exchange.new_user.email': 'john.doe@bigcorp.com',
            'exchange.new_user.first_name': 'John',
            'exchange.new_user.last_name': 'Doe'
        }
    
    return data

def test_exchange(il, unit_test_data):
    e = il.get_exchange(unit_test_data['exchange.id'])
    
    assert e['workspaceName'] == 'API Unit Test'
    assert 'description' not in e

    return e