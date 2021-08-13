from dd_import.dd_api import Api
from dd_import.environment import Environment


def dd_import_languages():
    try:
        environment = Environment()
        environment.check_environment_languages()
        api = Api()
        product_type_id = api.get_product_type()
        product_id = api.get_product(product_type_id)
        api.import_languages(product_id)
    except Exception as e:
        print(str(e))
        exit(1)


if __name__ == '__main__':
    dd_import_languages()
