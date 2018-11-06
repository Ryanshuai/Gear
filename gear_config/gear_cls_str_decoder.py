import os
import re
import sys
from os.path import dirname, join
import time
from copy import copy
from gear_config.yaml_to_object import get_Cls, Cls


# macros mode ==========================================================================================================
macros_dict = dict()
macros_dict['%time'] = "time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))"
macros_dict['%config_name'] = "os.path.basename(sys.argv[0])"
macros_dict['%user'] = "????????"

macros_dict['%project_dir'] = 'dirname(dirname(sys.argv[0]))'


def base_decode_reserve_str(the_str: str):
    for k, v in macros_dict.items():
        the_str = re.sub(k, v, the_str)
    return the_str


# reserve mode =========================================================================================================
reserve_pattern = re.compile('%(?!arg)[_a-zA-Z]\w*')

quote_pattern_abs = re.compile('(?:%arg(?:\\.[_a-zA-Z]\w*)+)')
quote_pattern_rel = re.compile('(?:%\\.+(?:\\.[_a-zA-Z]\w*)+)')
quote_pattern = re.compile('(?:%arg(?:\\.[_a-zA-Z]\w*)+)|(?:%\\.+(?:\\.[_a-zA-Z]\w*)+)')

base_function_pattern = re.compile('[_a-zA-Z]\w*\\([^()]*\\)')

gear_patter = re.compile('(?:%(?!arg)[_a-zA-Z]\w*)|(?:%arg(?:\\.[_a-zA-Z]\w*)+)|(?:%\\.+(?:\\.[_a-zA-Z]\w*)+)|(?:[_a-zA-Z]\w*\\([^()]*\\))')


def base_decode_abs_quote_str(arg: Cls, the_str: str):
    search = re.search(quote_pattern_abs, the_str)
    while search is not None:
        quote_str = the_str[search.regs[0][0]:search.regs[0][1]]
        pos_str = quote_str[1:]
        quote_value = eval(pos_str)
        the_str = the_str.replace(quote_str, quote_value, 1)
        search = re.search(quote_pattern_abs, the_str)
    return the_str


def relative_quote_to_abs_quote(now_pos_str: str, relative_quote_str: str):
    idx = re.search('[_a-zA-Z]', relative_quote_str).regs[0][0]
    assert idx > 0, 'input is not a relative quote.'
    abs_quote_str = re.sub('(?:\\.[_a-zA-Z]\w*){'+str(idx)+'}$', relative_quote_str[idx-1:], now_pos_str)
    return abs_quote_str







gear_user_list = ['qxc', 'ysy', 'jh1', 'ys2', 'qty', 'zam', 'ca', 'xc']
built_class = (bool, int, float, str, dict, list, None)


test_str = "join('test', join('wait', 'me')) + %{a} + %a.b + %{a.b.c} + %{a.b} + %a + %ccc.a + %TE + %_sd8 + " \
           "str(5) + str(2+3) + [] + [[a, b][]] + [[['str']]].shape  %arg.a.b %arg.c.dd %arg._.e arg   %" \
           "%.root   %...todo  %..td  %...todo.a.b  %..td.afdsaf.dcc  %arg  %time %user %config_name"


search = gear_patter.findall(test_str)
for reg in search:
    pass
    # print(reg)


test2_str = "%time %user %config_name"
test2_str = base_decode_reserve_str(test2_str)
print(test2_str)

test3_str = "______________%arg.save.gear_save_root ________________"
arg = get_Cls('YOUR_CONFIG/default.yaml')

test3_str = base_decode_quote_str(arg, test3_str)
print(test3_str)

