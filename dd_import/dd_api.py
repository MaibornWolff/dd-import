import datetime
import json

import requests
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

from dd_import.environment import Environment

# Disable SSL Warnings
disable_warnings(InsecureRequestWarning)


class Api:

    def __init__(self):
        self.environment = Environment()
        self.headers = {'Content-type': 'application/json',
                        'Authorization': 'Token ' + self.environment.api_key}
        self.headers_without_json = {'Authorization':
                                     'Token ' + self.environment.api_key}
        self.product_type_url = self.environment.url + '/api/v2/product_types/'
        self.product_url = self.environment.url + '/api/v2/products/'
        self.engagement_url = self.environment.url + '/api/v2/engagements/'
        self.test_url = self.environment.url + '/api/v2/tests/'
        self.test_type_url = self.environment.url + '/api/v2/test_types/'
        self.reimport_scan_url = self.environment.url + '/api/v2/reimport-scan/'
        self.import_languages_url = self.environment.url + '/api/v2/import-languages/'
        self.ssl_verification = self.environment.ssl_verification

    def get_product_type(self):
        payload = {'name': self.environment.product_type_name}
        r = requests.get(self.product_type_url,
                         headers=self.headers,
                         params=payload,
                         verify=self.ssl_verification)
        r.raise_for_status()
        product_type_data = json.loads(r.text)
        for product_type in product_type_data.get('results', []):
            if product_type.get('name', '') == self.environment.product_type_name:
                product_type_id = product_type['id']
                print('Product type found, id: ', product_type_id)
                return product_type_id
        raise Exception(f'Product type {self.environment.product_type_name} not found')

    def get_product(self, product_type):
        payload = {'name': self.environment.product_name,
                   'prod_type': product_type}
        r = requests.get(self.product_url,
                         headers=self.headers,
                         params=payload,
                         verify=self.ssl_verification)
        r.raise_for_status()
        product_data = json.loads(r.text)
        for product in product_data.get('results', []):
            if product.get('name', '') == self.environment.product_name:
                product_id = product['id']
                print('Product found,      id: ', product_id)
                return product_id
        return self.new_product(product_type)

    def new_product(self, product_type):
        payload = {'name': self.environment.product_name,
                   'description': self.environment.product_name,
                   'prod_type': product_type}
        r = requests.post(self.product_url,
                          headers=self.headers,
                          data=json.dumps(payload),
                          verify=self.ssl_verification)
        r.raise_for_status()
        product_data = json.loads(r.text)
        print('New product,        id: ', product_data['id'])
        return product_data['id']

    def get_engagement(self, product):
        payload = {'name': self.environment.engagement_name,
                   'product': product}
        r = requests.get(self.engagement_url,
                         headers=self.headers,
                         params=payload,
                         verify=self.ssl_verification)
        r.raise_for_status()
        engagement_data = json.loads(r.text)
        for engagement in engagement_data.get('results', []):
            if engagement.get('name', '') == self.environment.engagement_name:
                engagement_id = engagement['id']
                print('Engagement found,   id: ', engagement_id)
                return engagement_id
        return self.new_engagement(product)

    def new_engagement(self, product):
        payload = {'name': self.environment.engagement_name,
                   'product': product,
                   'target_start': datetime.date.today().isoformat(),
                   'target_end': '2999-12-31',
                   'engagement_type': 'CI/CD',
                   'status': 'In Progress'}
        r = requests.post(self.engagement_url,
                          headers=self.headers,
                          data=json.dumps(payload),
                          verify=self.ssl_verification)
        r.raise_for_status()
        engagement_data = json.loads(r.text)
        print('New engagement,     id: ', engagement_data['id'])
        return engagement_data['id']

    def update_engagement(self, engagement):
        if self.environment.build_id is not None or \
           self.environment.commit_hash is not None or \
           self.environment.branch_tag is not None:
            payload = {'build_id': self.environment.build_id,
                       'commit_hash': self.environment.commit_hash,
                       'branch_tag': self.environment.branch_tag}
            r = requests.patch(self.engagement_url + str(engagement) + '/',
                               headers=self.headers,
                               data=json.dumps(payload),
                               verify=self.ssl_verification)
            r.raise_for_status()

    def get_test(self, engagement):
        payload = {'title': self.environment.test_name,
                   'engagement': engagement}
        r = requests.get(self.test_url,
                         headers=self.headers,
                         params=payload,
                         verify=self.ssl_verification)
        r.raise_for_status()
        test_data = json.loads(r.text)
        for test in test_data.get('results', []):
            if test.get('title', '') == self.environment.test_name:
                test_id = test['id']
                print('Test found,         id: ', test_id)
                return test_id
        return self.new_test(engagement)

    def new_test(self, engagement):
        today = datetime.date.today()
        today = datetime.datetime(today.year, today.month, today.day)
        payload = {'title': self.environment.test_name,
                   'engagement': engagement,
                   'target_start': today.isoformat(),
                   'target_end': datetime.datetime
                   .fromisoformat('2999-12-31').isoformat(),
                   'test_type': self.get_test_type()}
        r = requests.post(self.test_url,
                          headers=self.headers,
                          data=json.dumps(payload),
                          verify=self.ssl_verification)
        r.raise_for_status()
        test_data = json.loads(r.text)
        print('New test,           id: ', test_data['id'])
        return test_data['id']

    def get_test_type(self):
        payload = {'name': self.environment.test_type_name}
        r = requests.get(self.test_type_url,
                         headers=self.headers,
                         params=payload,
                         verify=self.ssl_verification)
        r.raise_for_status()
        test_type_data = json.loads(r.text)
        for test_type in test_type_data.get('results', []):
            if test_type.get('name', '') == self.environment.test_type_name:
                return test_type['id']
        raise Exception(f'Test type {self.environment.test_type_name} not found')

    def reimport_scan(self, test):
        payload = {'scan_date': datetime.date.today().isoformat(),
                   'scan_type': self.environment.test_type_name,
                   'test': test,
                   'active': self.environment.active,
                   'verified': self.environment.verified,
                   'push_to_jira': self.environment.push_to_jira,
                   'close_old_findings': self.environment.close_old_findings,
                   }
        if self.environment.minimum_severity is not None:
            payload['minimum_severity'] = self.environment.minimum_severity
        if self.environment.version is not None:
            payload['version'] = self.environment.version
        if self.environment.endpoint_id is not None:
            payload['endpoint_to_add'] = int(self.environment.endpoint_id)
        if self.environment.service is not None:
            payload['service'] = self.environment.service
        if self.environment.api_scan_configuration_id is not None:
            payload['api_scan_configuration'] = self.environment.api_scan_configuration_id

        if self.environment.file_name is not None:
            files = {'file': (self.environment.file_name,
                              open(self.environment.file_name, 'rb'),
                              'application/json', {'Expires': '0'})}
            response = requests.post(self.reimport_scan_url,
                                     headers=self.headers_without_json,
                                     data=payload,
                                     files=files,
                                     verify=self.ssl_verification)
        else:
            response = requests.post(self.reimport_scan_url,
                                     headers=self.headers_without_json,
                                     data=payload,
                                     verify=self.ssl_verification)

        response.raise_for_status()

        print()
        print('Scan results imported')

    def import_languages(self, product):
        payload = {'product': product}
        files = {'file': (self.environment.file_name,
                 open(self.environment.file_name, 'rb'),
                 'application/json', {'Expires': '0'})}

        response = requests.post(self.import_languages_url,
                                 headers=self.headers_without_json,
                                 data=payload,
                                 files=files,
                                 verify=self.ssl_verification)
        response.raise_for_status()

        print()
        print('Languages imported')
