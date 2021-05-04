#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/3 14:01
# @name: base_model
# @author：XPR
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from paddle import nn
from ppocr.modeling.transforms import build_transform
from ppocr.modeling.backbones import build_backbone
from ppocr.modeling.necks import build_neck
from ppocr.modeling.heads import build_head

__all__ = ['BaseModel']


class BaseModel(nn.Layer):
    def __init__(self, config):
        super(BaseModel, self).__init__()

        in_channels = config.get('in_channels', 3)
        model_type = config['model_type']
        # build transfrom,
        # for rec, transfrom can be TPS,None
        # for det and cls, transfrom shoule to be None,
        # if you make model differently, you can use transfrom in det and cls
        if 'Transform' not in config or config['Transform'] is None:
            self.use_transform = False
        else:
            self.use_transform = True
            config['Transform']['in_channels'] = in_channels
            self.transform = build_transform(config['Transform'])
            in_channels = self.transform.out_channels

        # build backbone, backbone is need for del, rec
        config["Backbone"]['in_channels'] = in_channels
        self.backbone = build_backbone(config["Backbone"], model_type)
        in_channels = self.backbone.out_channels

        # build neck
        # for rec, neck can be cnn,rnn or reshape(None)
        # for det, neck can be FPN, BIFPN and so on.
        if 'Neck' not in config or config['Neck'] is None:
            self.use_neck = False
        else:
            self.use_neck = True
            config['Neck']['in_channels'] = in_channels
            self.neck = build_neck(config['Neck'])
            in_channels = self.neck.out_channels

        # # build head, head is need for det, rec
        config["Head"]['in_channels'] = in_channels
        self.head = build_head(config["Head"])

    def forward(self, x, data=None):
        if self.use_transform:
            x = self.transform(x)
        x = self.backbone(x)
        if self.use_neck:
            x = self.neck(x)
        if data is None:
            x = self.head(x)
        else:
            x = self.head(x, data)
        return x

