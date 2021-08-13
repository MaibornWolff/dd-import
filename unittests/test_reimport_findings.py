from unittest import TestCase
from unittest.mock import patch

from dd_import.dd_reimport_findings import dd_reimport_findings


class TestReimportFindings(TestCase):

    @patch('dd_import.environment.Environment.check_environment_reimport_findings')
    @patch('dd_import.dd_api.Api.get_product_type')
    @patch('dd_import.dd_api.Api.get_product')
    @patch('dd_import.dd_api.Api.get_engagement')
    @patch('dd_import.dd_api.Api.get_test')
    @patch('dd_import.dd_api.Api.reimport_scan')
    @patch.dict('os.environ', {'DD_URL': 'url', 'DD_API_KEY': 'api_key'})
    def test_dd_reimport_findings(self, mockApiRS, mockApiT, mockApiE, mockApiP, mockApiPT, mockEnv):
        mockApiPT.return_value = 1
        mockApiP.return_value = 2
        mockApiE.return_value = 3
        mockApiT.return_value = 4

        dd_reimport_findings()

        mockEnv.assert_called_once()
        mockApiPT.assert_called_once()
        mockApiP.assert_called_once_with(1)
        mockApiE.assert_called_once_with(2)
        mockApiT.assert_called_once_with(3)
        mockApiRS.assert_called_once_with(4)
