# -*- coding: utf-8 -*-

import os
mask = 3

def cfg_yolov3_5l(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_anchors,cfg_flip,cfg_jitter,cfg_random):
    
    cfg_filters = str( (int(cfg_classes) + 5) * mask )
    
    filepath = os.path.dirname(__file__) + '/CFG/yolov3_5l.cfg'
    textList = ""
    f = open(filepath, "r")
    textList = f.readlines() #テキストを一行ずつ配列として読込む（行の終わりの改行コードも含めて読込む）
    f.close()
    cfg = ""
    for x in textList:
        x = x.replace('\n', '')
        x = x.replace('\r', '')
        cfg = cfg + x + '\n'

    if cfg_flip == '0':
        cfg = cfg.replace('learning_rate=0.001', 'flip=0\n\nlearning_rate=0.001')
    if cfg_jitter == '0':
        cfg = cfg.replace('jitter=.3', 'jitter=0')
    if cfg_random == '0':
        cfg = cfg.replace('random=1', 'random=0')

    cfg = cfg.replace('batch=64', 'batch=' + cfg_batch)
    cfg = cfg.replace('subdivisions=16\n', 'subdivisions=' + cfg_subdivisions + '\n')
    cfg = cfg.replace('width=416', 'width=' + cfg_width)
    cfg = cfg.replace('height=416', 'height=' + cfg_height)
    cfg = cfg.replace('learning_rate=0.001', 'learning_rate=' + cfg_learning_rate)
    cfg = cfg.replace('burn_in=1000', 'burn_in=' + cfg_burn_in)
    cfg = cfg.replace('max_batches = 500200', 'max_batches = ' + cfg_max_batches)
    cfg = cfg.replace('filters=255', 'filters=' + cfg_filters)
    cfg = cfg.replace('classes=80', 'classes=' + cfg_classes)
    cfg = cfg.replace('anchors = 4,4,  5,5,  6,6, 7,7,  8,8,  9,9, 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326', cfg_anchors)
    return(cfg)

if __name__ == '__main__': #C言語のmain()に相当。このファイルが実行された場合、以下の行が実行される（モジュールとして読込まれた場合は、実行されない）。
    CFG = cfg_yolov3_5l('1', '1', '608', '608', '0.0005', '0', '100000', '1', 'anchors = 1,1,  2,2,  3,3, 4,4,  5,5,  6,6, 7,7,  8,8,  9,9,  10,10,  11,11,  12,12,  13,13,  14,14,  15,15', '0', '.3','1')
    filepath = os.path.dirname(__file__) + '/_test_cfg.cfg'
    f = open(filepath, "w")
    f.writelines(CFG)
    f.close()
