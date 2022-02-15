import configparser

def get_param(param):
    config = configparser.ConfigParser()
    config.sections()
    config.read('defects4all.ini')
    return config['DEFAULT'][param]




