#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/2 23:38
# @name: __init__
# @author：XPR
import copy

__all__ = ['build_model']


def build_model(config):
    from .base_model import BaseModel

    config = copy.deepcopy(config)
    module_class = BaseModel(config)
    return module_class
