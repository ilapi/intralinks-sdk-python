"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list

def get_batches(api_client, exchange_id, operation_type="Bulk Upload"):
    response = api_client.get(
        '/v2/workspaces/{}/batches'.format(exchange_id),
        params={'operationType':operation_type},
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()

    return get_node_as_list(data, 'batches')

def get_batch_items(api_client, exchange_id, batch_id):
    response = api_client.get(
        '/v2/workspaces/{}/batches/{}'.format(exchange_id, batch_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()

    return get_node_as_list(data, ['batchItemsResponse', 'contentList'])

def create_batch(api_client, exchange_id, type, size):
    raise Exception()