import os
from configparser import ConfigParser, NoOptionError


class Properties:
    _base_dir = os.path.dirname(os.path.dirname(__file__))
    _name = None
    _instance = None
    _config = None

    @staticmethod
    def default_instance():
        if Properties._instance is None:
            Properties._instance = Properties("app.properties")
        return Properties._instance

    def __init__(self, name):
        self._name = name
        self.reload()

    def reload(self):
        new_config = ConfigParser()
        new_config.read(os.path.join(self._base_dir, self._name), encoding="UTF-8")
        self._config = new_config

    def get(self, section, key):
        try:
            return self._config.get(section, key)
        except NoOptionError:
            return None
