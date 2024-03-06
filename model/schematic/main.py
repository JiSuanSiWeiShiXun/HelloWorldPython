# coding=utf-8
'''
@File    :   main.py
@Time    :   2024/03/05 11:14:50
@Author  :   youling 
@Contact :   xiezhihong@kingsoft.com
@Desc    :   None
'''
from schematics.models import Model
from schematics.types import *
from schematics.types.compound import *

class Git(object):
    pass

class File(object):
    pass

class CreateInfo(Model):
    name = StringType()
    note = StringType()
    case = PolyModelType([Git, File])
    packages = StringType()
    gameid = StringType()
