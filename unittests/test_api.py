import datetime
import json
from unittest import TestCase
from unittest.mock import Mock, patch

from requests.models import Response

from dd_import.dd_api import Api


class TestApi(TestCase):

    def setUp(self):
        self.header = {'Content-type': 'application/json',
                       'Authorization': 'Token api_key'}

        self.header_without_json = {'Authorization': 'Token api_key'}

        self.product_type_id = 1
        self.product_id = 2
        self.engagement_id = 3
        self.test_id = 4
        self.test_type_id = 5

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_PRODUCT_TYPE_NAME': 'product_type'})
    def test_get_product_type_found(self, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 0, \"name\": \"product_type_dev\"}, {\"id\": 1, \"name\": \"product_type\"}]}'
        mockGet.return_value = response

        api = Api()
        id = api.get_product_type()

        self.assertEqual(id, self.product_type_id)
        url = 'https://example.com/api/v2/product_types/'
        payload = {'name': 'product_type'}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch('dd_import.dd_api.Api.new_product_type')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_PRODUCT_TYPE_NAME': 'product_type'})
    def test_get_product_type_not_found(self, mockNewProductType, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 1, \"results\": [{\"id\": 0, \"name\": \"product_type_dev\"}]}'
        mockGet.return_value = response
        mockNewProductType.return_value = self.product_type_id

        api = Api()
        id = api.get_product_type()

        self.assertEqual(id, self.product_type_id)
        url = 'https://example.com/api/v2/product_types/'
        payload = {'name': 'product_type'}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        response.raise_for_status.assert_called_once()
        mockNewProductType.assert_called_once_with('product_type')

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_PRODUCT_TYPE_NAME': 'product_type'})
    def test_new_product_type(self, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"id\": 1}'
        mockPost.return_value = response

        api = Api()
        id = api.new_product_type('product_type')

        self.assertEqual(id, self.product_type_id)
        url = 'https://example.com/api/v2/product_types/'
        payload = '{"name": "product_type"}'
        mockPost.assert_called_once_with(url, headers=self.header, data=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_PRODUCT_NAME': 'product'})
    def test_get_product_found(self, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 1, \"name\": \"product_dev\"}, {\"id\": 2, \"name\": \"product\"}]}'
        mockGet.return_value = response

        api = Api()
        id = api.get_product(self.product_type_id)

        self.assertEqual(id, self.product_id)
        url = 'https://example.com/api/v2/products/'
        payload = {'name': 'product', 'prod_type': self.product_type_id}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch('dd_import.dd_api.Api.new_product')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_PRODUCT_NAME': 'product'})
    def test_get_product_not_found(self, mockNewProduct, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 1, \"name\": \"product_dev\"}, {\"id\": 2, \"name\": \"product_prod\"}]}'
        mockGet.return_value = response
        mockNewProduct.return_value = self.product_id

        api = Api()
        id = api.get_product(self.product_type_id)

        self.assertEqual(id, self.product_id)
        url = 'https://example.com/api/v2/products/'
        payload = {'name': 'product', 'prod_type': self.product_type_id}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        mockNewProduct.assert_called_once_with(self.product_type_id)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_PRODUCT_NAME': 'product'})
    def test_new_product(self, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"id\": 2}'
        mockPost.return_value = response

        api = Api()
        id = api.new_product(self.product_type_id)

        self.assertEqual(id, self.product_id)
        url = 'https://example.com/api/v2/products/'
        payload = '{"name": "product", "description": "product", "prod_type": 1}'
        mockPost.assert_called_once_with(url, headers=self.header, data=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_ENGAGEMENT_NAME': 'engagement'})
    def test_get_engagement_found(self, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 2, \"name\": \"engagement_dev\"}, {\"id\": 3, \"name\": \"engagement\"}]}'
        mockGet.return_value = response

        api = Api()
        id = api.get_engagement(self.product_id)

        self.assertEqual(id, self.engagement_id)
        url = 'https://example.com/api/v2/engagements/'
        payload = {'name': 'engagement', 'product': self.product_id}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch('dd_import.dd_api.Api.new_engagement')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_ENGAGEMENT_NAME': 'engagement'})
    def test_get_engagement_not_found(self, mockNewEngagement, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 2, \"name\": \"engagement_dev\"}, {\"id\": 3, \"name\": \"engagement_prod\"}]}'
        mockGet.return_value = response
        mockNewEngagement.return_value = self.engagement_id

        api = Api()
        id = api.get_engagement(self.product_id)

        self.assertEqual(id, self.engagement_id)
        url = 'https://example.com/api/v2/engagements/'
        payload = {'name': 'engagement', 'product': self.product_id}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        mockNewEngagement.assert_called_once_with(self.product_id)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_ENGAGEMENT_NAME': 'engagement'})
    def test_new_engagement_without_target(self, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"id\": 3}'
        mockPost.return_value = response

        api = Api()
        id = api.new_engagement(self.product_id)

        self.assertEqual(id, self.engagement_id)
        today = datetime.date.today().isoformat()
        url = 'https://example.com/api/v2/engagements/'
        payload = f'{{"name": "engagement", "product": 2, "target_start": "{today}", "target_end": "2999-12-31", "engagement_type": "CI/CD", "status": "In Progress"}}'
        mockPost.assert_called_once_with(url, headers=self.header, data=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_ENGAGEMENT_NAME': 'engagement',
                               'DD_ENGAGEMENT_TARGET_START': '2023-02-01',
                               'DD_ENGAGEMENT_TARGET_END': '2023-02-28'})
    def test_new_engagement_with_target(self, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"id\": 3}'
        mockPost.return_value = response

        api = Api()
        id = api.new_engagement(self.product_id)

        self.assertEqual(id, self.engagement_id)
        url = 'https://example.com/api/v2/engagements/'
        payload = '{"name": "engagement", "product": 2, "target_start": "2023-02-01", "target_end": "2023-02-28", "engagement_type": "CI/CD", "status": "In Progress"}'
        mockPost.assert_called_once_with(url, headers=self.header, data=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_ENGAGEMENT_NAME': 'engagement',
                               'DD_SOURCE_CODE_MANAGEMENT_URI': 'https://github.com/MyOrg/MyProject/tree/main'})
    def test_new_engagement_with_source_code_management_uri(self, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"id\": 3}'
        mockPost.return_value = response

        api = Api()
        id = api.new_engagement(self.product_id)

        self.assertEqual(id, self.engagement_id)
        today = datetime.date.today().isoformat()
        url = 'https://example.com/api/v2/engagements/'
        payload = f'{{"name": "engagement", "product": 2, "target_start": "{today}", "target_end": "2999-12-31", "engagement_type": "CI/CD", "status": "In Progress", "source_code_management_uri": "https://github.com/MyOrg/MyProject/tree/main"}}'
        mockPost.assert_called_once_with(url, headers=self.header, data=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.patch')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_ENGAGEMENT_NAME': 'engagement'})
    def test_update_engagement_empty(self, mockPatch, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        mockPatch.return_value = response

        api = Api()
        api.update_engagement(self.engagement_id)

        mockPatch.assert_not_called()
        response.raise_for_status.assert_not_called()

    @patch('dd_import.environment.Environment')
    @patch('requests.patch')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_ENGAGEMENT_NAME': 'engagement',
                               'DD_BUILD_ID': 'build_id',
                               'DD_COMMIT_HASH': 'commit_hash',
                               'DD_BRANCH_TAG': 'branch_tag'})
    def test_update_engagement(self, mockPatch, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        mockPatch.return_value = response

        api = Api()
        api.update_engagement(self.engagement_id)

        url = 'https://example.com/api/v2/engagements/3/'
        payload = '{"build_id": "build_id", "commit_hash": "commit_hash", "branch_tag": "branch_tag"}'
        mockPatch.assert_called_once_with(url, headers=self.header, data=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_NAME': 'test'})
    def test_get_test_found(self, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 2}, {\"id\": 3, \"title\": \"test_dev\"}, {\"id\": 4, \"title\": \"test\"}]}'
        mockGet.return_value = response

        api = Api()
        id = api.get_test(self.engagement_id)

        self.assertEqual(id, self.test_id)
        url = 'https://example.com/api/v2/tests/'
        payload = {'title': 'test', 'engagement': self.engagement_id}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch('dd_import.dd_api.Api.new_test')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_NAME': 'test'})
    def test_get_test_not_found(self, mockNewTest, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 2}, {\"id\": 3, \"title\": \"test_dev\"}, {\"id\": 4, \"title\": \"test_prod\"}]}'
        mockGet.return_value = response
        mockNewTest.return_value = self.test_id

        api = Api()
        id = api.get_test(self.engagement_id)

        self.assertEqual(id, self.test_id)
        url = 'https://example.com/api/v2/tests/'
        payload = {'title': 'test', 'engagement': self.engagement_id}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        mockNewTest.assert_called_once_with(self.engagement_id)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch('dd_import.dd_api.Api.get_test_type')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_NAME': 'test'})
    def test_new_test(self, mockTestType, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"id\": 4}'
        mockPost.return_value = response
        mockTestType.return_value = self.test_type_id

        api = Api()
        id = api.new_test(self.engagement_id)

        self.assertEqual(id, self.test_id)
        url = 'https://example.com/api/v2/tests/'
        today = datetime.date.today()
        today = datetime.datetime(today.year, today.month, today.day)
        payload = {'title': 'test',
                   'engagement': self.engagement_id,
                   'target_start': today.isoformat(),
                   'target_end': datetime.datetime
                   .fromisoformat('2999-12-31').isoformat(),
                   'test_type': self.test_type_id}
        payload = json.dumps(payload)
        mockPost.assert_called_once_with(url, headers=self.header, data=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_TYPE_NAME': 'test_type'})
    def test_get_test_type_found(self, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 4, \"name\": \"test_type_dev\"}, {\"id\": 5, \"name\": \"test_type\"}]}'
        mockGet.return_value = response

        api = Api()
        id = api.get_test_type()

        self.assertEqual(id, self.test_type_id)
        url = 'https://example.com/api/v2/test_types/'
        payload = {'name': 'test_type'}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.get')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_TYPE_NAME': 'test_type'})
    def test_get_test_type_not_found(self, mockGet, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        response.text = '{\"count\": 2, \"results\": [{\"id\": 4, \"name\": \"test_type_dev\"}, {\"id\": 5, \"name\": \"test_type_prod\"}]}'
        mockGet.return_value = response

        with self.assertRaises(Exception) as cm:
            api = Api()
            api.get_test_type()

        self.assertEqual('Test type test_type not found', str(cm.exception))
        url = 'https://example.com/api/v2/test_types/'
        payload = {'name': 'test_type'}
        mockGet.assert_called_once_with(url, headers=self.header, params=payload, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_TYPE_NAME': 'test_type',
                               'DD_ACTIVE': 'True',
                               'DD_VERIFIED': 'true',
                               'DD_PUSH_TO_JIRA': 'true',
                               'DD_CLOSE_OLD_FINDINGS': 'true',
                               'DD_MINIMUM_SEVERITY': 'Info',
                               'DD_VERSION': 'version',
                               'DD_ENDPOINT_ID': '6',
                               'DD_SERVICE': 'service'})
    def test_reimport_findings_without_file(self, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        mockPost.return_value = response

        api = Api()
        api.reimport_scan(self.test_id)

        url = 'https://example.com/api/v2/reimport-scan/'
        payload = {'scan_date': datetime.date.today().isoformat(),
                   'scan_type': 'test_type',
                   'test': self.test_id,
                   'active': True,
                   'verified': True,
                   'push_to_jira': True,
                   'close_old_findings': True,
                   'close_old_findings_product_scope': False,
                   'do_not_reactivate': False,
                   'minimum_severity': 'Info',
                   'version': 'version',
                   'endpoint_to_add': 6,
                   'service': 'service'
                   }
        files = {}
        mockPost.assert_called_once_with(url, headers=self.header_without_json, data=payload, files=files, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch('builtins.open')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_TYPE_NAME': 'test_type',
                               'DD_ACTIVE': 'False',
                               'DD_VERIFIED': 'false',
                               'DD_PUSH_TO_JIRA': 'false',
                               'DD_CLOSE_OLD_FINDINGS': 'false',
                               'DD_CLOSE_OLD_FINDINGS_PRODUCT_SCOPE': 'true',
                               'DD_FILE_NAME': 'file_name'})
    def test_reimport_findings_with_file(self, mockOpen, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        mockPost.return_value = response
        mockOpen.return_value = 'file_open'

        api = Api()
        api.reimport_scan(self.test_id)

        url = 'https://example.com/api/v2/reimport-scan/'
        payload = {'scan_date': datetime.date.today().isoformat(),
                   'scan_type': 'test_type',
                   'test': self.test_id,
                   'active': False,
                   'verified': False,
                   'push_to_jira': False,
                   'close_old_findings': False,
                   'close_old_findings_product_scope': True,
                   'do_not_reactivate': False
                   }
        files = {'file': ('file_name', 'file_open', 'application/json', {'Expires': '0'})}
        mockPost.assert_called_once_with(url, headers=self.header_without_json, data=payload, files=files, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch('builtins.open')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_TYPE_NAME': 'test_type',
                               'DD_ACTIVE': 'False',
                               'DD_VERIFIED': 'false',
                               'DD_PUSH_TO_JIRA': 'false',
                               'DD_CLOSE_OLD_FINDINGS': 'false',
                               'DD_FILE_NAME': 'file_name',
                               'DD_SOURCE_CODE_MANAGEMENT_URI': 'https://github.com/MyOrg/MyProject/tree/main'})
    def test_reimport_findings_with_source_code_management_uri(self, mockOpen, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        mockPost.return_value = response
        mockOpen.return_value = 'file_open'

        api = Api()
        api.reimport_scan(self.test_id)

        url = 'https://example.com/api/v2/reimport-scan/'
        payload = {'scan_date': datetime.date.today().isoformat(),
                   'scan_type': 'test_type',
                   'test': self.test_id,
                   'active': False,
                   'verified': False,
                   'push_to_jira': False,
                   'close_old_findings': False,
                   'close_old_findings_product_scope': False,
                   'do_not_reactivate': False,
                   'source_code_management_uri': 'https://github.com/MyOrg/MyProject/tree/main'
                   }
        files = {'file': ('file_name', 'file_open', 'application/json', {'Expires': '0'})}
        mockPost.assert_called_once_with(url, headers=self.header_without_json, data=payload, files=files, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch('builtins.open')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_TEST_TYPE_NAME': 'test_type',
                               'DD_ACTIVE': 'False',
                               'DD_VERIFIED': 'false',
                               'DD_PUSH_TO_JIRA': 'false',
                               'DD_CLOSE_OLD_FINDINGS': 'false',
                               'DD_DO_NOT_REACTIVATE': 'true',
                               'DD_FILE_NAME': 'file_name',
                               'DD_SOURCE_CODE_MANAGEMENT_URI': 'https://github.com/MyOrg/MyProject/tree/main'})
    def test_reimport_findings_with_do_not_reactivate(self, mockOpen, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        mockPost.return_value = response
        mockOpen.return_value = 'file_open'

        api = Api()
        api.reimport_scan(self.test_id)

        url = 'https://example.com/api/v2/reimport-scan/'
        payload = {'scan_date': datetime.date.today().isoformat(),
                   'scan_type': 'test_type',
                   'test': self.test_id,
                   'active': False,
                   'verified': False,
                   'push_to_jira': False,
                   'close_old_findings': False,
                   'close_old_findings_product_scope': False,
                   'do_not_reactivate': True,
                   'source_code_management_uri': 'https://github.com/MyOrg/MyProject/tree/main'
                   }
        files = {'file': ('file_name', 'file_open', 'application/json', {'Expires': '0'})}
        mockPost.assert_called_once_with(url, headers=self.header_without_json, data=payload, files=files, verify=True)
        response.raise_for_status.assert_called_once()

    @patch('dd_import.environment.Environment')
    @patch('requests.post')
    @patch('builtins.open')
    @patch.dict('os.environ', {'DD_URL': 'https://example.com',
                               'DD_API_KEY': 'api_key',
                               'DD_FILE_NAME': 'file_name'})
    def test_import_languages(self, mockOpen, mockPost, mockEnv):
        response = Mock(spec=Response)
        response.status_code = 200
        mockPost.return_value = response
        mockOpen.return_value = 'file_open'

        api = Api()
        api.import_languages(self.product_id)

        url = 'https://example.com/api/v2/import-languages/'
        payload = {'product': self.product_id}
        files = {'file': ('file_name', 'file_open', 'application/json', {'Expires': '0'})}
        mockPost.assert_called_once_with(url, headers=self.header_without_json, data=payload, files=files, verify=True)
        response.raise_for_status.assert_called_once()
