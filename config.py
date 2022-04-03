import configparser
from dataclasses import dataclass
import string

conf = configparser.ConfigParser()
conf.read('config.ini')

class EmailConf:
    def __init__(self, conf) -> None:
        for key,value in conf['email'].items():
            setattr(self,key,value)

class JoplinConf:
    def __init__(self,conf) -> None:
        for key,value in conf['joplin'].items():
            setattr(self,key,value)

emailConf = EmailConf(conf)
joplinConf = JoplinConf(conf)
