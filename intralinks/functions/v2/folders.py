"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, filter_dict, entity_to_dict
import intralinks.functions.entities
import json

def get_folders(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/folders'.format(exchange_id),
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    result = get_node_as_list(data, 'folder')

    for r in result:
        if 'hasNote' in r and r['hasNote'] in {'T', 'F'}:
            r['hasNote'] = r['hasNote'] == 'T'

    return result

def create_folder(api_client, exchange_id, folder):
    folder_data = entity_to_dict(folder)
    
    response = api_client.create(
        '/v2/workspaces/{}/folders'.format(exchange_id),
        data=json.dumps({'folders':[{'folder':folder_data}]}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.assert_status_code(201)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    result = get_node_as_item(data, 'folderPartial')

    if 'hasNote' in result and result['hasNote'] in {'T', 'F'}:
        result['hasNote'] = result['hasNote'] == 'T'

    return result

def create_folders(api_client, exchange_id, folders):
    raise Exception()
    
def update_folder(api_client, exchange_id, folder):
    folder_data = entity_to_dict(folder)
    folder_data = filter_dict(folder_data, remove_fields={'isEmailin', 'versionNumber', 'isFavorite', 'lastModifiedBy', 'lastModifiedOn', 'createdBy', 'createdOn', 'hasChildFolders', 'orderNumber', 'indexNumber'})
    
    response = api_client.update(
        '/v2/workspaces/{}/folders'.format(exchange_id),
        data=json.dumps({'folders':[folder_data]}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.assert_status_code(202)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    result = get_node_as_item(data, 'folderPartial')
    
    if 'hasNote' in result and result['hasNote'] in {'T', 'F'}:
        result['hasNote'] = result['hasNote'] == 'T'

    return result

def delete_folder(api_client, exchange_id, id, version, delete_folder_contents=True):
    response = api_client.delete(
        '/v2/workspaces/{}/folders/{}'.format(exchange_id, id),
        params={
            'version':version, 
            'deleteFolderContents': 'true' if delete_folder_contents else 'false'
        },
        api_version=2
    )
    
    response.assert_status_code(202)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return data
    
def delete_folders(api_client, exchange_id, folders):
    raise Exception()