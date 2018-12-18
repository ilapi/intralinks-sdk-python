"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list

def get_permissions(api_client, exchange_id, document_id):
    response = api_client.get(
        '/v2/workspaces/{}/documents/{}/permissions'.format(exchange_id, document_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    return get_node_as_list(data, 'permissions')