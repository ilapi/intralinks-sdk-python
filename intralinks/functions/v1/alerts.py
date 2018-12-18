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

    response.check(200, 'text/xml')

    data = response.data()

    return get_node_as_list(data, 'alertText')

