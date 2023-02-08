import configparser 
import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.normpath(os.path.join(CURRENT_DIR, "../resources"))
CONFIG_FILE = "config.ini"
PARSER_FILE = "c.so"

FUNCTION_CHOOSE_P_KEY = 'FUNCTION_CHOOSE_P'
CONFIG_PATH = os.path.join(RESOURCES_DIR, CONFIG_FILE)
PARSER_PATH = os.path.join(RESOURCES_DIR, PARSER_FILE)

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

def get_config(key: str):
    return config['DEFAULT'][key]
