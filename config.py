import configparser
from singleton import singleton
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'conf.ini')


@singleton
class Config(object):
    _config = configparser.ConfigParser()
    _config.read(CONFIG_FILE, encoding='utf-8')
    SOURCE_CONN = dict(TYPE=_config['SOURCE']['DBTYPE'],
                       HOST=_config['SOURCE']['HOST'],
                       USER=_config['SOURCE']['USER'],
                       PORT=_config['SOURCE']['PORT'],
                       PASSWORD=_config['SOURCE']['PASSWORD'],
                       SCHEMA=_config['SOURCE']['SCHEMA'],
                       SID=_config['SOURCE']['SID'])
    TARGET_CONN = dict(TYPE=_config['TARGET']['DBTYPE'],
                       HOST=_config['TARGET']['HOST'],
                       USER=_config['TARGET']['USER'],
                       PORT=_config['TARGET']['PORT'],
                       SCHEMA=_config['TARGET']['SCHEMA'],
                       SID=_config['TARGET']['SID'])
    RUNTIME_CONFIG = dict(BUFFER=_config['CONFIG']['BUFFER'],
                          THREADS=_config['CONFIG']['THREADS'])
