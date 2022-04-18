import configparser
from dataclasses import dataclass
import string

conf = configparser.ConfigParser()
conf.read('config.ini')

class GenConf:
    def __init__(self, conf) -> None:
        for key,value in conf['general'].items():
            setattr(self,key,value)

class EmailConf:
    def __init__(self, conf) -> None:
        for key,value in conf['email'].items():
            setattr(self,key,value)

class JoplinConf:
    def __init__(self,conf) -> None:
        for key,value in conf['joplin'].items():
            setattr(self,key,value)

genConf = GenConf(conf)
emailConf = EmailConf(conf)
joplinConf = JoplinConf(conf)
