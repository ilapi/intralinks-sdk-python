from bs4 import BeautifulSoup
import difflib
import intralinks
import datetime
import json
import hashlib

class CustomAlertManager:
    def __init__(self, il):
        self.il = il
        self.exchange_alerts = None
        self.template_alerts = None

    def load_exchange_alerts(self, exchange_ids, json_file_name=None):
        all_alerts =  []

        if isinstance(exchange_ids, int) or isinstance(exchange_ids, str):
            exchange_ids = [exchange_ids]

        for i in exchange_ids:
            print('Retrieving alerts for exchange {}'.format(i))

            alerts = intralinks.functions.v1.custom_alerts.get_custom_alerts(self.il.api_client, exchange_id=i)

            if alerts['customAlerts'] is not None:
                all_alerts.extend(alerts['customAlerts']['customAlert'])
        
        if json_file_name is not None:
            with open(json_file_name.format(datetime.datetime.today().strftime('%Y%m%d_%H%M%S')), 'w') as f:
                f.write(json.dumps(all_alerts))

        self.exchange_alerts = all_alerts

    def load_template_alerts(self, template_ids, json_file_name=None):
        all_alerts =  []

        if isinstance(template_ids, int) or isinstance(template_ids, str):
            template_ids = [template_ids]

        for i in template_ids:
            print('Retrieving alerts for template {}'.format(i))

            alerts = intralinks.functions.v1.custom_alerts.get_custom_alerts(self.il.api_client, template_id=i)

            if alerts['customAlerts'] is not None:
                all_alerts.extend(alerts['customAlerts']['customAlert'])
        
        if json_file_name is not None:
            with open(json_file_name.format(datetime.datetime.today().strftime('%Y%m%d_%H%M%S')), 'w') as f:
                f.write(json.dumps(all_alerts))

        self.template_alerts = all_alerts

    def extract_text(self, a):
        soup = BeautifulSoup(a, 'html.parser')
        return '\n'.join([l for l in [l.strip() for l in soup.body.get_text().split('\n')] if l != ''])

    def digest_text(self, s, size=3):
        d = hashlib.sha256(s.encode('utf-8')).hexdigest()
        return d[:size]

    def diff_text(self, t1, t2):
        for line in difflib.context_diff(t1.split('\n'), t2.split('\n')):
            print(line)