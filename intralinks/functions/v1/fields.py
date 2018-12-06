"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list

def get_field_definitions(api_client, exchange_id):
    response = api_client.get(
        '/services/workspaces/fieldDefinitions', 
        params={
            'workspaceId':exchange_id
        },
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_list(data, ('fieldDefinitionList', 'fieldDefinition'))
