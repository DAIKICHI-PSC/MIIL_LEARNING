# -*- coding: utf-8 -*-

import os
mask = 4

def cfg_resnet152_trident(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_flip,cfg_jitter):
    
    cfg_filters = str( (int(cfg_classes) + 5) * mask )
    
    filepath = os.path.dirname(__file__) + '/CFG/resnet152_trident.cfg'
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

    cfg = cfg.replace('batch=64', 'batch=' + cfg_batch)
    cfg = cfg.replace('subdivisions=64\n', 'subdivisions=' + cfg_subdivisions + '\n')
    cfg = cfg.replace('width=608', 'width=' + cfg_width)
    cfg = cfg.replace('height=608', 'height=' + cfg_height)
    cfg = cfg.replace('learning_rate=0.001', 'learning_rate=' + cfg_learning_rate)
    cfg = cfg.replace('burn_in=1000', 'burn_in=' + cfg_burn_in)
    cfg = cfg.replace('max_batches = 10000', 'max_batches = ' + cfg_max_batches)
    cfg = cfg.replace('filters=24', 'filters=' + cfg_filters)
    cfg = cfg.replace('classes=1', 'classes=' + cfg_classes)
    #cfg = cfg.replace('anchors = 8,8, 10,13, 16,30, 33,23,  32,32, 30,61, 62,45, 64,64,  59,119, 116,90, 156,198, 373,326', cfg_anchors)
    return(cfg)

if __name__ == '__main__': #C言語のmain()に相当。このファイルが実行された場合、以下の行が実行される（モジュールとして読込まれた場合は、実行されない）。
    CFG = cfg_resnet152_trident('1', '1', '416', '416', '0.0005', '0', '500000', '5', '0', '.3')
    filepath = os.path.dirname(__file__) + '/_test_cfg.cfg'
    f = open(filepath, "w")
    f.writelines(CFG)
    f.close()
