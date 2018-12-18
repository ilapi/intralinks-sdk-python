"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, entity_to_dict
from intralinks.utils.xml import to_xml
import intralinks.functions.entities

def get_folders(api_client, exchange_id, folder_id=None):
    """
        Does not retrieve the note
    """
    response = api_client.get(
        '/services/workspaces/folders', 
        params={
            'workspaceId':exchange_id,
            'folderId':folder_id
        },
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return get_node_as_list(data, 'folder')

def get_folder(api_client, exchange_id, folder_id):
    folders = get_folder(api_client, exchange_id, folder_id)
    return folders[0] if len(folders) == 1 else None

def get_folder_with_note(api_client, exchange_id, folder_id):
    response = api_client.get(
        '/services/workspaces/folders/note', 
        params={
            'workspaceId':exchange_id,
            'folderId':folder_id
        },
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return get_node(data, 'folderNote')

def create_folder(api_client, exchange_id, folder):
    folder_data = entity_to_dict(folder)

    response = api_client.create(
        '/v1/services/workspaces/folders', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':to_xml(folder_data, ['folder', 'folderCreate', 'folderCreateRequest'])},
        api_version=1
    )
    
    response.check(200, 'text/xml')

    data = response.data()
    
    return get_node_as_item(data, 'folderPartial')

def create_folders(api_client, exchange_id, folders):
    created_folders = [entity_to_dict(f) for f in folders]

    xml_data = ['<folderCreateRequest>']

    for f in created_folders:
        xml_data.append(to_xml(f, ['folder', 'folderCreate']))
    
    xml_data.append('</folderCreateRequest>')

    response = api_client.create(
        '/v1/services/workspaces/folders', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':''.join(xml_data)},
        api_version=1
    )

    response.check(200, 'text/xml')
    
    data = response.data()
    
    return get_node_as_list(data, 'folderPartial')

def update_folder(api_client, exchange_id, folder):
    folder_data = entity_to_dict(folder)

    response = api_client.update(
        '/v1/services/workspaces/folders', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':to_xml(folder_data, ['folder', 'folderUpdateRequest'])},
        api_version=1
    )
    
    response.check(200, 'text/xml')

    data = response.data()
    
    return get_node_as_item(data, 'folderPartial')

def delete_folder(api_client, exchange_id, folder):   
    return delete_folders(api_client, exchange_id, [folder])

def delete_folders(api_client, exchange_id, folders): 
    deleted_folders = [
        {
            'id':f['id'], 
            'version':f['version'], 
            'type':'FOLDER'
        } for f in folders
    ]
     
    response = api_client.delete(
        '/v1/services/workspaces/folders/items', 
        params={
            'workspaceId':exchange_id,
            'deleteFolderContents':True
        }, 
        data={'xml':to_xml(deleted_folders, ['entityId', 'folderItemsDeleteRequest'])},
        api_version=1
    )
    
    response.check(200, 'text/xml')

    data = response.data()
    
    return data