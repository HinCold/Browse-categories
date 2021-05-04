#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/3 23:41
# @name: __init__.py
# @author：XPR

__all__ = ['build_head']


def build_head(config):
    # det head
    from .det_db_head import DBHead

    # rec head
    from .rec_att_head import AttentionHead
    from .rec_ctc_head import CTCHead
    support_dict = ['DBHead', 'CTCHead', 'AttentionHead']

    module_name = config.pop('name')
    assert module_name in support_dict, Exception('head only support {}'.format(
        support_dict))
    module_class = eval(module_name)(**config)
    return module_class
