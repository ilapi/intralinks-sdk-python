"""
For educational purpose only
"""

from intralinks.utils.xml import to_xml

def get_splash(api_client, exchange_id):
    response = api_client.get(
        '/services/workspaces/entry', 
        params={'workspaceId':exchange_id},
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return data

def enter_exchange(api_client, exchange_id, accept_splash=None, one_time_password=False):
    if one_time_password:
        enter_content = {'xml':to_xml({'acceptSplash':accept_splash, 'oneTimePassword':one_time_password }, 'workspaceEntryRequest')}
    else:
        enter_content = {'xml':to_xml({'acceptSplash':accept_splash}, 'workspaceEntryRequest')}

    response = api_client.create(
        '/services/workspaces/entry', 
        params={
            'workspaceId':exchange_id
        }, 
        data=enter_content,
        api_version=1
    )

    data = response.data()

    return get_node_as_item(data, 'state')

def delete_exchange_entry(api_client, exchange_id):
    response = api_client.delete(
        '/services/workspaces/entry', 
        params={
            'workspaceId':exchange_id
        },
        api_version=1
    )

    data = response.data()

    return data


def download_splash_image(api_client, exchange_id, file_path_without_extension):
    response = api_client.get(
        '/services/workspaces/splashImage', 
        params={
            'workspaceId': exchange_id
        }, 
        stream=True,
        api_version=1
    )
    
    response.assert_status_code(200)
    
    extensions = {
        'image/jpeg':'.jpg',
        'image/gif':'.gif',
    }
    
    extension = extensions[response.headers['Content-Type']]
    
    with open(file_path_without_extension + extension, 'wb') as fp:
        response.dump(fp)
    
    return file_path_without_extension + extension