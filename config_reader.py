import configparser 

FUNCTION_CHOOSE_P_KEY = 'FUNCTION_CHOOSE_P'

config = configparser.ConfigParser()
config.read('config.ini')


def get_config(key: str):
    return config['DEFAULT'][key]
