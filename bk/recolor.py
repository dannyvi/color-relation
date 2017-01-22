#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from functools import reduce
import numpy as np
from femmasop import nCircleAdd,nLimitAdd
from dimension.colorconvertc import jch2rgb

def polar2magf(polar):
    if polar.ndim >2:
        shape = polar.shape
        polar.resize(-1,3)
        r_c = polar[:,1]
        r_h = polar[:,2]*2*np.pi

        r_z = polar[:,0]
        r_x = r_c * np.cos(r_h)
        r_y = r_c * np.sin(r_h)
        s = np.array([r_x,r_y,r_z]).T.reshape(-1,3),astype('float').reshape(shape)
        return s
    elif polar.ndim == 2:
        r_c = polar[:,1]
        r_h = polar[:,2]*2*np.pi

        r_z = polar[:,0]
        r_x = r_c * np.cos(r_h)
        r_y = r_c * np.sin(r_h)
        return np.array([r_x,r_y,r_z]).T.reshape(-1,3).astype('float')
    elif polar.ndim == 1:
        c_z = polar[0]
        c_x = polar[1]*np.cos(polar[2]).astype('float')
        c_y = polar[1]*np.sin(polar[2]).astype('float')
        return np.array([c_x,c_y,c_z]).T.reshape(-1,3).astype('float')
    else:
        return 0

def mag2polarf(mag):
    if mag.ndim >2:
        shape = mag.shape
        mag.resize(-1,3)
        x = mag[:,0]
        y = mag[:,1]

        J = nLimitAdd(0,0,1)(mag[:,2])
        C = np.sqrt(np.square(y)+np.square(x))
        H = nCircleAdd(0,0,1)(np.arctan2(y,x)/(np.pi*2))
        s = np.array([J,C,H]).T.astype('float').reshape(shape)
        return s
    elif mag.ndim == 2:
        x = mag[:,0]
        y = mag[:,1]

        J = nLimitAdd(0,0,1)(mag[:,2])
        C = np.sqrt(np.square(y)+np.square(x))
        H = nCircleAdd(0,0,1)(np.arctan2(y,x)/(np.pi*2))
        s = np.array([J,C,H]).T.astype('float')
        return s
    elif mag.ndim == 1:
        J = nLimitAdd(0,0,1)(k[2])
        C = np.sqrt(np.square(k[1])+np.square(k[0]))
        H = nCircleAdd(0,0,1)(np.arctan2(y,x)/(np.pi*2))
        return np.array([J,C,H]).T.astype('float')
    else : return 0

def mag2polari(mag):
    return mag2polarf(mag)*np.array([100,100,360]).astype('int32')


def rColorSeq(center=[0,0,0.2],rule=[[0.2,0.4,0.3],[0.6,0.3,0.6]],scale=0.3,time=4):
    rule = np.array(rule).astype('float')-center
    cen  = np.array(center).astype('float')

    r = polar2magf(rule)
    k = polar2magf(cen)

    for i in range(time):
        k = (r+k).reshape(-1,1,3)
        r = r * scale

    k = k.reshape(-1,3)
    s = mag2polari(k)
    return s

def multIterColorSeq(center,rule,scale,time):
    a = []
    for m in rule:
        a.append(polar2magf(np.array(m).astype('float')-center))
    cen  = np.array(center).astype('float')

    #r = polar2magf(rule)
    k = polar2magf(cen)

    for i in range(time):
        for j in range(len(a)):
            k = (a[j]+k).reshape(-1,1,3)
            a = list(map(lambda x: x*scale[j],a))

    k = k.reshape(-1,3)
    s = mag2polari(k)
    return s

def genRule(rulelen,rulemin,rulemax):
    a = []
    for i in range(rulelen):
        r = np.random.random(np.random.randint(rulemin,rulemax)*3).reshape(-1,3)
        a.append(r)
    return a


if __name__ == "__main__":
    print(dir())
    #recColors()
