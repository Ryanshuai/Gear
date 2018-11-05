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
        self.data_dir = None
        self.gear_cls_tree_path = 'arg'
        self.save_dir = None
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
                                self.enable_fourth_channel = True
                                self.gear_cls_tree_path = 'arg.data.dataset.defaults'
                                self.heatmap_stride = 2
                                self.keypoints_list = [0, 1, 2, 3, 8, 9, 10, 11, 12, 13]
                                self.keypoints_names = ['head', 'neck', 'right_shoulder', 'left_shoulder', 'right_hip', 'left_hip', 'right_knee', 'left_knee', 'right_ankle', 'left_ankle']
                                self.root = '/home/ys/Data/data_reognized_20180910'
                                class IMAGE_SIZE(Cls):
                                    def __init__(self):
                                        super().__init__()
                                        self.gear_cls_tree_path = 'arg.data.dataset.defaults.image_size'
                                        self.height = 192
                                        self.width = 128
                                self.image_size = IMAGE_SIZE()
                        self.defaults = DEFAULTS()
                        class TRAIN(Cls):
                            def __init__(self):
                                super().__init__()
                                self.background_index = [0]
                                self.center_perturb_max = 20
                                self.crop_height = 192
                                self.crop_max_size = 3.5
                                self.crop_min_size = 1.0
                                self.crop_width = 128
                                self.cross_body_crop_probs = [0.3, 0.3, 0.4]
                                self.enable_cross_body_crop = True
                                self.enable_fourth_channel = True
                                self.enable_generate_fake_fourth_channel = False
                                self.fourth_channel_heatmap_sigma = 4.0
                                self.fourth_channel_keypoint_position_jitter_pixels = 5
                                self.fourth_channel_keypoint_vis_status_jitter_prob = 0.3
                                self.fourth_channel_prob = 0.8
                                self.gear_cls_tree_path = 'arg.data.dataset.train'
                                self.heatmap_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                                self.heatmap_sigma = [4.0]
                                self.heatmap_stride = 2
                                self.heatmap_visible_level = 2
                                self.keypoints_list = [0, 1, 2, 3, 8, 9, 10, 11, 12, 13]
                                self.keypoints_names = ['head', 'neck', 'right_shoulder', 'left_shoulder', 'right_hip', 'left_hip', 'right_knee', 'left_knee', 'right_ankle', 'left_ankle']
                                self.link_sequence = [[0, 1, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8, 9]]
                                self.points_exclude = [4, 5, 6, 7]
                                self.relative_txt_path = 'txt/multiple_txt_files_mode/20180910_example/train/20180910_train_pointer.txt'
                                self.root = '/home/ys/Data/data_reognized_20180910'
                                self.rotate = 5
                                self.txt_path = None
                                class BOXSIZE(Cls):
                                    def __init__(self):
                                        super().__init__()
                                        self.gear_cls_tree_path = 'arg.data.dataset.train.boxsize'
                                        self.height = 192
                                        self.width = 128
                                self.boxsize = BOXSIZE()
                                class IMAGE_SIZE(Cls):
                                    def __init__(self):
                                        super().__init__()
                                        self.gear_cls_tree_path = 'arg.data.dataset.train.image_size'
                                        self.height = 192
                                        self.width = 128
                                self.image_size = IMAGE_SIZE()
                                class SCALE(Cls):
                                    def __init__(self):
                                        super().__init__()
                                        self.gear_cls_tree_path = 'arg.data.dataset.train.scale'
                                        self.max = 1.1
                                        self.min = 0.9
                                self.scale = SCALE()
                        self.train = TRAIN()
                        class VALID(Cls):
                            def __init__(self):
                                super().__init__()
                                self.background_index = [0]
                                self.crop_height = 192
                                self.crop_max_size = 1.0
                                self.crop_min_size = 1.0
                                self.crop_width = 128
                                self.enable_fourth_channel = True
                                self.fourth_channel_heatmap_sigma = 4.0
                                self.gear_cls_tree_path = 'arg.data.dataset.valid'
                                self.heatmap_index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
                                self.heatmap_sigma = [4.0]
                                self.heatmap_stride = 2
                                self.heatmap_visible_level = 2
                                self.keypoints_list = [0, 1, 2, 3, 8, 9, 10, 11, 12, 13]
                                self.keypoints_names = ['head', 'neck', 'right_shoulder', 'left_shoulder', 'right_hip', 'left_hip', 'right_knee', 'left_knee', 'right_ankle', 'left_ankle']
                                self.link_sequence = [[0, 1, 1, 2, 3, 4, 5, 6, 7], [1, 2, 3, 4, 5, 6, 7, 8, 9]]
                                self.points_exclude = [4, 5, 6, 7]
                                self.relative_txt_path = 'txt/multiple_txt_files_mode/20180910_example/valid/valid.txt'
                                self.root = '/home/ys/Data/data_reognized_20180910'
                                self.txt_path = None
                                self.video_path = '/home/ys/Data/pose_estimate_test/video_test_selected_20180608/NoNeedRotate/'
                                class BOXSIZE(Cls):
                                    def __init__(self):
                                        super().__init__()
                                        self.gear_cls_tree_path = 'arg.data.dataset.valid.boxsize'
                                        self.height = 192
                                        self.width = 128
                                self.boxsize = BOXSIZE()
                                class IMAGE_SIZE(Cls):
                                    def __init__(self):
                                        super().__init__()
                                        self.gear_cls_tree_path = 'arg.data.dataset.valid.image_size'
                                        self.height = 192
                                        self.width = 128
                                self.image_size = IMAGE_SIZE()
                        self.valid = VALID()
                self.dataset = DATASET()
        self.data = DATA()
        class IMAGE_SITE(Cls):
            def __init__(self):
                super().__init__()
                self.data_dir = '/root/group-mtlab-bj/image_site_datasets'
                self.enable = False
                self.gear_cls_tree_path = 'arg.image_site'
                self.url = 'http://172.16.3.247:8000/image-site/dataset/{dataset_name}?size=50&page=1'
        self.image_site = IMAGE_SITE()
        class LOSS(Cls):
            def __init__(self):
                super().__init__()
                self.gear_cls_tree_path = 'arg.loss'
                self.global_weight = 1
                self.refine_weight = 1
                self.top_k = 6
        self.loss = LOSS()
        class MODEL(Cls):
            def __init__(self):
                super().__init__()
                self.fourth_channel = False
                self.gear_cls_tree_path = 'arg.model'
                self.out_c = 10
                self.out_h = 100
                self.out_w = 64
                self.output_type = 'heatmap'
                self.pyramid_num = 4
        self.model = MODEL()
        class OPTIM(Cls):
            def __init__(self):
                super().__init__()
                self.gear_cls_tree_path = 'arg.optim'
                self.lr = 0.001
                self.weight_decay = 1e-05
        self.optim = OPTIM()
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
        class SAVE(Cls):
            def __init__(self):
                super().__init__()
                self.analyze = None
                self.gear_cls_tree_path = 'arg.save'
                self.gear_save_root = '/home/ys/Data/pose_estimate_save/'
                self.model = None
                self.relative_analyze = 'valid/coco_analyze'
                self.relative_model = 'join(%arg.save_root, 'models')'
                self.relative_tensorboard = 'tensorboard'
                self.relative_test = 'tst'
                self.relative_train = 'train'
                self.relative_valid = 'valid'
                self.root = None
                self.tensorboard = None
                self.test = None
                self.train = None
                self.valid = None
        self.save = SAVE()
        class TENSORBOARD(Cls):
            def __init__(self):
                super().__init__()
                self.enable = True
                self.gear_cls_tree_path = 'arg.tensorboard'
        self.tensorboard = TENSORBOARD()
        class TRAIN(Cls):
            def __init__(self):
                super().__init__()
                self.epochs = 20
                self.gear_cls_tree_path = 'arg.train'
                self.log_interval = 10
                self.save_model_interval = 1
                self.valid_interval = 1
        self.train = TRAIN()
        class VISDOM(Cls):
            def __init__(self):
                super().__init__()
                self.enable = False
                self.gear_cls_tree_path = 'arg.visdom'
                self.port = 8097
                self.server = 'http://localhost'
        self.visdom = VISDOM()
