"""
For educational purpose only
"""

from intralinks.utils.data import get_node_as_list
from intralinks.utils.xml import to_xml

def get_alert_details(api_client, exchange_id, alert_type=None):
    response = api_client.get(
        '/services/workspaces/alertText', 
        params={
            'workspaceId':exchange_id,
            'workspaceAlertType':alert_type
        },
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return get_node_as_list(data, 'alertText')

