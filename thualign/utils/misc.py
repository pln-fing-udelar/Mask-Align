# Copyright 2021-Present The THUAlign Authors


_GLOBAL_STEP = 0


def get_global_step():
    return _GLOBAL_STEP


def set_global_step(step):
    global _GLOBAL_STEP
    _GLOBAL_STEP = step
