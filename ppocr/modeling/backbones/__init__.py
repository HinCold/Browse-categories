#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/3 18:42
# @name: __init__.py
# @author：XPR

__all__ = ['build_backbone']


def build_backbone(config, model_type):
    if model_type == 'det':
        from .det_mobilenet_v3 import MobileNetV3
        from .det_resnet_vd import ResNet
        support_dict = ['MobileNetV3', 'ResNet']
    elif model_type == 'rec' or model_type == 'cls':
        from .rec_mobilenet_v3 import MobileNetV3
        from .rec_resnet_vd import ResNet
        from .rec_resnet_fpn import ResNetFPN
        support_dict = ['MobileNetV3', 'ResNet', 'ResNetFPN']
    else:
        raise NotImplementedError

    module_name = config.pop('name')
    assert  module_name in support_dict, Exception(
        'when model typs is {}, backbone only support {}'.format(model_type,
                                                                 support_dict))
    module_class = eval(module_name)(**config)
    return module_class
