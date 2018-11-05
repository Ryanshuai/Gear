import os
import sys
import time
import warnings
from ..yaml_to_object import Cls


config_name = os.path.basename(sys.argv[0])
user_list = list(filter(lambda user: os.path.exists('/root/' + user), user_list))
if len(user_list) == 0:
    user_list = list(filter(lambda user: os.path.exists('/home/' + user), user_list))
if len(user_list) == 0:
    user = 'none'
else:
    user = user_list[0]
time = time.strftime('%Y_%m_%d_%H_%M_%S', time.localtime(time.time()))
experiment_name = user + '-' + config_name + '-' + time


class ARG(Cls):
    def __init__(self):
        super().__init__()
        class STAMP(Cls):
            def __init__(self):
                super().__init__()
                self.config_name = config_name
                self.user = user
                if self.user == 'none':
                    warnings.warn('gear warning: cannot find your user name, please insert in user list or specify it', DeprecationWarning)
                self.time = time
                self.experiment_name = experiment_name
        self.stamp = STAMP()
        self.gear_cls_tree_path = 'arg'
        class DATA(Cls):
            def __init__(self):
                super().__init__()
                self.gear_cls_tree_path = 'arg.data'
                class DATALOADER(Cls):
                    def __init__(self):
                        super().__init__()
                        self.gear_cls_tree_path = 'arg.data.dataloader'
                        class TEST(Cls):
                            def __init__(self):
                                super().__init__()
                                self.batch_size = 1
                                self.gear_cls_tree_path = 'arg.data.dataloader.test'
                                self.num_workers = 4
                                self.shuffle = True
                        self.test = TEST()
                        class TRAIN(Cls):
                            def __init__(self):
                                super().__init__()
                                self.batch_size = 1
                                self.gear_cls_tree_path = 'arg.data.dataloader.train'
                                self.num_workers = 1
                                self.shuffle = True
                        self.train = TRAIN()
                        class VALID(Cls):
                            def __init__(self):
                                super().__init__()
                                self.batch_size = 1
                                self.gear_cls_tree_path = 'arg.data.dataloader.valid'
                                self.num_workers = 4
                                self.shuffle = True
                        self.valid = VALID()
                self.dataloader = DATALOADER()
                class DATASET(Cls):
                    def __init__(self):
                        super().__init__()
                        self.gear_cls_tree_path = 'arg.data.dataset'
                        class DEFAULTS(Cls):
                            def __init__(self):
                                super().__init__()
                                self.enable_fourth_channel = '*******************************************'
                                self.gear_cls_tree_path = 'arg.data.dataset.defaults'
                                self.heatmap_stride = 2
                                self.image_size = '----------------------------------------------------'
                                self.keypoints_list = [0, 1, 2, 3, 8, 9, 10, 11, 12, 13]
                                self.keypoints_names = ['head', 'neck', 'right_shoulder', 'left_shoulder', 'right_hip', 'left_hip', 'right_knee', 'left_knee', 'right_ankle', 'left_ankle']
                                self.root = '++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
                        self.defaults = DEFAULTS()
                self.dataset = DATASET()
        self.data = DATA()
        class POST(Cls):
            def __init__(self):
                super().__init__()
                self.background_index = [0]
                self.gear_cls_tree_path = 'arg.post'
                self.heatmap_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                self.link_sequence = [[0, 1, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8, 9]]
                self.points_exclude = [4, 5, 6, 7]
                class BOXSIZE(Cls):
                    def __init__(self):
                        super().__init__()
                        self.gear_cls_tree_path = 'arg.post.boxsize'
                        self.height = 192
                        self.width = 128
                self.boxsize = BOXSIZE()
        self.post = POST()
