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
                self.b = '^time'
                self.c = '^.b'
                self.d = 'test_stringggg'
                self.e = None
                self.gear_cls_tree_path = 'arg.a'
        self.a = A()
