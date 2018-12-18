"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, entity_to_dict
import intralinks.functions.entities
import time
import json

def get_documents(api_client, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/documents'.format(exchange_id),
        api_version=2
    )
    
    response.check(200, 'application/json')
    
    data = response.data()
    
    return get_node_as_list(data, 'document')

def download_file(api_client, exchange_id, document_id, file_path):
    response = api_client.get(
        '/v2/workspaces/{}/documents/{}/file'.format(exchange_id, document_id), 
        stream=True,
        api_version=2
    )
    
    response.assert_status_code(200)
    
    with open(file_path, 'wb') as fp:
        response.dump(fp)

def create_document(api_client, exchange_id, document, batch_id=None):
    l = create_documents(api_client, exchange_id, [document], batch_id)
    return l[0] if len(l) > 0 else None

def create_documents(api_client, exchange_id, documents, batch_id=None):
    document_data = [{'document':entity_to_dict(d)} for d in documents]
    
    response = api_client.create(
        '/v2/workspaces/{}/documents'.format(exchange_id), 
        params={'batch_id': batch_id},
        data=json.dumps({'documents':document_data}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(201, 'application/json')
    
    data = response.data()
    
    return get_node_as_list(data, 'documentPartial')

def update_document(api_client, exchange_id, document):
    document_data = entity_to_dict(document)
    
    response = api_client.update(
        '/v2/workspaces/{}/documents'.format(exchange_id), 
        data=json.dumps({'documents':[document_data]}), 
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return get_node_as_item(data, 'documentPartial')

def delete_document(api_client, exchange_id, document):
    return delete_documents(api_client, exchange_id, [document])

def delete_documents(api_client, exchange_id, documents):
    document_data = [{'id':d['id'], 'version':d['version']} for d in documents]

    response = api_client.delete(
        '/v2/workspaces/{}/documents'.format(exchange_id),
        data=json.dumps({'documents':document_data}),
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.check(202, 'application/json')
    
    data = response.data()
    
    return data


def upload_file(api_client, exchange_id, document_id, version, file_path):
    with open(file_path, 'rb') as fp:
        response = api_client.update(
            '/v2/workspaces/{}/documents/{}/file'.format(exchange_id, document_id), 
            params={'version':version}, 
            files={'documentFile': fp},
            api_version=2
        )
        
        response.check(202, 'application/json')
    
    data = response.data()
    
    return data

def get_access_statuses(api_client, exchange_id, document_id, max_retries=5):
    count = 1
    
    while True:
        response = api_client.get(
            '/v2/workspaces/{}/documents/{}/accessReport'.format(exchange_id, document_id),
            api_version=2
        )
        
        response.check(200, 'application/json')
        
        data = response.data()
        
        if 'docAccessInfo' not in data:
            if 'subcode' in data and data['subcode'] == '9-9-9-1':
                count += 1

                if count > max_retries:
                    raise Exception(response.url, response.text)
                else:
                    print('--- Access statuses for document #{} - Retry #{} ---'.format(document_id, count))
                    time.sleep(5)
            else:
                raise Exception(response.url, response.text)
        
        else:
            access_info = data['docAccessInfo']
            
            return access_info