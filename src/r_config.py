import configparser

class Read:
    def __init__(self, config_file = 'config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def get_default(self, key):
        with open('config.ini', 'r') as f:
            for line in f:
                if line.startswith(key):
                    return line.split('=')[1].strip()