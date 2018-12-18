"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list
import json

def get_field_definitions(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/fieldDefinitions'.format(exchange_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    return get_node_as_list(data, 'fieldDefinitions')

def get_exchange_custom_fields(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/customFields'.format(exchange_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    return get_node_as_list(data, 'customFields')

def get_document_custom_fields(api_client, exchange_id, document_id):
    response = api_client.get(
        '/v2/workspaces/{}/documents/{}/customFields'.format(exchange_id, document_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    return get_node_as_list(data, 'customFields')

def get_folder_custom_fields(api_client, exchange_id, folder_id):
    response = api_client.get(
        '/v2/workspaces/{}/folders/{}/customFields'.format(exchange_id, folder_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()

    return get_node_as_list(data, 'customFields')

def get_group_custom_fields(api_client, exchange_id, group_id):
    response = api_client.get(
        '/v2/workspaces/{}/groups/{}/customFields'.format(exchange_id, group_id),
        api_version=2
    )
    
    response.check(200, 'application/json')

    data = response.data()

    return get_node_as_list(data, 'customFields')