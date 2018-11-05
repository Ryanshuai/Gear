import os
import time
import numpy as np
import subprocess
import sys

import torch
from torch import nn
from visdom import Visdom
import torchvision.utils as vutils
from tensorboardX import SummaryWriter


class VIS:
    """Vis class .

        a visualization tool for training/valid/test deep learning model.

    line:
        draw lines used in loss, accuracy etc.
    img:
        show img
    weight:
        show weights of a model.
    gradient:
        show gradient of all parameter of a model.
    model:
        show structure of a model.
    """
    def __init__(self,
                 tensorboard_enable=True,
                 tensorboard_save_dir='tensorboard_logs',
                 iteration_per_epoch=None,
                 visdom_enable=False):
        self.iteration_per_epoch = iteration_per_epoch
        self.epoch_counter = None
        self.iteration_counter = None
        # self.use_visdom = visdom_enable
        # if arg.visdom.enable:
        #     self.use_visdom = True
        #     self.vis = Visdom(env=arg.stamp.experiment_name, server=arg.visdom.server, port=arg.visdom.port)
        #     self.wins = []

        self.use_tensor_board = tensorboard_enable
        if tensorboard_enable:
            self.tb_writer = SummaryWriter(tensorboard_save_dir)

            # cmd = os.environ['HOME'] + "'/anaconda3/bin/'tensorboard --logdir=" + tensorboard_save_dir
            cmd = sys.executable[:-6] + "tensorboard --logdir=" + tensorboard_save_dir
            self.tb_log_out_process = subprocess.Popen("exec " + cmd, stdout=subprocess.PIPE, shell=True)

    def __del__(self):
        if self.use_tensor_board:
            self.tb_log_out_process.kill()

    def _update_step(self):
        assert self.iteration_per_epoch is not None, "try this: vis.iteration_per_epoch = len(YOUR_dataloader)"
        assert self.epoch_counter is not None, "try this: vis.epoch_counter = YOUR_EPOCH_INDEX"
        assert self.iteration_counter is not None, "try this: vis.epoch_counter = YOUR_BATCH_INDEX"
        self.step = self.iteration_per_epoch * self.epoch_counter + self.iteration_counter
        return self.step

    def line(self, name, y: float, step=None):
        if step is None:
            step = self._update_step()
        if self.use_tensor_board:
            self.tb_writer.add_scalar(name, y, step)
        # if self.use_visdom:
        #     if win not in self.wins:
        #         new_win = self.vis.line(win=win, name=name,
        #                                 X=np.array([x]), Y=np.array([y]),
        #                                 update=None, opts=dict(showlegend=True))
        #         self.wins.append(new_win)
        #     else:
        #         self.vis.line(win=win, name=name,
        #                       X=np.array([x]), Y=np.array([y]),
        #                       update='append', opts=dict(showlegend=True))

    def image(self, name, image, step=None, normalize=False, scale_each=False):
        if step is None:
            step = self._update_step()
        if self.use_tensor_board:
            if isinstance(image, np.ndarray):
                image = torch.from_numpy(image)
            if image.dim() == 4:
                image = vutils.make_grid(image, normalize=normalize, scale_each=scale_each)
            if image.shape[-1] == 3:
                if image.dim() == 4:
                    image = image.permute(0, 3, 1, 2)
                elif image.dim() == 3:
                    image = image.permute(2, 0, 1)
            self.tb_writer.add_image(name, image, global_step=step)

    def weight(self, model, step):
        if step is None:
            step = self._update_step()
        for k, v in model.state_dict().items():
            self.tb_writer.add_histogram('weight' + '/' + k, v, global_step=step)
            if v.grad is not None:
                print(v)

    def gradient(self, model, step):
        if step is None:
            step = self._update_step()
        for m in model.named_modules():
            k, v = m[0], m[1]
            if isinstance(v, nn.Conv2d):
                w_grad = v.weight.grad
                self.tb_writer.add_histogram('gradient' + '/' + k + '_w_grad', w_grad, global_step=step)
                if v.bias is not None:
                    b_grad = v.bias.grad
                    self.tb_writer.add_histogram('gradient' + '/' + k + '_b_grad', b_grad, global_step=step)
            elif isinstance(v, nn.BatchNorm2d):
                pass
            elif isinstance(v, nn.Linear):
                w_grad = v.weight.grad
                self.tb_writer.add_histogram('gradient' + '/' + k + '_w_grad', w_grad, global_step=step)
                if v.bias is not None:
                    b_grad = v.bias.grad
                    self.tb_writer.add_histogram('gradient' + '/' + k + '_b_grad', b_grad, global_step=step)

    def model(self, model, input_to_model):
        self.tb_writer.add_graph(model, input_to_model=input_to_model)


if __name__ == '__main__':

    myvis = VIS(tensorboard_save_dir='logs')
    for i in range(1, 10):
        # myvis.text('links', 'sdfasdfasdddddddddddddddddd')
        myvis.line('loss/train', -9 * i, i)
        myvis.line('loss/tst', 3 * i, i)
        time.sleep(1)
        print(i)
