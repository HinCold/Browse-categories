#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/3 20:56
# @name: __init__.py
# @author：XPR

__all__ = ['build_neck']


def build_neck(config):
    from .db_fpn import DBFPN
    from .rnn import SequenceEncoder
    support_dict = ['DBFPN', 'SequenceEncoder']

    module_name = config.pop('name')
    assert module_name in support_dict, Exception('neck only support {}'.format(
        support_dict))
    module_name = eval(module_name)(**config)
    return module_name
