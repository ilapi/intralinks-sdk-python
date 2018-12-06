"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, entity_to_dict
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

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, ('users', 'user'))[0]

def search_directory_user(api_client, email, exchange_id):
    return get_user_account(api_client, email, exchange_id)

def create_user_account(api_client, user):
    user_data = entity_to_dict(user)

    response = api_client.create(
        '/services/users', 
        data={'xml':to_xml(user_data, ['user', 'userRequest'])},
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()
    
    data = response.data()
    
    return data