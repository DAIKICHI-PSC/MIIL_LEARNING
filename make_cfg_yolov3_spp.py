# -*- coding: utf-8 -*-

import os



from get_num_mask_filters import get_num_mask_filters 



def cfg_yolov3_spp(cfg_batch,cfg_subdivisions,cfg_width,cfg_height,cfg_learning_rate,cfg_burn_in,cfg_max_batches,cfg_classes,cfg_anchors,cfg_flip,cfg_small,cfg_conv,cfg_jitter,cfg_random):



    cla = int(cfg_classes)
    anc = cfg_anchors.replace('anchors =', '')
    ret, num, mask1, mask2, mask3, filters1, filters2, filters3 = get_num_mask_filters(cla, anc)



    filepath = os.path.dirname(__file__) + '/CFG/yolov3-spp.cfg'
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
    if  cfg_small =='1':
        cfg = cfg.replace('stride=2\n\n[route]\nlayers = -1, 36', 'stride=4\n\n[route]\nlayers = -1, 11')
    if  cfg_conv =='1':
        cfg = cfg.replace('######################', 'stopbackward=1\n######################')
    if cfg_jitter == '0':
        cfg = cfg.replace('jitter=.3', 'jitter=0')
    if cfg_random == '0':
        cfg = cfg.replace('random=1', 'random=0')

    cfg = cfg.replace('batch=1', 'batch=' + cfg_batch)
    cfg = cfg.replace('subdivisions=1\n', 'subdivisions=' + cfg_subdivisions + '\n')
    cfg = cfg.replace('width=608', 'width=' + cfg_width)
    cfg = cfg.replace('height=608', 'height=' + cfg_height)
    cfg = cfg.replace('learning_rate=0.001', 'learning_rate=' + cfg_learning_rate)
    cfg = cfg.replace('burn_in=1000', 'burn_in=' + cfg_burn_in)
    cfg = cfg.replace('max_batches = 500200', 'max_batches = ' + cfg_max_batches)



    cfg = cfg.replace('filters=255_1', 'filters=' + filters1)
    cfg = cfg.replace('filters=255_2', 'filters=' + filters2)
    cfg = cfg.replace('filters=255_3', 'filters=' + filters3)
    cfg = cfg.replace('num=9', 'num=' + num)
    cfg = cfg.replace('mask = 1', mask1)
    cfg = cfg.replace('mask = 2', mask2)
    cfg = cfg.replace('mask = 3', mask3)



    cfg = cfg.replace('classes=80', 'classes=' + cfg_classes)
    cfg = cfg.replace('anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326', cfg_anchors)



    if ret == 0:
        return(cfg)
    else:
        return('')



if __name__ == '__main__': #C言語のmain()に相当。このファイルが実行された場合、以下の行が実行される（モジュールとして読込まれた場合は、実行されない）。
    CFG = cfg_yolov3_spp('64', '64', '416', '416', '0.0001', '0', '100000', '1', 'anchors = 1,1,  2,2,  3,3,  4,4,  5,5,  6,6,  7,7,  8,8,  9,9', '0', '1', '1', '.3', '1')
    filepath = os.path.dirname(__file__) + '/_test_cfg.cfg'
    f = open(filepath, "w")
    f.writelines(CFG)
    f.close()
