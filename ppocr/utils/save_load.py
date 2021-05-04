#!/usr/bin/python
# -*- coding: UTF-8 -*-
# @date: 2021/5/2 23:40
# @name: save_load
# @author：XPR
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import pickle
import six

import paddle

__all__ = ['init_model']


def load_dygraph_pretrain(model, logger, path=None, load_static_weights=False):
    if not (os.path.isdir(path) or os.path.exists(path + '.pdparams')):
        raise ValueError("Model pretrain path {} does not "
                         "exists.".format(path))
    if load_static_weights:
        pre_state_dict = paddle.static.load_program_state(path)
        param_state_dict = {}
        model_dict = model.state_dict()
        for key in model_dict.keys():
            weight_name = model_dict[key].name
            weight_name = weight_name.replace('binarize', '').replace(
                'thresh', '')  # for DB
            if weight_name in pre_state_dict.keys():
                # logger.info('Load weight: {}, shape: {}'.format(
                #     weight_name, pre_state_dict[weight_name].shape))
                if 'encoder_rnn' in key:
                    # delete axis which is 1
                    pre_state_dict[weight_name] = pre_state_dict[
                        weight_name].squeeze()
                    # change axis
                    if len(pre_state_dict[weight_name].shape) > 1:
                        pre_state_dict[weight_name] = pre_state_dict[
                            weight_name].transpose((1, 0))
                param_state_dict[key] = pre_state_dict[weight_name]
            else:
                param_state_dict[key] = model_dict[key]
        model.set_state_dict(param_state_dict)
        return

    param_state_dict = paddle.load(path + '.pdparams')
    model.set_state_dict(param_state_dict)
    return


def init_model(config, model, logger, optimizer=None, lr_scheduler=None):
    """
        load model from checkpoint or pretrained_model
    """
    global_config = config['Global']
    checkpoints = global_config.get('checkpoints')
    pretrained_model = global_config.get('pretrained_model')
    best_model_dict = {}
    if checkpoints:
        assert os.path.exists(checkpoints + ".pdparams"), \
            "Given dir {}.pdparams not exist.".format(checkpoints)
        assert os.path.exists(checkpoints + ".pdopt"), \
            "Given dir {}.pdopt not exist.".format(checkpoints)
        para_dict = paddle.load(checkpoints + '.pdparams')
        opti_dict = paddle.load(checkpoints + '.pdopt')
        model.set_state_dict(para_dict)
        if optimizer is not None:
            optimizer.set_state_dict(opti_dict)

        if os.path.exists(checkpoints + '.states'):
            with open(checkpoints + '.states', 'rb') as f:
                states_dict = pickle.load(f) if six.PY2 else pickle.load(
                    f, encoding='latin1')
            best_model_dict = states_dict.get('best_model_dict', {})
            if 'epoch' in states_dict:
                best_model_dict['start_epoch'] = states_dict['epoch'] + 1

        logger.info("resume from {}".format(checkpoints))
    elif pretrained_model:
        load_static_weights = global_config.get('load_static_weights', False)
        if not isinstance(pretrained_model, list):
            pretrained_model = [pretrained_model]
        if not isinstance(load_static_weights, list):
            load_static_weights = [load_static_weights] * len(pretrained_model)
        for idx, pretrained in enumerate(pretrained_model):
            load_static = load_static_weights[idx]
            load_dygraph_pretrain(
                model, logger, path=pretrained, load_static_weights=load_static)
            logger.info("load pretrained model from {}".format(
                pretrained_model))
    else:
        logger.info('train from scratch')
    return best_model_dict
