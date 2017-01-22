#!/usr/local/bin/python3.4
#-*- coding:utf-8 -*-
import numpy as np
from npcvt import npjch2infrgb

j_num,c_num,h_num=400,400,360
j_unit,c_unit,h_unit = j_num/100,c_num/115,h_num/360


def npvalidrgb(rgb):
    rgb   = np.where(np.isnan(rgb),-1,rgb)
    v_0   = np.where(rgb>=0  ,True,False)
    v_255 = np.where(rgb<=255,True,False)
    validity = v_0 & v_255
    return np.all(validity,1)

def gen_map(valid=True):
    index_table = np.zeros((j_num,c_num,h_num,3),dtype='float')
    for i in range(j_num):
        index_table[i,:,:,0]=i/j_unit
    for i in range(c_num):
        index_table[:,i,:,1]=i/c_unit
    for i in range(h_num):
        index_table[:,:,i,2]=i/h_unit
    rgb_map = npjch2infrgb(index_table.reshape(-1,3)).astype('int16').reshape(index_table.shape)
    rgb_map[j_num-1,:,:,:]=255
    rgb_map[0,:,:,:]=0
    if valid:
        valid_map = npvalidrgb(rgb_map.reshape(-1,3)).reshape(rgb_map.shape[:-1])
        for j in range(1,j_num-1):
            for h in range(h_num):
                init_jch = rgb_map[j,0,h]
                for c in range(c_num):
                    if valid_map[j,c,h]:
                        init_jch = rgb_map[j,c,h]
                    else:
                        rgb_map[j,c:,h] = init_jch
                        break
    return rgb_map

def valid_map():
    index_table = np.zeros((j_num,c_num,h_num,3),dtype='float')
    for i in range(j_num):
        index_table[i,:,:,0]=i/j_unit
    for i in range(c_num):
        index_table[:,i,:,1]=i/c_unit
    for i in range(h_num):
        index_table[:,:,i,2]=i/h_unit
    rgb_map = npjch2infrgb(index_table.reshape(-1,3)).astype('int16').reshape(index_table.shape)
    valid_map = npvalidrgb(rgb_map.reshape(-1,3)).reshape(rgb_map.shape[:-1])
    v_map = np.where(valid_map,255,0)
    return v_map
    #valid_map

def true_cvalue():
    index_table = np.zeros((j_num,c_num,h_num,3),dtype='int16')
    for i in range(j_num):
        index_table[i,:,:,0]=i/j_unit
    for i in range(c_num):
        index_table[:,i,:,1]=i/c_unit
    for i in range(h_num):
        index_table[:,:,i,2]=i/h_unit
    rgb_map = npjch2infrgb(index_table.reshape(-1,3)).astype('int16').reshape(index_table.shape)
    c_map = np.ones(rgb_map.shape[:-1],dtype='int')*255
    if True:
        valid_map = npvalidrgb(rgb_map.reshape(-1,3)).reshape(rgb_map.shape[:-1])
        for j in range(0,j_num):
            for h in range(h_num):
                init_c = 0 #rgb_map[j,0,h]
                for c in range(c_num):
                    if valid_map[j,c,h]:
                        init_c += 1#rgb_map[j,c,h]
                    else:
                        #rgb_map[j,c:,h] = init_jch
                        c_map[j,c:,h] = init_c
                        break
    return c_map
