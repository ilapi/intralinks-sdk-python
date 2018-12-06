"""
For educational purpose only
"""

from intralinks.utils.xml import to_xml

class AlertResourceType:
    EXCHANGE = 9
    TEMPLATE = 8

class AlertType:
    NEW_DOCUMENT_SINGLE = 0
    NEW_DOCUMENT_BULK = 2
    NEW_DOCUMENT_MULTIFILE = 145
    WELCOME_USER_NEW = 113
    WELCOME_USER_EXISTING = 109

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

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return data

def set_custom_alerts(api_client, custom_alert):
    response = api_client.create(
        '/services/customAlerts', 
        data={'xml':to_xml({'customAlerts':{'customAlert':custom_alert}}, 'customAlertCreateRequest')},
        api_version=1
    )

    response.assert_status_code(200)
    response.assert_content_type('text/xml')
    response.assert_no_errors()

    data = response.data()

    return data
