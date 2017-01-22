#!/usr/bin/python3.4
#-*- coding:utf-8 -*-

import numpy as np
from PIL import Image
from Imga import tst
from effects import *

def tst_visual(pic,jch_=0):
    a = tst(pic)
    j = a.jch[:,jch_].reshape(a.shape[:-1])
    map = gap_map(j)
    v_map = visualize_map(map)
    im = Image.fromarray(v_map)
    im.show()



if __name__=="__main__":
    import sys
    tst_visual(sys.argv[1],sys.argv[2])
