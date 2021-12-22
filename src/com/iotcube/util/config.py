#-*- coding: utf-8 -*-
import configparser

class Config(object):
    config = None
    configList = []
    configFile = '/workspace/src/config.ini'
    
    def __new__(cls):
        if not hasattr(cls,'instance'):
            cls.config = configparser.ConfigParser()
            cls.config.read(cls.configFile)
            cls.configList = cls.config.sections()
            cls.instance = super(Config, cls).__new__(cls)
        return cls.instance

    def getConfig(cls, category, key):
        return cls.config[category][key]

    def toString(cls):
        with open(cls.configFile, 'r') as f:
            return f.read()
        