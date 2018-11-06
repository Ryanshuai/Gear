import os
import re

from gear_config.yaml_to_object import get_Cls, Cls
from gear_config.gear_cls_str_decoder import Decoder


def write_down_obj(obj, tab_num):
    function_str = '(?:[_a-zA-Z]\w*\\([$()]*\\))'
    base_function_pattern = re.compile(function_str)

    attr_list = dir(obj)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or callable(getattr(obj, x)) or x == ''), attr_list))

    father_name = obj.gear_cls_tree_path.split('.')[-1]

    line = "{}class {}(Cls):".format(tab_num*'    ', father_name.upper()); lines.append(line)
    line = "{}def __init__(self):".format((tab_num+1)*'    ', father_name.upper()); lines.append(line)
    line = "{}    super().__init__()".format((tab_num+1)*'    '); lines.append(line)

    cls_list = []
    build_in_list = []
    for attr in attr_list:
        if isinstance(getattr(obj, attr), Cls):
            cls_list.append(attr)
        else:
            build_in_list.append(attr)

    for attr in build_in_list:
        context = getattr(obj, attr)
        if isinstance(context, str) and base_function_pattern.search(context) is None:
            line = "{}self.{} = '{}'".format((tab_num+2)*'    ', attr, getattr(obj, attr)); lines.append(line)
        else:
            line = "{}self.{} = {}".format((tab_num+2)*'    ', attr, getattr(obj, attr)); lines.append(line)

    for attr in cls_list:
        write_down_obj(getattr(obj, attr), tab_num=tab_num+2)
        line = "{}self.{} = {}()".format((tab_num+2)*'    ', attr, attr.upper()); lines.append(line)

    return lines


cwd = os.getcwd()

yaml_wait_list = []

for fpathe, dirs, fs in os.walk(cwd):
    for f in fs:
        if f[-5:] == '.yaml':
            yaml_file = os.path.join(fpathe, f)
            # ch_time = os.stat(yaml_file).st_mtime
            yaml_wait_list.append(yaml_file)
# print(yaml_wait_list)


for yaml_file in yaml_wait_list:
    py_file_path = yaml_file[:-5]+'.py'

    arg = get_Cls(yaml_file)
    arg = Decoder(arg).decode()

    lines = []
    line = 'import os'; lines.append(line)
    line = 'import sys'; lines.append(line)
    line = 'import time'; lines.append(line)
    line = 'import warnings'; lines.append(line)
    line = 'from gear_config.yaml_to_object import Cls'; lines.append(line)
    line = ""; lines.append(line)
    line = ""; lines.append(line)


    write_down_obj(arg, tab_num=0)
    # for line in lines:
    #     print(line)

    with open(py_file_path, "w") as f:
        for line in lines:
            f.write(line)
            f.write('\n')


