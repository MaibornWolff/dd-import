from unittest import TestCase
from unittest.mock import patch

from dd_import.dd_import_languages import dd_import_languages


class TestImportLanguages(TestCase):

    @patch('dd_import.environment.Environment.check_environment_languages')
    @patch('dd_import.dd_api.Api.get_product_type')
    @patch('dd_import.dd_api.Api.get_product')
    @patch('dd_import.dd_api.Api.import_languages')
    @patch.dict('os.environ', {'DD_URL': 'url', 'DD_API_KEY': 'api_key'})
    def test_dd_import_languages(self, mockApiIL, mockApiP, mockApiPT, mockEnv):
        mockApiPT.return_value = 1
        mockApiP.return_value = 2

        dd_import_languages()

        mockEnv.assert_called_once()
        mockApiPT.assert_called_once()
        mockApiP.assert_called_once_with(1)
        mockApiIL.assert_called_once_with(2)
