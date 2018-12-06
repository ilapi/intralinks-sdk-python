"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list

def get_permissions(api_client, exchange_id, document_id):
    response = api_client.get(
        '/v2/workspaces/{}/documents/{}/permissions'.format(exchange_id, document_id),
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_list(data, 'permissions')