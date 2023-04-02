# coding=utf-8
"""
objected oriented inotify component
"""
from typing import List

class CoredumpGuard(object):
    def __init__(self,
                 monitor_directory: List[str]):
        self.path = monitor_directory
        
