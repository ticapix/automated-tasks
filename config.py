import configparser
import os


rootpath = os.path.abspath(os.path.dirname(__file__))

config = configparser.ConfigParser()
config.read(os.path.join(rootpath, 'config.ini'))
