# Copyright 2021-Present The THUAlign Authors


import torch.nn as nn

import thualign.utils as utils


class Module(nn.Module):

    def __init__(self, name=""):
        super().__init__()
        scope = utils.get_scope()
        self._name = scope + "/" + name if scope else name

    def add_name(self, tensor, name):
        tensor.tensor_name = utils.unique_name(name)

    @property
    def name(self):
        return self._name
