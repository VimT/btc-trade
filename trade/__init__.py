from . import TA
from .core import Trade
from .global_fun import *
from .constant import *

import configparser

cf = configparser.ConfigParser()
cf.read('config.ini')

exchange = Trade()
