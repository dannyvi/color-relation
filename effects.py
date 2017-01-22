#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

import numpy as np

def parallel_matrix(mat,x,y,rotation=False):
    x = -x
    y = -y
    if abs(x)>mat.shape[1]:
        x = np.sign(x)*(mat.shape[1])
    if abs(y)>mat.shape[0]:
        y = np.sign(y)*(mat.shape[0])
    mat2 = np.zeros(mat.shape,dtype = mat.dtype)
    mat3 = np.zeros(mat.shape,dtype = mat.dtype)
    if not rotation :
        if x > 0:
            mat2[:,x:] = mat[:,:-x]
            mat2[:,:x] = mat[:,np.zeros(x,dtype='int')]
        elif x==0:
            mat2 = mat
        else:
            mat2[:,:x] = mat[:,-x:]
            mat2[:,x:] = mat[:,np.ones(-x,dtype='int')*(-1)]
        if y > 0:
            mat3[y:] = mat2[:-y]
            mat3[:y] = mat2[np.zeros(y,dtype='int')]
        elif y==0:
            mat3 = mat2
        else:
            mat3[:y] = mat2[-y:]
            mat3[y:] = mat2[np.ones(-y,dtype='int')*(-1)]
        return mat3
    else:
        if x > 0:
            mat2[:,x:] = mat[:,:-x]
            mat2[:,:x] = mat[:,-x:]
        elif x==0:
            mat2 = mat
        else:
            mat2[:,:x] = mat[:,-x:]
            mat2[:,x:] = mat[:,:-x]
        if y > 0:
            mat3[y:] = mat2[:-y]
            mat3[:y] = mat2[-y:]
        elif y==0:
            mat3 = mat2
        else:
            mat3[:y] = mat2[-y:]
            mat3[y:] = mat2[:-y]
        return mat3

def gaussian_blur(mat,radius=1,weight=0):
    diameter = radius*2+1
    if weight == 0:
        weight = np.ones((diameter,diameter))/(diameter**2)
    #print(weight)
    mat_a = np.zeros([diameter,diameter]+list(mat.shape))
    for i in range(-radius,radius+1):
        for j in range(-radius,radius+1):
            mat_a[i+radius,j+radius] = parallel_matrix(mat,i,j)*weight[i+radius,j+radius]
    #        print(mat_a[i+radius,j+radius])
    #print(mat_a)
    k = np.sum(mat_a.reshape(diameter**2,mat.shape[0],mat.shape[1]),axis=0)
    return k.astype(mat.dtype)

def in_range(mat):
    return (np.min(mat),np.max(mat))

def adjust_range(mat,low,high):
    minv,maxv = in_range(mat)
    mat2 = (mat-minv)*(high-low)/(maxv-minv)+low
    return mat2

def adjust_range_exp(mat,maxvalue=100):
    mat = mat/maxvalue
    #low = low/maxvalue
    #high=high/maxvalue
    #minv,maxv = in_range(mat)
    mat2 = (mat**0.5)*maxvalue      #*(high-low)/(maxv-minv)+low
    return mat2

def differ_map(mat,unit=1):
    shape = mat.shape
    #横关系图
    #mat1 = np.zeros((shape[0],mat.shape[1]-1),dtype = mat.dtype)
    dif_horizon =mat[:,unit::unit]-mat[:,:-unit:unit]
    #纵关系图
    dif_vertical =mat[unit::unit,:]-mat[:-unit:unit,:]
    return [dif_horizon,dif_vertical]

def differ_cross(mat,unit=1):
    #shape = mat.shape
    dif_rs = mat[unit::unit,unit::unit]-mat[:-unit:unit,:-unit:unit]
    dif_ls = mat[:-unit:unit,unit::unit]-mat[unit::unit,:-unit:unit]
    return [dif_rs,dif_ls]

def gap_4_map(mat,unit=1):
    diff_h,diff_v = differ_map(mat,unit)
    diff_h = np.abs(diff_h[::unit,:])
    diff_v = np.abs(diff_v[:,::unit])
    pad_h  = np.zeros((diff_h.shape[0],diff_h.shape[1]+2),dtype=mat.dtype)
    pad_v  = np.zeros((diff_v.shape[0]+2,diff_v.shape[1]),dtype=mat.dtype)
    pad_h[:,1:-1] = diff_h
    pad_v[1:-1,:] = diff_v
    gap_m  = np.zeros((pad_h.shape[0],pad_v.shape[1]),dtype=mat.dtype)
    gap_up  = pad_v[:-1,:]
    gap_down= pad_v[1:,:]
    gap_left= pad_h[:,:-1]
    gap_right=pad_h[:,1:]
    gap_m  = gap_up+gap_down+gap_left+gap_right
    #max_value = np.max(gap_map)
    return gap_m/4
    #pass


def gap_8_map(mat,unit=1):
    diff_h,diff_v = differ_map(mat,unit)
    diff_l,diff_r = differ_cross(mat,unit)
    diff_h = np.abs(diff_h[::unit,:])
    diff_v = np.abs(diff_v[:,::unit])
    diff_l = np.abs(diff_l)
    diff_r = np.abs(diff_r)
    pad_h  = np.zeros((diff_h.shape[0],diff_h.shape[1]+2),dtype=mat.dtype)
    pad_v  = np.zeros((diff_v.shape[0]+2,diff_v.shape[1]),dtype=mat.dtype)
    pad_l  = np.zeros((diff_l.shape[0]+2,diff_l.shape[1]+2),dtype=mat.dtype)
    pad_r  = np.zeros((diff_r.shape[0]+2,diff_r.shape[1]+2),dtype=mat.dtype)
    #pad_l  =
    pad_h[:,1:-1] = diff_h
    pad_v[1:-1,:] = diff_v
    pad_l[1:-1,1:-1]= diff_l
    pad_r[1:-1,1:-1]= diff_r
    gap_m  = np.zeros((pad_h.shape[0],pad_v.shape[1]),dtype=mat.dtype)
    gap_up  = pad_v[:-1,:]
    gap_down= pad_v[1:,:]
    gap_left= pad_h[:,:-1]
    gap_right=pad_h[:,1:]
    gap_ul  = pad_r[:-1,:-1]
    gap_dr  = pad_r[1:,1:]
    gap_ur  = pad_l[:-1,:-1]
    gap_dl  = pad_l[1:,1:]
    gap_m  = gap_up+gap_down+gap_left+gap_right+gap_ul+gap_dr+gap_ur+gap_dl
    #max_value = np.max(gap_map)
    return gap_m/8
    #pass


def visualize_map(mat):
    prop = np.max(mat)/255
    return np.abs(mat/prop).astype('uint8')

def strengthen_tst(mat,flood=50):
    gap_view = gap_8_map(mat)
    blured_view = gaussian_blur(mat)
    direction = np.where(mat>blured_view,1,-1)
    proportion = max(100-np.max(mat),np.min(mat),10)/100
    #flood = 70
    area = np.where(gap_view>np.max(gap_view)-flood,True,False)
    result = np.where(area,mat*((1+proportion)**direction),mat)
    result = np.where(result>100,100,result)
    return result

def strengthen_tst2(mat,top=100.0):
    #指数效果增强
    #gap_view = gap_8_map(mat)
    blured_view = gaussian_blur(mat)
    mat = mat/top
    blured_view = blured_view/top
    #direction = np.where(mat>blured_view,1,-1)
    #proportion = max(100-np.max(mat),np.min(mat),10)/100
    #flood = 70
    #area = np.where(gap_view>np.average(gap_view),True,False)
    #result = np.where(area,mat*((1+proportion)**direction),mat)
    #result = mat ** (blured_view/mat)
    result = np.where(mat==0,mat,mat ** ((blured_view+0.01)/(mat+0.01)))
    result = result * top
    return result

def strengthen_tst3(mat,top=100.0):
    #指数效果增强
    gap_view = gap_8_map(mat)
    blured_view = gaussian_blur(mat)
    mat = mat/top
    blured_view = blured_view/top
    #direction = np.where(mat>blured_view,1,-1)
    #proportion = max(100-np.max(mat),np.min(mat),10)/100
    #flood = 70
    area = np.where(gap_view>np.average(gap_view),True,False)
    strengthed = np.where(mat==0,mat,mat**((blured_view+0.01)/(mat+0.01)))
    weaked     = np.where(mat==0,mat,mat**((mat+0.01)/(blured_view+0.01)))
    result = np.where(area,strengthed,weaked)
    #result = np.where(mat==0,mat,mat ** (blured_view/mat))
    result = result * top
    return result
