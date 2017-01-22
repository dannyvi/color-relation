#!/usr/local/bin/python3.4
#-*- coding:utf-8 -*-
#import math
import numpy as np
from npxyzjch import *
#import time

def npxyz2infrgb(xyz):
    xyz = xyz/100.0

    M_1 = np.array([[3.2406, -1.5372, -0.4986],\
                    [-0.9689, 1.8758,  0.0415],\
                    [0.0557, -0.2040,  1.0570]]).T
    RGB = xyz.dot(M_1)
    #RGB = np.where(RGB<=0,0.00000001,RGB)
    RGB = np.where(RGB>0.0031308,\
                   1.055*(np.abs(RGB)**0.4166666)*np.sign(RGB)-0.055,\
                   12.92*RGB)

    RGB = np.around(RGB*255)

    return RGB

def npvalidrgb(rgb):
    rgb   = np.where(np.isnan(rgb),-1,rgb)
    v_0   = np.where(rgb>=0  ,True,False)
    v_255 = np.where(rgb<=255,True,False)
    validity = v_0 & v_255
    return np.all(validity,1)

def npinvalidrgb(rgb):
    return np.invert(npvalidrgb(rgb))

def npxyz2rgb(xyz):
    xyz = xyz/100.0

    M_1 = np.array([[3.2406, -1.5372, -0.4986],\
                    [-0.9689, 1.8758,  0.0415],\
                    [0.0557, -0.2040,  1.0570]]).T
    RGB = xyz.dot(M_1)
    RGB = np.where(RGB<=0,0.00000001,RGB)
    RGB = np.where(RGB>0.0031308,\
                   1.055*(RGB**0.4166666)-0.055,\
                   12.92*RGB)

    RGB = np.around(RGB*255)
    RGB = np.where(RGB<=0,0,RGB)
    RGB = np.where(RGB>255,255,RGB)
    RGB = RGB.astype('uint8')

    return RGB

def nprgb2xyz(color):
    color = color/255.0
    color = np.where(color>0.04045,np.power(((color+0.055)/1.055),2.4),\
                     color/12.92)
    M = np.array([[0.4124, 0.3576, 0.1805],\
                  [0.2126, 0.7152, 0.0722],\
                  [0.0193, 0.1192, 0.9505]]).T

    return color.dot(M)*100


def nprgb2jch(color):
    XYZ = nprgb2xyz(color)
    value = npxyz2cam02(XYZ)
    return value[:,[2,4,1]]*np.array([1.0,1.0,0.9])

def npjch2rgb(jch):
    xyz = npjch2xyz(jch)
    #print(xyz)
    return npxyz2rgb(xyz)

def npjch2infrgb(jch):
    xyz = npjch2xyz(jch)
    return npxyz2infrgb(xyz)

def npjch2mskrgb(jch,msk):
    rgb = npjch2infrgb(jch)
    v   = npvalidrgb(rgb)
    if np.all(v):
        return rgb
    else:
        rgb[np.invert(v)] = msk
        return rgb.astype('uint8')

def npjch2ccmrgb(jch):
    jj  = jch.copy()
    jj[:,1] = np.around(jj[:,1])
    xyz = npjch2xyz(jj)
    rgb = npxyz2infrgb(xyz)
    v   = npinvalidrgb(rgb)
    while(np.any(v)):
        jj[v] -= (0,1,0)
        jj[:,1] = np.where(jj[:,1]<0,0,jj[:,1])
        rgb[v]     = npjch2infrgb(jj[v])
        v = npinvalidrgb(rgb)
    return rgb.astype('uint8')

if __name__=="__main__":
    a = np.array([[20.0,20.0,20.0]])
    print(npjch2xyz(a))
