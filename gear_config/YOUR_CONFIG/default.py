import os
import sys
import time
import warnings
from gear_config.yaml_to_object import Cls


class ARG(Cls):
    def __init__(self):
        super().__init__()
        self.gear_cls_tree_path = 'arg'
        class A(Cls):
            def __init__(self):
                super().__init__()
                self.b = 'time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))'
                self.c = 'time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))'
                self.d = 'test_stringggg'
                self.e = '$'
                self.gear_cls_tree_path = 'arg.a'
        self.a = A()
