import intralinks_test.exchanges_helper

def test_get_exchanges(v2_client, test_data):
    intralinks_test.exchanges_helper.test_get_exchanges(v2_client, test_data)

def test_get_exchange(v2_client, test_data):
    intralinks_test.exchanges_helper.test_get_exchange(v2_client, test_data)