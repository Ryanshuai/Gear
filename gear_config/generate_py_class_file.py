import os
import re

from yaml_to_object import get_Cls, Cls


def write_down_obj(obj, tab_num):
    attr_list = dir(obj)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or callable(getattr(obj, x)) or x == ''), attr_list))

    father_name = obj.gear_cls_tree_path.split('.')[-1]

    line = "{}class {}(Cls):".format(tab_num*'    ', father_name.upper()); lines.append(line)
    line = "{}def __init__(self):".format((tab_num+1)*'    ', father_name.upper()); lines.append(line)
    line = "{}    super().__init__()".format((tab_num+1)*'    '); lines.append(line)

    # if tab_num == 0:
    #     line = 8*' '+"class STAMP(Cls):"; lines.append(line)
    #     line = 8*' '+"    def __init__(self):"; lines.append(line)
    #     line = 8*' '+"        super().__init__()"; lines.append(line)
    #     line = 8*' '+"        self.config_name = config_name"; lines.append(line)
    #     line = 8*' '+"        self.user = user"; lines.append(line)
    #     line = 8*' '+"        if self.user == 'none':"; lines.append(line)
    #     line = 8*' '+"            warnings.warn('gear warning: cannot find your user name, please insert in user list or specify it', DeprecationWarning)"; lines.append(line)
    #     line = 8*' '+"        self.time = time"; lines.append(line)
    #     line = 8*' '+"        self.experiment_name = experiment_name"; lines.append(line)
    #     line = 8*' '+"self.stamp = STAMP()"; lines.append(line)

    cls_list = []
    build_in_list = []
    for attr in attr_list:
        if isinstance(getattr(obj, attr), Cls):
            cls_list.append(attr)
        else:
            build_in_list.append(attr)

    for attr in build_in_list:
        if isinstance(getattr(obj, attr), str):
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
            ch_time = os.stat(yaml_file).st_mtime
            yaml_wait_list.append(yaml_file)
# print(yaml_wait_list)

yaml_file = yaml_wait_list[0]
arg = get_Cls(yaml_file)

py_file_path = yaml_file[:-5]+'.py'


for yaml_file in yaml_wait_list:
    py_file_path = yaml_file[:-5]+'.py'

    arg = get_Cls(yaml_file)

    lines = []
    line = 'import os'; lines.append(line)
    line = 'import sys'; lines.append(line)
    line = 'import time'; lines.append(line)
    line = 'import warnings'; lines.append(line)
    line = 'from gear_config.yaml_to_object import Cls'; lines.append(line)
    # line = ''; lines.append(line)
    # line = ''; lines.append(line)
    # line = "config_name = os.path.basename(sys.argv[0])"; lines.append(line)
    # line = "user_list = list(filter(lambda user: os.path.exists('/root/' + user), user_list))"; lines.append(line)
    # line = "if len(user_list) == 0:"; lines.append(line)
    # line = "    user_list = list(filter(lambda user: os.path.exists('/home/' + user), user_list))"; lines.append(line)
    # line = "if len(user_list) == 0:"; lines.append(line)
    # line = "    user = 'none'"; lines.append(line)
    # line = "else:"; lines.append(line)
    # line = "    user = user_list[0]"; lines.append(line)
    # line = "time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))"; lines.append(line)
    # line = "experiment_name = user + '-' + config_name + '-' + time"; lines.append(line)
    line = ""; lines.append(line)
    line = ""; lines.append(line)


    write_down_obj(arg, tab_num=0)
    # for line in lines:
    #     print(line)

    with open(py_file_path, "w") as f:
        for line in lines:
            f.write(line)
            f.write('\n')


