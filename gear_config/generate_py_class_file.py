import os
import time

from yaml_to_object import get_Cls, Cls


def write_down_obj(obj, father_name, tab_num):
    attr_list = dir(obj)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or callable(getattr(obj, x)) or x == ''), attr_list))

    line = "{}class {}(Cls):".format(tab_num*'    ', father_name.upper()); lines.append(line)
    line = "{}def __init__(self):".format((tab_num+1)*'    ', father_name.upper()); lines.append(line)
    line = "{}    super().__init__()".format((tab_num+1)*'    '); lines.append(line)

    if tab_num == 0:
        line = 8*' '+"class GEAR_STAMP(Cls):"; lines.append(line)
        line = 8*' '+"    def __init__(self):"; lines.append(line)
        line = 8*' '+"        super().__init__()"; lines.append(line)
        line = 8*' '+"        self.gear_config_name = gear_config_name"; lines.append(line)
        line = 8*' '+"        self.gear_user = gear_user"; lines.append(line)
        line = 8*' '+"        if self.gear_user == 'none':"; lines.append(line)
        line = 8*' '+"            warnings.warn('gear warning: cannot find your user name, please insert in user list or specify it', DeprecationWarning)"; lines.append(line)
        line = 8*' '+"        self.gear_time = gear_time"; lines.append(line)
        line = 8*' '+"        self.gear_experiment_name = gear_experiment_name"; lines.append(line)
        line = 8*' '+"self.gear_stamp = GEAR_STAMP()"; lines.append(line)

    variable_list = []
    function_list = []
    for attr in attr_list:
        if not isinstance(getattr(obj, attr), Cls):
            variable_list.append(attr)
        else:
            function_list.append(attr)

    if 'gear_save_root' in variable_list:
        attr = 'gear_save_root'
        line = "{}self.{} = '{}'".format((tab_num + 2) * '    ', attr, getattr(obj, attr)); lines.append(line)
        variable_list.remove('gear_save_root')
        line = "{}self.root = join(self.gear_save_root, gear_experiment_name)".format((tab_num + 2) * '    '); lines.append(line)
        if 'root' in variable_list:
            variable_list.remove('root')

    if 'root' in variable_list:
        attr = 'root'
        line = "{}self.{} = '{}'".format((tab_num + 2) * '    ', attr, getattr(obj, attr)); lines.append(line)
        variable_list.remove('root')

    for attr in variable_list:
        if attr[0: 9] == 'relative_':
            if obj.root is None and hasattr(obj, 'gear_save_root') and obj.gear_save_root is None:
                print("gear warning:{} don't have corresponding root".format(attr))
            line = "{}self.{} = '{}'".format((tab_num + 2) * '    ', attr, getattr(obj, attr)); lines.append(line)
            line = "{}self.{} = join(self.root, '{}')".format((tab_num + 2) * '    ', attr[9:], getattr(obj, attr)); lines.append(line)
            variable_list = [ele for ele in variable_list if ele != attr]
            variable_list = [ele for ele in variable_list if ele != attr[9:]]

    for attr in variable_list:
        if isinstance(getattr(obj, attr), str):
            line = "{}self.{} = '{}'".format((tab_num+2)*'    ', attr, getattr(obj, attr)); lines.append(line)
        else:
            line = "{}self.{} = {}".format((tab_num+2)*'    ', attr, getattr(obj, attr)); lines.append(line)

    for attr in function_list:
        write_down_obj(getattr(obj, attr), attr, tab_num=tab_num+2)
        line = "{}self.{} = {}()".format((tab_num+2)*'    ', attr, attr.upper()); lines.append(line)

    return lines


now_time = time.time()
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
    line = 'from os.path import join'; lines.append(line)
    line = 'import sys'; lines.append(line)
    line = 'import time'; lines.append(line)
    line = 'import warnings'; lines.append(line)
    line = 'from ..config_utils import gear_user_list'; lines.append(line)
    line = 'from ..yaml_to_object import Cls'; lines.append(line)
    line = ''; lines.append(line)
    line = ''; lines.append(line)
    line = "gear_config_name = os.path.basename(sys.argv[0])"; lines.append(line)
    line = "user_list = list(filter(lambda user: os.path.exists('/root/' + user), gear_user_list))"; lines.append(line)
    line = "if len(user_list) == 0:"; lines.append(line)
    line = "    user_list = list(filter(lambda user: os.path.exists('/home/' + user), gear_user_list))"; lines.append(line)
    line = "if len(user_list) == 0:"; lines.append(line)
    line = "    gear_user = 'none'"; lines.append(line)
    line = "else:"; lines.append(line)
    line = "    gear_user = user_list[0]"; lines.append(line)
    line = "gear_time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))"; lines.append(line)
    line = "gear_experiment_name = gear_user + '-' + gear_config_name + '-' + gear_time"; lines.append(line)
    line = ""; lines.append(line)
    line = ""; lines.append(line)


    write_down_obj(arg, father_name='Arg', tab_num=0)
    # for line in lines:
    #     print(line)

    with open(py_file_path, "w") as f:
        for line in lines:
            f.write(line)
            f.write('\n')


