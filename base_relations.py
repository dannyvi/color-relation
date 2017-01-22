#!/usr/bin/python3.4
#-*- coding:utf-8 -*-
import numpy as np
from npcvt import nprgb2jch,npvalidrgb
from colorindex import jch_rgb_index,c_valid_index
from PIL import Image

mask_value=[0,255,255]

def image2jch(filename):
    f = Image.open(filename).convert('RGB')
    a = np.array(f)
    f.close()
    return nprgb2jch(a.reshape(-1,3)).reshape(a.shape).astype('int')

def jch2image(jcho):
    jch = jcho.astype('int').reshape(-1,3)
    f = jch_rgb_index[jch[:,0],jch[:,1],jch[:,2]].reshape(jcho.shape)
    return Image.fromarray(f)

def j_lin(j2,center,proportion,outrange=False,replace=[[30,114,280],[50,114,14]]):
    jch = j2.reshape(-1,3)
    jch= (jch-[center,0,0])*[1+proportion,1,1]+[center,0,0]
    if not outrange:
        jch[...,0] = np.where(jch[...,0]<0,0,jch[...,0])
        jch[...,0] = np.where(jch[...,0]>100,100,jch[...,0])
        return jch.reshape(j2.shape).astype('int')
    else:
        j = jch[:,0]
        low_valid = j<0 #np.all(jch<0,1)
        jch[low_valid] = replace[0] #= np.where(low_valid,replace[0],jch)
        high_valid= j>100#np.all(jch>100,1)
        jch[high_valid]= replace[1] #= np.where(high_valid,replace[1],jch)
        return jch.reshape(j2.shape).astype('int')

def c_lin(j2,center,proportion,outrange=False,replace=\
          [[40,114,300],[80,114,140],[90,114,100]]):
    jch = j2.reshape(-1,3)
    jch= ((jch-[0,center,0])*[1,1+proportion,1]+[0,center,0]).astype('int')
    if not outrange:
        jch[...,1] = np.where(jch[...,1]<0,0,jch[...,1])
        jch[...,1] = np.where(jch[...,1]>114,114,jch[...,1])
        return jch.reshape(j2.shape).astype('int')
    else:
        c = jch[:,1]
        low_valid = c<0
        high_valid = c>114
        jch[low_valid] = replace[0]
        jch[high_valid] = replace[1]
        c_valid = np.invert(c_valid_index[jch[:,0],jch[:,1],jch[:,2]])
        jch[c_valid] = replace[2]
        jch[low_valid] = replace[0]
        jch[high_valid] = replace[1]
        return jch.reshape(j2.shape).astype('int')

def distribution(jch,prt="c"):
    prt_dict = {"j":0,"c":1,"h":2}
    #jch = j2.reshape(-1,3)
    seq = jch[...,prt_dict[prt]].astype('uint8')
    return Image.fromarray(seq)

image_path = "/Users/yudan/Documents/mypicworks/samples/"

def tst(name,center,prop,func,**kwargs):
    a = image2jch(image_path+name)
    jch = func(a,center,prop,kwargs)
    return jch2image(jch)

def tst2():
    b = Image.open(image_path+"m.jpg")
    e = Image.open(image_path+"l.jpg")
    f = Image.open(image_path+"k.jpg")
    #b = image2jch(image_path+"b.jpg")
    #e = image2jch(image_path+"e.jpg")
    #f = image2jch(image_path+"f.jpg")
    size = (1000,1000)
    samp = Image.BICUBIC
    s1 = b.resize(size,samp)
    s2 = e.resize(size,samp)
    s3 = f.resize(size,samp)

    # nprgb2jch(a.reshape(-1,3)).reshape(a.shape).astype('int')
    #b = #image2jch(b)
    #e = #image2jch(e)
    #f = #image2jch(f)
    g = np.array
    jch1 = nprgb2jch(g(s1).reshape(-1,3)).reshape(g(s1).shape).astype('int')
    jch2 = nprgb2jch(g(s2).reshape(-1,3)).reshape(g(s2).shape).astype('int')
    jch3 = nprgb2jch(g(s3).reshape(-1,3)).reshape(g(s3).shape).astype('int')
    #jch2 = image2jch(s2)
    #jch3 = image2jch(s3)
    jjj  = np.zeros(jch1.shape,dtype="int")
    jjj[...,0]=jch1[...,0]
    jjj[...,1]=jch2[...,1]
    jjj[...,2]=jch3[...,2]
    return (jch2image(jjj),s1,s2,s3)
#if __name__=="__main__":
#    from
