# Copyright 2021-Present The THUAlign Authors
# Modified from torch.nn.utils.convert_parameters.py


import torch


def params_to_vec(parameters):
    r"""Convert parameters to one vector

    Arguments:
        parameters (Iterable[Tensor]): an iterator of Tensors that are the
            parameters of a model.

    Returns:
        The parameters represented by a single vector
    """

    # Flag for the device where the parameter is located
    param_device = None
    vec = []

    for param in parameters:
        if param is None:
            continue

        # Ensure the parameters are located in the same device
        param_device = _check_param_device(param, param_device)
        vec.append(param.view(-1))

    return torch.cat(vec)


def vec_to_params(vec, parameters):
    r"""Convert one vector to the parameters

    Arguments:
        vec (Tensor): a single vector represents the parameters of a model.
        parameters (Iterable[Tensor]): an iterator of Tensors that are the
            parameters of a model.
    """

    # Ensure vec of type Tensor
    if not isinstance(vec, torch.Tensor):
        raise TypeError("expected torch.Tensor, but got: {}"
                        .format(torch.typename(vec)))

    # Flag for the device where the parameter is located
    param_device = None

    # Pointer for slicing the vector for each parameter
    pointer = 0

    for param in parameters:
        if param is None:
            continue

        # Ensure the parameters are located in the same device
        param_device = _check_param_device(param, param_device)

        # The length of the parameter
        num_param = param.numel()

        # Slice the vector, reshape it, and replace the old data of the parameter
        param.data = vec[pointer:pointer + num_param].view_as(param).data

        # Increment the pointer
        pointer += num_param


def _check_param_device(param, old_param_device):
    r"""This helper function is to check if the parameters are located
    in the same device. Currently, the conversion between model parameters
    and single vector form is not supported for multiple allocations,
    e.g. parameters in different GPUs, or mixture of CPU/GPU.

    Arguments:
        param ([Tensor]): a Tensor of a parameter of a model
        old_param_device (int): the device where the first parameter of a
                                model is allocated.

    Returns:
        old_param_device (int): report device for the first time
    """

    # Meet the first parameter
    if old_param_device is None:
        old_param_device = param.get_device() if param.is_cuda else -1
    else:
        warn = False

        if param.is_cuda:  # Check if in same GPU
            warn = (param.get_device() != old_param_device)
        else:  # Check if in CPU
            warn = (old_param_device != -1)

        if warn:
            raise TypeError("Found two parameters on different devices,"
                            " this is currently not supported.")

    return old_param_device
