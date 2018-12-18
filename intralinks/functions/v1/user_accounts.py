"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item, entity_to_dict
from intralinks.utils.xml import to_xml

def get_user_account(api_client, email, exchange_id=None):
    response = api_client.get(
        '/services/users', 
        params={
            'emailId':email, 
            'workspaceId':exchange_id
        },
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return get_node_as_item(data, ('users', 'user'))

def search_directory_user(api_client, email, exchange_id):
    return get_user_account(api_client, email, exchange_id)

def create_user_account(api_client, user):
    user_data = entity_to_dict(user)

    response = api_client.create(
        '/services/users', 
        data={'xml':to_xml(user_data, ['user', 'userRequest'])},
        api_version=1
    )

    response.check(200, 'text/xml')
    
    data = response.data()
    
    return data