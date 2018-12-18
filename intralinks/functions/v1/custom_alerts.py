"""
For educational purpose only
"""

from intralinks.functions.entities import AlertResourceType
from intralinks.utils.data import get_node_as_list
from intralinks.utils.xml import to_xml

def get_custom_alerts(api_client, exchange_id=None, template_id=None, alert_type=None, alert_locale=None):
    params = {
        'alertTypeId': alert_type,
        'locale':alert_locale
    }

    if exchange_id is not None:
        params['resourceId'] = exchange_id
        params['resourceTypeId'] = AlertResourceType.EXCHANGE

    elif template_id is not None:
        params['resourceId'] = template_id
        params['resourceTypeId'] = AlertResourceType.TEMPLATE

    response = api_client.get(
        '/services/customAlerts', 
        params=params,
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return get_node_as_list(data, ('customAlerts', 'customAlert'))

def set_custom_alerts(api_client, custom_alert):
    response = api_client.create(
        '/services/customAlerts', 
        data={'xml':to_xml({'customAlerts':{'customAlert':custom_alert}}, 'customAlertCreateRequest')},
        api_version=1
    )

    response.check(200, 'text/xml')

    data = response.data()

    return data
