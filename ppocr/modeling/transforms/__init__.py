#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/3 14:33
# @name: __init__.py
# @author：XPR


__all__ = ['build_transform']


def build_transform(config):
    from .tps import TPS

    support_dict = ['TPS']

    module_name = config.pop('name')
    assert module_name in support_dict, Exception('transform only support {}'.format(support_dict))
    module_class = eval(module_name)(**config)
    return module_class
