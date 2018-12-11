def test_get_exchanges(il, test_data):
    es = il.get_exchanges()
    assert len(es) > 1 

    exchange_by_id = {e['id']:e for e in es}
    assert test_data['exchange.id'] in exchange_by_id

    e = exchange_by_id[test_data['exchange.id']]
    assert e['workspaceName'] == 'API Unit Test'

def test_get_exchange(il, test_data):
    #%% [markdown]
    # Get the exchange for unit test
    #%%
    e = il.get_exchange(test_data['exchange.id'])
    assert e['workspaceName'] == 'API Unit Test'
    assert 'description' not in e

    #%% [markdown]
    # Update the exchange for unit test

    #%%
    e['workspaceName'] = 'Temp'
    e['description'] = 'une description'
    e = il.update_exchange(e)
    assert e['workspaceName'] == 'Temp'
    assert e['description'] == 'une description'

    #%% [markdown]
    # Get the exchange again an check it has been properly updated

    #%%
    e = il.get_exchange(6115625)
    assert e['workspaceName'] == 'Temp'
    assert e['description'] == 'une description'

    #%% [markdown]
    # Update the exchange to the initial state (esp. by removing the description)

    #%%
    e['workspaceName'] = 'API Unit Test'
    e['description'] = ''
    e = il.update_exchange(e)
    assert e['workspaceName'] == 'API Unit Test'
    assert e['description'] == ''

    #%% [markdown]
    # Get the exchange again an check it has been properly updated

    #%%
    e = il.get_exchange(6115625)
    assert e['workspaceName'] == 'API Unit Test'
    assert 'description' not in e