"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, entity_to_dict
from intralinks.utils.xml import to_xml
import intralinks.functions.entities
import os.path

def get_documents(api_client, exchange_id):
    response = api_client.get(
        '/services/workspaces/documents', 
        params={
            'workspaceId':exchange_id
        },
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, 'document')

def download_file(api_client, exchange_id, document_id, file_path):
    raise Exception()

def upload_file(api_client, exchange_id, document_id, version, file_path):
    raise Exception()

def get_access_statuses(api_client, exchange_id, document_id, max_retries=5):
    response = api_client.get(
        '/services/workspaces/documents/reports/documentAccessReport',
        params={
            'workspaceId': exchange_id,
            'documentId': document_id
        },
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return data['reportResponse']

def create_document(api_client, exchange_id, document, file=None, permissions=None, batch_id=None):
    document_data = entity_to_dict(document)
    
    data = {'document':document_data}

    if permissions:
        if isinstance(permissions, list):
            data['permissions'] = {'permissioned':[{'permissionInfo':p} for p in permissions]}
        else:
            data['permissions'] = {'permissioned':{'permissionInfo':permissions}}

    files = {'documentFile':(os.path.basename(file.name), file, 'application/octet-stream')} if file is not None else None

    response = api_client.create(
        '/services/workspaces/documents', 
        params={
            'workspaceId':exchange_id,
            'batchId':batch_id,
        }, 
        data={'xml':''.join(to_xml(data, ['documentCreate', 'documentCreateRequest']))},
        files=files,
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()
    
    data = response.data()
    
    return data['documentPartial']

def create_documents(api_client, exchange_id, documents, batch_id=None):
    keys = {'name', 'parentId', 'note', 'effectiveDate'}

    created_documents = [{k:d[k] for k in keys if k in d} for d in documents]

    xml_data = ['<documentCreateRequest>']

    for f in created_documents:
        xml_data.append(to_xml(f, ['document', 'documentCreate']))
    
    xml_data.append('</documentCreateRequest>')

    response = api_client.create(
        '/services/workspaces/documents', 
        params={
            'workspaceId':exchange_id,
            'batchId':batch_id,
        }, 
        data={'xml':''.join(xml_data)},
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()
    
    data = response.data()
    
    return data['documentPartial']

def update_document(api_client, exchange_id, document, file=None, permissions=None):
    document_data = entity_to_dict(document)
    
    data = {'document':document_data}

    if permissions:
        if isinstance(permissions, list):
            data['permissions'] = {'permissioned':[{'permissionInfo':p} for p in permissions]}
        else:
            data['permissions'] = {'permissioned':{'permissionInfo':permissions}}

    files = {'documentFile':(os.path.basename(file.name), file, 'application/octet-stream')} if file is not None else None

    response = api_client.update(
        '/services/workspaces/documents', 
        params={
            'workspaceId':exchange_id
        }, 
        data={'xml':''.join(to_xml(data, 'documentUpdateRequest'))},
        files=files,
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()
    
    data = response.data()
    
    return data['documentPartial']

def delete_document(api_client, exchange_id, id, version):   
    documents = [{'id':id, 'version':version}]

    return delete_documents(api_client, exchange_id, documents)

def delete_documents(api_client, exchange_id, documents): 
    deleted_documents = [
        {
            'id':g['id'], 
            'version':g['version'], 
            'type':'DOCUMENT'
        } for g in documents
    ]
     
    response = api_client.delete(
        '/v1/services/workspaces/folders/items', 
        params={
            'workspaceId':exchange_id,
            'deleteFolderContents':True
        }, 
        data={'xml':to_xml(deleted_documents, ['entityId', 'folderItemsDeleteRequest'])},
        api_version=1
    )
    
    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()
    
    return data