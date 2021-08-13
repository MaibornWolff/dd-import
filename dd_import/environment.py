import os


class Environment:

    def __init__(self):
        self.url = os.getenv('DD_URL')
        self.api_key = os.getenv('DD_API_KEY')
        self.product_name = os.getenv('DD_PRODUCT_NAME')
        self.product_type_name = os.getenv('DD_PRODUCT_TYPE_NAME')
        self.engagement_name = os.getenv('DD_ENGAGEMENT_NAME')
        self.test_name = os.getenv('DD_TEST_NAME')
        self.test_type_name = os.getenv('DD_TEST_TYPE_NAME')
        self.file_name = os.getenv('DD_FILE_NAME')
        self.active = os.getenv('DD_ACTIVE', 'True').lower() in ['true']
        self.verified = os.getenv('DD_VERIFIED', 'True').lower() in ['true']
        self.minimum_severity = os.getenv('DD_MINIMUM_SEVERITY', None)
        self.push_to_jira = os.getenv('DD_PUSH_TO_JIRA', 'False').lower() in ['true']
        self.close_old_findings = os.getenv('DD_CLOSE_OLD_FINDINGS', 'True').lower() in ['true']
        self.version = os.getenv('DD_VERSION', None)
        self.endpoint_id = os.getenv('DD_ENDPOINT_ID', None)
        self.build_id = os.getenv('DD_BUILD_ID', None)
        self.commit_hash = os.getenv('DD_COMMIT_HASH', None)
        self.branch_tag = os.getenv('DD_BRANCH_TAG', None)

    def check_environment_reimport_findings(self):
        error_string = self.check_environment_common()
        if self.engagement_name is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'DD_ENGAGEMENT_NAME is missing'
        if self.test_name is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'DD_TEST_NAME is missing'
        if self.test_type_name is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'DD_TEST_TYPE_NAME is missing'

        if len(error_string) > 0:
            raise Exception(error_string)

        print('DD_URL:                ', self.url)
        print('DD_PRODUCT_TYPE_NAME:  ', self.product_type_name)
        print('DD_PRODUCT_NAME:       ', self.product_name)
        print('DD_ENGAGEMENT_NAME:    ', self.engagement_name)
        print('DD_TEST_NAME:          ', self.test_name)
        print('DD_TEST_TYPE_NAME:     ', self.test_type_name)
        print('DD_FILE_NAME:          ', self.file_name)
        print('DD_ACTIVE:             ', self.active)
        print('DD_VERIFIED :          ', self.verified)
        print('DD_MINIMUM_SEVERITY:   ', self.minimum_severity)
        print('DD_PUSH_TO_JIRA:       ', self.push_to_jira)
        print('DD_CLOSE_OLD_FINDINGS: ', self.close_old_findings)
        print('DD_VERSION:            ', self.version)
        print('DD_ENDPOINT_ID:        ', self.endpoint_id)
        print('DD_BUILD_ID:           ', self.build_id)
        print('DD_COMMIT_HASH:        ', self.commit_hash)
        print('DD_BRANCH_TAG:         ', self.branch_tag)
        print('')

    def check_environment_languages(self):
        error_string = self.check_environment_common()

        if self.file_name is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'DD_FILE_NAME is missing'

        if len(error_string) > 0:
            raise Exception(error_string)

        print('DD_URL:                ', self.url)
        print('DD_PRODUCT_TYPE_NAME:  ', self.product_type_name)
        print('DD_PRODUCT_NAME:       ', self.product_name)
        print('DD_FILE_NAME:          ', self.file_name)
        print('')

    def check_environment_common(self):
        error_string = ''
        if self.url is None:
            error_string = 'DD_URL is missing'
        if self.api_key is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'DD_API_KEY is missing'
        if self.product_type_name is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'DD_PRODUCT_TYPE_NAME is missing'
        if self.product_name is None:
            if error_string != '':
                error_string = error_string + ' / '
            error_string = error_string + 'DD_PRODUCT_NAME is missing'

        return error_string
