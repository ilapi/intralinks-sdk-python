"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list, get_node_as_item
import urllib.request

def get_user_account2(api_client, email):
    response = api_client.get(
        '/v2/users/{}'.format(urllib.request.quote(email)),
        api_version=2
    )

    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_item(data, 'user')

def get_user_account(api_client, email, exchange_id):
    response = api_client.get(
        '/v2/workspaces/{}/users'.format(exchange_id), 
        params={'email': email},
        api_version=2
    )
    
    response.assert_status_code(200)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
         
    return get_node_as_item(data, 'users')

def create_user_account(api_client, email, first_name, last_name, organization, phone, language):
    new_global_user = {
        "email": email,
        "firstName": first_name,
        "lastName": last_name,
        "organization": organization,
        "officePhone": phone,
        "language": language
    }
    
    response = api_client.create(
        '/v2/users',
        data=json.dumps(new_global_user),
        headers={'Content-Type':'application/json'},
        api_version=2
    )
    
    response.assert_status_code(201)
    response.assert_content_type('application/json')
    response.assert_no_errors()
    
    data = response.data()
    
    return get_node_as_item(data, ['userPartials', 'userPartial'])