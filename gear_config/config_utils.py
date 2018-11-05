import os
import time
from gear_config.yaml_to_object import Cls


gear_user_list = ['qxc', 'ysy', 'jh1', 'ys2', 'qty', 'zam', 'ca', 'xc']
built_class = (bool, int, float, str, dict, list, None)


def merge(a, b):
    assert isinstance(a, Cls)
    assert isinstance(b, Cls)
    """
    :param a: the default gear_config object
    :param b: the specific gear_config object
    :return: a covered by b
    """
    b_attr_list = dir(b)
    b_attr_list = list(filter(lambda x: not x[:1] == '_', b_attr_list))
    for attr in b_attr_list:
        if not isinstance(getattr(b, attr), Cls):
            val = getattr(b, attr)
            setattr(a, attr, val)
        if isinstance(getattr(b, attr), Cls):
            merge(getattr(a, attr), getattr(b, attr))
    return a


if __name__ == '__main__':

    # from gear_config.YOUR_CONFIG.default import ARG
    # arg = ARG()
    # print(arg)
    # from gear_config.YOUR_CONFIG.specific import ARG as sp_ARG
    # sp_arg = sp_ARG()
    # arg = merge(arg, sp_arg)
    # del arg.data
    # print(arg)
    # print(arg == arg)
    # print(arg == sp_arg)

    from gear_config.YOUR_CONFIG.default import ARG
    arg = ARG()
    from gear_config.YOUR_CONFIG.specific import ARG as sp_ARG
    sp_arg = sp_ARG()
