import os
import re
import sys
from os.path import dirname, join
import time
from copy import copy
from gear_config.yaml_to_object import Cls



class Decoder:
    def __init__(self, arg: Cls, macros_dict=None):
        self.arg = arg

        macros_dict = dict()
        macros_dict['$time'] = "time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))"
        macros_dict['$config_name'] = "os.path.basename(sys.argv[0])"
        macros_dict['$user'] = "????????"
        macros_dict['$project_dir'] = 'dirname(dirname(sys.argv[0]))'
        if macros_dict is not None:
            self.macros_dict = macros_dict

        self.rel_quote_str = '(?:\\$\\.*(?:\\.[_a-zA-Z]\w*)+)'
        self.abs_quote_str = '(?:\\$arg(?:\\.[_a-zA-Z]\w*)+)'
        self.reserve_str = '(?:\\$(?!arg)[_a-zA-Z]\w*)'
        self.function_str = '(?:[_a-zA-Z]\w*\\([$()]*\\))'

        self.rel_quote_pattern = re.compile(self.rel_quote_str)
        self.abs_quote_pattern = re.compile(self.abs_quote_str)
        self.reserve_pattern = re.compile(self.reserve_str)
        self.base_function_pattern = re.compile(self.function_str)

        self.reserve_or_abs_quote_pattern = re.compile(self.reserve_str+'|'+self.abs_quote_str)
        self.quote_pattern = re.compile(self.rel_quote_str+'|'+self.abs_quote_str)
        self.reserve_or_quote_pattern = re.compile(self.reserve_str+'|'+self.rel_quote_str+'|'+self.abs_quote_str)
        self.function_or_quote_pattern = re.compile(self.function_str+'|'+self.rel_quote_str+'|'+self.abs_quote_str)
        self.gear_pattern = re.compile(self.rel_quote_str+'|'+self.abs_quote_str+'|'+self.reserve_str+'|'+self.function_str)

        self.visit_list = list()

    def rel_quote_to_abs_quote(self, abs_pos_str: str, the_str: str):
        search = re.search(self.rel_quote_pattern, the_str)
        while search is not None:
            rel_quote_str = the_str[search.regs[0][0]:search.regs[0][1]]
            rel_pos_str = rel_quote_str[1:]
            abs_pos_str = self.rel_pos_to_abs_pos(abs_pos_str, rel_pos_str)
            abs_quote_str = '$'+abs_pos_str
            the_str = the_str.replace(rel_quote_str, abs_quote_str, 1)
            search = re.search(self.rel_quote_pattern, the_str)
        return the_str

    @staticmethod
    def rel_pos_to_abs_pos(abs_pos_str: str, relative_quote_str: str):
        idx = re.search('[_a-zA-Z]', relative_quote_str).regs[0][0]
        assert idx > 0, 'input is not a relative quote.'
        abs_quote_str = re.sub('(?:\\.[_a-zA-Z]\w*){' + str(idx) + '}$', relative_quote_str[idx - 1:], abs_pos_str)
        return abs_quote_str

    def decode_reserve_in_str(self, the_str: str):
        for k, v in self.macros_dict.items():
            the_str = re.sub('\\'+k, v, the_str)  # \\ is for $ change to \\$
        return the_str

    def decode_function_in_str(self, the_str: str):
        assert self.reserve_or_quote_pattern.search(the_str) is None
        if self.base_function_pattern.search(the_str) is not None:
            res = eval(the_str)
            return res

    def decode_str(self, abs_pos_str: str, the_str: str):
        if self.gear_pattern.search(the_str) is None:  # the_str does not have gear mode
            return the_str

        the_str = self.decode_reserve_in_str(the_str)

        assert abs_pos_str not in self.visit_list, 'circular quote!'
        self.visit_list.append(abs_pos_str)
        the_str = self.rel_quote_to_abs_quote(abs_pos_str, the_str)

        search = re.search(self.abs_quote_pattern, the_str)
        while search is not None:
            abs_quote_str = the_str[search.regs[0][0]:search.regs[0][1]]
            search_abs_pos_str = abs_quote_str[1:]
            str_quote_value = str(eval('self.'+search_abs_pos_str))
            leaf_quote_value = self.decode_str(search_abs_pos_str, str_quote_value)
            # leaf_quote_value = self.decode_function_in_str(leaf_quote_value)
            the_str = the_str.replace(abs_quote_str, leaf_quote_value, 1)
            search = re.search(self.abs_quote_pattern, the_str)

        exec("self."+abs_pos_str+" = \"{}\"".format(the_str))
        self.visit_list.remove(abs_pos_str)
        return the_str

    def decode_arg(self, obj: Cls):
        attr_list = dir(obj)
        attr_list = list(filter(lambda x: not (x[:1] == '_' or callable(getattr(obj, x)) or x == ''), attr_list))
        for attr in attr_list:
            if isinstance(getattr(obj, attr), Cls):
                self.decode_arg(getattr(obj, attr))
            elif isinstance(getattr(obj, attr), str):
                self.decode_str(obj.gear_cls_tree_path+'.'+attr, getattr(obj, attr))
        return obj

    def decode(self):
        return self.decode_arg(self.arg)


if __name__ == '__main__':
    from gear_config.yaml_to_object import get_Cls, Cls

    yaml_file = '/home/ys/Desktop/github_gear/Gear/gear_config/YOUR_CONFIG/default.yaml'
    # yaml_file = '/home/ys/Desktop/github_gear/Gear/gear_config/YOUR_CONFIG/specific.yaml'
    arg = get_Cls(yaml_file)

    arg = Decoder(arg).decode()
    # ttttttttttt = decoder.decode_str('arg.a.c', '$.b')
    # print(ttttttttttt)

    print()

