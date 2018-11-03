import yaml
import os
import time


def input_parsing(inp):
    if isinstance(inp, str):
        path = inp
        f = open(path)
        d = yaml.load(f)
    else:
        raise Exception('default input type not support')
    return d


def dic2obj(d):
    top = Cls()
    for k, v in d.items():
        if isinstance(v, dict):
            setattr(top, k, dic2obj(v))
        else:
            setattr(top, k, v)
    return top


def obj_merge(ob_0, ob_1, no_list=None):
    if no_list is None:
        no_list = []
    attr_list = dir(ob_1)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or x == 'cover_by'), attr_list))
    for attr in attr_list:
        if attr in no_list:
            continue
        if not isinstance(getattr(ob_1, attr), Cls):
            val = getattr(ob_1, attr)
            setattr(ob_0, attr, val)
        if isinstance(getattr(ob_1, attr), Cls):
            obj_merge(getattr(ob_0, attr), getattr(ob_1, attr))

    return ob_0


def obj_eq(ob_0, ob_1, no_list=None):
    if no_list is None:
        no_list = []
    attr_list = dir(ob_1)
    attr_list = list(filter(lambda x: not (x[:1] == '_' or x == 'cover_by' or x == ''), attr_list))
    for attr in attr_list:
        if attr in no_list:
            continue
        if hasattr(ob_0, attr) ^ hasattr(ob_1, attr):
            return False
        if not isinstance(getattr(ob_0, attr), Cls):
            if getattr(ob_0, attr) != getattr(ob_1, attr):
                return False
        if isinstance(getattr(ob_0, attr), Cls):
            return obj_eq(getattr(ob_0, attr), getattr(ob_1, attr))

    return True


class Cls:
    def __init__(self):
        pass

    def __eq__(self, other):
        return obj_eq(self, other)

    def __ne__(self, other):
        return not obj_eq(self, other)


def get_Cls(default_file):
    d = input_parsing(default_file)
    obj = dic2obj(d)
    return obj


if __name__ == '__main__':
    # relative_path = 'YOUR_CONFIG/default.yaml'
    # arg = get_Cls(relative_path)
    # print(arg)

    import re
    test_str = "join('test', join('wait', 'me')) + %{a} + %a.b + %{a.b.c} + %{a.b} + %a + %ccc.a + %TE + %_sd8 + " \
               "str(5) + str(2+3) + [] + [[a, b][]] + [[['str']]].shape  %arg.a.b %arg.c.dd %arg._.e arg   %" \
               "%.root   %...todo  %..td  %...todo.a.b  %..td.afdsaf.dcc  %arg"

    reserve_pattern = re.compile('%(?!arg)[_a-zA-Z]\w*')

    quote_pattern_abs = re.compile('(?:%arg(?:\\.[_a-zA-Z]\w*)+)')
    quote_pattern_rel = re.compile('(?:%\\.+(?:\\.[_a-zA-Z]\w*)+)')
    quote_pattern = re.compile('(?:%arg(?:\\.[_a-zA-Z]\w*)+)|(?:%\\.+(?:\\.[_a-zA-Z]\w*)+)')

    base_function_pattern = re.compile('[_a-zA-Z]\w*\\([^()]*\\)')

    gear_patter = re.compile('(?:%(?!arg)[_a-zA-Z]\w*)|(?:%arg(?:\\.[_a-zA-Z]\w*)+)|(?:%\\.+(?:\\.[_a-zA-Z]\w*)+)|(?:[_a-zA-Z]\w*\\([^()]*\\))')

    search = gear_patter.findall(test_str)
    for reg in search:
        print(reg)

