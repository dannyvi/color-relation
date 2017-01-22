#!/usr/local/bin/python3.4
#-*- coding:utf-8 -*-
import numpy as np
from PIL import Image

def get_index():
    p = Image.open('colorindex.png')
    arr = np.array(p).reshape((101,115,360,3))
    p.close()
    return  arr

def get_sindex():
    p = Image.open('jch_map_400.png')
    arr = np.array(p).reshape((400,400,360,3))
    p.close()
    return  arr

def get_c_valid():
    p = Image.open('valid_index.png')
    arr = np.array(p).reshape((101,115,360))==255
    p.close()
    return arr

jch_rgb_index = get_index() #np.array(p).reshape((101,115,360,3))

sjch_rgb_index = get_sindex()

c_valid_index = get_c_valid()

def jch2rgb(jch):
    """
    要求jch为 0--100, 0--115, 0--360  整数
    色彩数量117万
    """
    return jch_rgb_index[jch[:,0],jch[:,1],jch[:,2]].reshape(-1,3).astype('uint8')

def sjch2rgb(jch):
    """
    增强色彩到 800 万.
    jch 为 1--100.0, 0--115.0, 0--360.0
    """
    j = np.around((jch[:,0]*(399/100))).astype('int')
    c = np.around((jch[:,1]*(399/115.0))).astype('int')
    h = (np.around((jch[:,2]))%360).astype('int')
    return sjch_rgb_index[j,c,h].reshape(-1,3).astype('uint8')
