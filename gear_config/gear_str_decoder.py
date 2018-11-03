import os
import time
from gear_config.yaml_to_object import Cls


def decode_str()


gear_user_list = ['qxc', 'ysy', 'jh1', 'ys2', 'qty', 'zam', 'ca', 'xc']
built_class = (bool, int, float, str, dict, list, None)

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