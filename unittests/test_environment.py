from unittest import TestCase
from unittest.mock import patch

from dd_import.environment import Environment


class TestEnvironment(TestCase):

    def test_check_environment_reimport_findings_empty(self):

        with self.assertRaises(Exception) as cm:
            environment = Environment()
            environment.check_environment_reimport_findings()

        self.assertEqual('DD_URL is missing / DD_API_KEY is missing / DD_PRODUCT_TYPE_NAME is missing / DD_PRODUCT_NAME is missing / DD_ENGAGEMENT_NAME is missing / DD_TEST_NAME is missing / DD_TEST_TYPE_NAME is missing', str(cm.exception))
        self.assertTrue(environment.active)
        self.assertTrue(environment.verified)
        self.assertFalse(environment.push_to_jira)
        self.assertTrue(environment.close_old_findings)

    @patch.dict('os.environ', {'DD_URL': 'url',
                               'DD_API_KEY': 'api_key',
                               'DD_PRODUCT_TYPE_NAME': 'product_type',
                               'DD_PRODUCT_NAME': 'product',
                               'DD_ENGAGEMENT_NAME': 'engagement',
                               'DD_TEST_NAME': 'test',
                               'DD_TEST_TYPE_NAME': 'test_type',
                               'DD_FILE_NAME': 'file_name',
                               'DD_ACTIVE': 'False',
                               'DD_VERIFIED': 'False',
                               'DD_MINIMUM_SEVERITY': 'minimum_severity',
                               'DD_PUSH_TO_JIRA': 'True',
                               'DD_CLOSE_OLD_FINDINGS': 'False',
                               'DD_VERSION': 'version',
                               'DD_ENDPOINT_ID': 'endpoint_id',
                               'DD_BUILD_ID': 'build_id',
                               'DD_COMMIT_HASH': 'commit_hash',
                               'DD_BRANCH_TAG': 'branch_tag'})
    def test_check_environment_reimport_findings_complete(self):

        environment = Environment()
        environment.check_environment_reimport_findings()

        self.assertEqual(environment.url, 'url')
        self.assertEqual(environment.api_key, 'api_key')
        self.assertEqual(environment.product_type_name, 'product_type')
        self.assertEqual(environment.product_name, 'product')
        self.assertEqual(environment.engagement_name, 'engagement')
        self.assertEqual(environment.test_name, 'test')
        self.assertEqual(environment.test_type_name, 'test_type')
        self.assertEqual(environment.file_name, 'file_name')
        self.assertEqual(environment.url, 'url')
        self.assertFalse(environment.active)
        self.assertFalse(environment.verified)
        self.assertEqual(environment.minimum_severity, 'minimum_severity')
        self.assertTrue(environment.push_to_jira)
        self.assertFalse(environment.close_old_findings)
        self.assertEqual(environment.version, 'version')
        self.assertEqual(environment.endpoint_id, 'endpoint_id')
        self.assertEqual(environment.build_id, 'build_id')
        self.assertEqual(environment.commit_hash, 'commit_hash')
        self.assertEqual(environment.branch_tag, 'branch_tag')

    def test_check_environment_languages_empty(self):
        with self.assertRaises(Exception) as cm:
            environment = Environment()
            environment.check_environment_languages()
        self.assertEqual('DD_URL is missing / DD_API_KEY is missing / DD_PRODUCT_TYPE_NAME is missing / DD_PRODUCT_NAME is missing / DD_FILE_NAME is missing', str(cm.exception))
        self.assertTrue(environment.active)
        self.assertTrue(environment.verified)
        self.assertFalse(environment.push_to_jira)
        self.assertTrue(environment.close_old_findings)

    @patch.dict('os.environ', {'DD_URL': 'url',
                               'DD_API_KEY': 'api_key',
                               'DD_PRODUCT_TYPE_NAME': 'product_type',
                               'DD_PRODUCT_NAME': 'product',
                               'DD_FILE_NAME': 'file_name'})
    def test_check_environment_languages_complete(self):

        environment = Environment()
        environment.check_environment_languages()

        self.assertEqual(environment.url, 'url')
        self.assertEqual(environment.api_key, 'api_key')
        self.assertEqual(environment.product_type_name, 'product_type')
        self.assertEqual(environment.product_name, 'product')
        self.assertEqual(environment.file_name, 'file_name')
