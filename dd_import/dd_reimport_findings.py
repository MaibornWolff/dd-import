from dd_import.dd_api import Api
from dd_import.environment import Environment


def dd_reimport_findings():
    try:
        environment = Environment()
        environment.check_environment_reimport_findings()
        api = Api()
        product_type_id = api.get_product_type()
        product_id = api.get_product(product_type_id)
        engagement_id = api.get_engagement(product_id)
        test_id = api.get_test(engagement_id)
        api.reimport_scan(test_id)
        api.update_engagement(engagement_id)
    except Exception as e:
        print(str(e))
        exit(1)


if __name__ == '__main__':
    dd_reimport_findings()
