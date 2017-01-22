#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

import numpy as np
#from npcvt import nprgb2jch,npvalidrgb
from colorindex import sjch2rgb#jch_rgb_index,c_valid_index
from PIL import Image
#from mask_gui import showmask
#from contour_gui import showcontour
import sys,os

def count_image(im):
    """
    判别图片 Image 的总颜色数，以及每个颜色所占像素量
    返回值: [[颜色],[数量]]
    """
    rgb = np.array(im).reshape(-1,3).astype('uint32')
    packedrgb=(255<<24|rgb[:,0]<<16|rgb[:,1]<<8|rgb[:,2]).flatten()#.tobytes()
    #total = np.zeros((256,256,256))==1
    #total[rgb[:,0],rgb[:,1],rgb[:,2]] = True
    #return np.sum(total)#int(np.sum(total)*100/(256**3))
    return np.unique(packedrgb,return_counts=True)

def count_jch(jch):
    """
    判别 jch 数列 的总颜色数，以及每个颜色所占像素量
    返回值: [[颜色],[数量]]
    """
    rgb = sjch2rgb(jch).reshape(-1,3).astype('uint32')#jch_rgb_index[jch[:,0],jch[:,1],jch[:,2]].reshape(-1,3).astype('uint32')
    packedrgb=(255<<24|rgb[:,0]<<16|rgb[:,1]<<8|rgb[:,2]).flatten()#.tobytes()
    return np.unique(packedrgb,return_counts=True)


#def polar2magf(polar):
#    """polar 要先转成0-1之间的小数，polar/[100,115,360] """
#    if polar.ndim >2:
#        shape = polar.shape
#        polar.resize(-1,3)
#        r_c = polar[:,1]
#        r_h = polar[:,2]*2*np.pi
#
#        r_z = polar[:,0]
#        r_x = r_c * np.cos(r_h)
#        r_y = r_c * np.sin(r_h)
#        s = np.array([r_x,r_y,r_z]).T.reshape(-1,3),astype('float').reshape(shape)
#        return s
#    elif polar.ndim == 2:
#        r_c = polar[:,1]
#        r_h = polar[:,2]*2*np.pi
#
#        r_z = polar[:,0]
#        r_x = r_c * np.cos(r_h)
#        r_y = r_c * np.sin(r_h)
#        return np.array([r_x,r_y,r_z]).T.reshape(-1,3).astype('float')
#    elif polar.ndim == 1:
#        c_z = polar[0]
#        c_x = polar[1]*np.cos(polar[2]).astype('float')
#        c_y = polar[1]*np.sin(polar[2]).astype('float')
#        return np.array([c_x,c_y,c_z]).T.reshape(-1,3).astype('float')
#    else:
#        return 0
#
#def mag2polarf(mag):
#    if mag.ndim >2:
#        shape = mag.shape
#        mag.resize(-1,3)
#        x = mag[:,0]
#        y = mag[:,1]
#
#        J = nLimitAdd(0,0,1)(mag[:,2])
#        C = np.sqrt(np.square(y)+np.square(x))
#        H = nCircleAdd(0,0,1)(np.arctan2(y,x)/(np.pi*2))
#        s = np.array([J,C,H]).T.astype('float').reshape(shape)
#        return s
#    elif mag.ndim == 2:
#        x = mag[:,0]
#        y = mag[:,1]
#
#        J = nLimitAdd(0,0,1)(mag[:,2])
#        C = np.sqrt(np.square(y)+np.square(x))
#        H = nCircleAdd(0,0,1)(np.arctan2(y,x)/(np.pi*2))
#        s = np.array([J,C,H]).T.astype('float')
#        return s
#    elif mag.ndim == 1:
#        J = nLimitAdd(0,0,1)(k[2])
#        C = np.sqrt(np.square(k[1])+np.square(k[0]))
#        H = nCircleAdd(0,0,1)(np.arctan2(y,x)/(np.pi*2))
#        return np.array([J,C,H]).T.astype('float')
#    else : return 0
#
#def mag2polari(mag):
#    return mag2polarf(mag)*np.array([100,100,360]).astype('int32')
#
#def polar2magi(polar):
#    return polar2magf
#
#def projection_cube(jch,shape):
#    rgb = jch_rgb_index[jch[:,0],jch[:,1],jch[:2]].reshape(-1,3)
#


if __name__=="__main__":
    import sys,os
    from base_relations import image_path
    from sImga import tst
    if len(sys.argv)>1:
        a = Image.open(image_path+sys.argv[1])#image_path+'a.jpg')
        #b = tst
    else:
        a = Image.open(image_path+'a.jpg')
    colors , stat = count_image(a)
    b = tst("a.jpg")
    c2,s2 = count_jch(b.jch)
    print(len(colors),np.amax(stat))
    print(len(c2),np.amax(s2))
    #a.show()
    #b.show()
