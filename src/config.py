from configparser import ConfigParser


class Config:
    parser = ConfigParser()

    def __init__(self, file_name='application.ini'):
        self.file_name = file_name
        self.parser.read(file_name)

    def section(self, section):
        return self.parser[section]

    def get(self, section, key):
        return self.parser[section][key]

    def get_int(self, section, key):
        return int(self.get(section, key))
