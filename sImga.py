#!/usr/bin/python3.4
#-*- coding:utf-8 -*-
import numpy as np
from npcvt import nprgb2jch,npvalidrgb
from colorindex import jch2rgb,sjch2rgb,sjch_rgb_index#jch_rgb_index,c_valid_index
from PIL import Image

from mask_gui import showmask
from contour_gui import showcontour
from base_functions import count_jch
import sys,os

#from dimension.colorconvertc import rgb2jch
# tone,area,accent
# 明度，纯度，色相
LOW_TONE,MID_TONE,HIGH_TONE,MIDLOW_TONE,MIDHIGH_TONE,LOWHIGH_TONE,AVER_TONE = (0,1,2,3,4,5,6)
LOW_AREA,MID_AREA,HIGH_AREA,MIDLOW_AREA,MIDHIGH_AREA,LOWHIGH_AREA,AVER_AREA = (0,1,2,3,4,5,6)
WARM_ACCE,MID_ACCE,COLD_ACCE =(0,1,2)

tone_info = ("低调","中调","高调","中低调","中高调","高低调","间调")
area_info = ("低纯","中纯","高纯","中低纯","中高纯","高低纯","间纯")
accent_info= ("暖色","间色","冷色")

class Img:
    """
    这个类创建一个可调节 明度 纯度 色相 的数据结构
    This class creates an data type that is allowed to mod j c h
    """
    def __init__(self):
        #if image.mode != "RGB":
        #    image = image.convert("RGB")
        #rgb = np.array(image)
        #self.shape = rgb.shape
        #self.jch   = nprgb2jch(rgb.reshape(-1,3)).astype('int16')
        self.shape = ()
        self.jch   = None
        self.dirty = False
        self.pic   = None
        self.jhistogram = None
        self.chistogram = None
        self.hhistogram = None
        self.jhistpic   = None
        self.chistpic   = None
        self.hhistpic   = None

    def _new(self,img):
        new = Img()
        new.shape = img.shape
        new.jch   = img.jch.copy()
        return new

    def copy(self):
        return self._new(self)

    def __repr__(self):
        color,stat = self.statcolor()
        cnum = len(color)
        maxvalue = np.amax(stat)
        minvalue = np.amin(stat)
        total = self.shape[0]*self.shape[1]
        ind   = np.argwhere(stat==maxvalue)[0,0]
        #c32 = None
        #if len(ind)>1:
        #    c32   = color[ind[0]]
        #else:
        c32   = color[ind]
        r = (c32>>16)%256
        g = (c32>>8)%256
        b = c32%256
        #print(r,g,b)
        #jch = rgb2jch([r,g,b])
        jch = nprgb2jch(np.array([[r,g,b]]))        #.astype('int')
        return ("<%s,%s at %s>\n__%s %s__\n__%s %s__\n__%s %s__\n用色:%s,总数:%s,平均重复:%s\n最多:%s,颜色:jch:%s,rgb:%s,最少:%s" %\
                (self.__class__.__module__,self.shape,id(self),\
                 tone_info[self.whichtone()],self.gettone(),\
                 area_info[self.whicharea()],self.getarea(),\
                 accent_info[self.whichaccent()],self.getaccent(),\
                 cnum,total,int(total/cnum),maxvalue,jch,np.array([r,g,b]),minvalue))

    def statcolor(self):
        #a = self.jch
        #rgb = jch_rgb_index[a[:,0],a[:,1],a[:,2]].reshape(self.shape)
        #total = np.zeros((256,256,256))==1
        #total[rgb[:,0],rgb[:,1],rgb[:,2]] = True
        #color,stat = count_jch(self.jch)
        return count_jch(self.jch)

    def anacolors(self):
        pass

    def show(self):
        if self.dirty or self.pic==None:
            a = self.jch
            rgb = sjch2rgb(self.jch).reshape(self.shape)
                           #jch_rgb_index[a[:,0],a[:,1],a[:,2]].reshape(self.shape)
            self.pic = Image.fromarray(rgb)
            self.dirty = False
        self.pic.show()

    def jhist(self):
        if self.dirty or self.jhistogram==None:
            jmap = (np.ones((200,202),dtype='int')*np.arange(202)*(255/200)).astype('int')
            jstat,k= np.histogram(self.jch[:,0].astype('int'),bins=np.arange(102))
            #print(np.amin(self.jch[:,0]))
            #print(jstat,len(k))
            jnorm= (jstat*100/np.amax(jstat)).astype('int')
            for i in range(202):
                jmap[:(200-jnorm[i//2]*2),i]=255
                if i==66 or i == 132:
                    jmap[(200-jnorm[i//2]*2):,i]=100
                #jmap[i,jnorm[i]:]=255
            #jmap[]
            mean = np.mean(self.jch[:,0])
            aver = np.average(self.jch[:,0])
            jmap[(100-mean)*2,:]=0
            jmap[(100-aver)*2,:]=100
            self.jhistogram = jmap.astype('uint8')

        return self.jhistogram

    def chist(self):
        if self.dirty or self.chistogram==None:
            cmap = np.ones((200,230),dtype='int')*(np.arange(230)//2)
            cstat,k= np.histogram(self.jch[:,1].astype('int'),bins=np.arange(116))
            #print(np.amin(self.jch[:,0]))
            #print(jstat,len(k))
            cnorm= (cstat*200/np.amax(cstat)).astype('int')
            for i in range(230):
                cmap[:(200-cnorm[i//2]),i]=200
                if i==76 or i == 152:
                    cmap[(200-cnorm[i//2]):,i]=100
                #jmap[i,jnorm[i]:]=255
            #jmap[]
            mean = np.mean(self.jch[:,1])
            aver = np.average(self.jch[:,1])
            cmap[(100-mean)*2,:]=30
            cmap[(100-aver)*2,:]=30
            self.chistogram = cmap.astype('uint8')
        return self.chistogram

    def hhist(self):
        if self.dirty or self.hhistogram==None:
            hmap = np.ones((200,360),dtype='int')*(np.arange(360))
            hstat,k= np.histogram(self.jch[:,2].astype('int'),bins=np.arange(361))
            #print(np.amin(self.jch[:,0]))
            #print(jstat,len(k))
            hnorm= (hstat*200/np.amax(hstat)).astype('int')
            for i in range(360):
                hmap[:(200-hnorm[i]),i]=500
                #if i==120 or i == 2:
                #    cmap[(200-cnorm[i//2]):,i]=100
                #jmap[i,jnorm[i]:]=255
            #jmap[]
            #mean = np.mean(self.jch[:,2])
            #aver = np.average(self.jch[:,2])
            #cmap[(100-mean)*2,:]=0
            #cmap[(100-aver)*2,:]=100
            self.hhistogram = hmap.astype('int')
        return self.hhistogram

    def _getjhistpic(self):
        if self.dirty or self.jhistpic==None:
            self.jhistpic = Image.fromarray(self.jhist())
        return self.jhistpic

    def _getchistpic(self):
        if self.dirty or self.chistpic==None:
            c_ = self.chist()
            shape = c_.shape#+(3,)
            c  = c_.reshape(-1)
            j = np.ones(c.shape,dtype='uint8')*80
            j = np.where(c>150,99,j)
            c = np.where(c>150,0,c)
            h = np.ones(c.shape,dtype='uint8')*140
            rgb = sjch2rgb(np.array([j,c,h]).T).reshape(shape+(3,))
            #jch_rgb_index[j,c,h].reshape(shape+(3,))
            self.chistpic = Image.fromarray(rgb) #.resize((200,200))
        return self.chistpic

    def _gethhistpic(self):
        if self.dirty or self.hhistpic==None:
            h_ = self.hhist()
            shape = h_.shape#+(3,)
            h  = h_.reshape(-1)
            j = np.ones(h.shape,dtype='int')*45
            j = np.where(h>400,99,j)
            h  = np.where(h>400,0,h)
            c = np.ones(h.shape,dtype='uint8')*44
            rgb = sjch2rgb(np.array([j,c,h]).T).reshape(shape+(3,))
            #jch_rgb_index[j,c,h].reshape(shape+(3,))
            self.hhistpic = Image.fromarray(rgb) #.resize((200,200))
        return self.hhistpic



    def showchist(self):
        #c_ = self.chist()
        #shape = c_.shape#+(3,)
        #c  = c_.reshape(-1)
        #j = np.ones(c.shape,dtype='uint8')*45
        #h = np.ones(c.shape,dtype='uint8')*14
        #rgb = jch_rgb_index[j,c,h].reshape(shape+(3,))
        #pic = Image.fromarray(rgb) #.resize((200,200))
        pic = self._getchistpic()#Image.fromarray(self.chist()) #.resize((200,200))

        pic.show()

    def showjhist(self):
        pic = self._getjhistpic()#Image.fromarray(self.jhist()) #.resize((200,200))
        pic.show()

    def showhhist(self):
        pic = self._gethhistpic()#Image.fromarray(self.jhist()) #.resize((200,200))
        pic.show()

    def showhist(self):
        p = Image.new('RGB',(1080,200),color=0x888888)
        p_j = self._getjhistpic().convert('RGB')
        p_c = self._getchistpic()
        p_h = self._gethhistpic()
        p.paste(p_j,(0,0))
        p.paste(p_c,(360,0))
        p.paste(p_h,(720,0))
        p.show()

    def showinfo(self):
        p = Image.new('RGB',(1080,800),color=0x888888)
        p_j = self._getjhistpic().convert('RGB')
        p_c = self._getchistpic()
        p_h = self._gethhistpic()
        p.paste(p_j,(0,0))
        p.paste(p_c,(360,0))
        p.paste(p_h,(720,0))
        j_ = self.jch[:,0]#.reshape(self.shape[:-1])
        cj = np.zeros(j_.shape)
        hj = np.zeros(j_.shape)
        #j_map = Image.fromarray(j_).convert('RGB')
        j_rgb = sjch2rgb(np.array([j_,cj,hj]).T).reshape(self.shape)
            #sjch_rgb_index[j_,0,0].reshape(self.shape)

        c_ = self.jch[:,1]#.reshape(self.shape(-1))
        jc = np.ones(c_.shape)*50
        hc = np.ones(c_.shape)*14
        c_rgb = sjch2rgb(np.array([jc,c_,hc]).T).reshape(self.shape)
        #jch_rgb_index[50,c_,14].reshape(self.shape)
        #c_rgb = jch_rgb_index[cj,c_,ch].reshape(self.shape)

        h_ = self.jch[:,2]
        jh = np.ones(h_.shape)*60
        ch = np.ones(h_.shape)*100
        h_rgb = sjch2rgb(np.array([jh,ch,h_]).T).reshape(self.shape)
        #jch_rgb_index[60,100,self.jch[:,2]].reshape(self.shape)

        proportion = max(self.shape[0]/600,self.shape[1]/360)

        y = int(self.shape[0]/proportion)
        x = int(self.shape[1]/proportion)
        #print(x,y)

        p1 = Image.fromarray(j_rgb).resize((x,y))
        p2 = Image.fromarray(c_rgb).resize((x,y))
        p3 = Image.fromarray(h_rgb).resize((x,y))

        p.paste(p1,(0,200))
        p.paste(p2,(360,200))
        p.paste(p3,(720,200))
        p.show()

    def showmaskmap(self):
        showmask(self.jch,self.shape)
        #try:
        #    pid = os.fork()
        #    if pid ==0:
        #        jch = self.jch
        #        shape = self.shape
        #        showmask(jch,shape)
        #    else:
        #        return 0
        #except OSError as e:
        #    pass

    def showcontourmap(self):
        showcontour(self.jch,self.shape)
        #try:
        #    pid = os.fork()
        #    if pid ==0:
        #        jch = self.jch
        #        shape = self.shape
        #        showcontour(jch,shape)
        #    else:
        #        return 0
        #except OSError as e:
        #    pass
        #showcontour(self.jch,self.shape)

    #以上为显示直方图，映射图
    def gettone(self):
        tone = np.histogram(self.jch[:,0].astype('int'),bins=(0,33,67,100))[0]
        tone = tone*100/(np.sum(tone))
        return tone.astype('int')

    def whichtone(self):
        tone = self.gettone()
        #print("tone",tone)
        if tone[0]>=50:
            return LOW_TONE
        elif tone[1]>=50:
            return MID_TONE
        elif tone[2]>=50:
            return HIGH_TONE
        elif tone[0]<7:
            return MIDHIGH_TONE
        elif tone[1]<7:
            return LOWHIGH_TONE
        elif tone[2]<7:
            return MIDLOW_TONE
        else:
            return AVER_TONE

    def islowtone(self):
        return self.whichtone()==LOW_TONE

    def ismidtone(self):
        return self.whichtone()==MID_TONE

    def ishightone(self):
        return self.whichtone()==HIGH_TONE

    def isavertone(self):
        return self.whichtone()==AVER_TONE

    def ismidlowtone(self):
        return self.whichtone()==MIDLOW_TONE

    def ismidhightone(self):
        return self.whichtone()==MIDHIGH_TONE

    def islowhightone(self):
        return self.whichtone()==LOWHIGH_TONE

    def getarea(self):
        area = np.histogram(self.jch[:,1],bins=(0,20,40,115))[0]
        area = area*100/(np.sum(area))
        return area.astype('int')

    def whicharea(self):
        area = self.getarea()
        if area[0]>=50:
            return LOW_AREA
        elif area[1]>=50:
            return MID_AREA
        elif area[2]>=50:
            return HIGH_AREA
        elif area[0]<7:
            return MIDHIGH_AREA
        elif area[1]<7:
            return LOWHIGH_AREA
        elif area[2]<7:
            return MIDHIGH_AREA
        else:
            return AVER_AREA

    def islowarea(self):
        return self.whicharea()==LOW_AREA

    def ismidarea(self):
        return self.whicharea()==MID_AREA

    def ishigharea(self):
        return self.whicharea()==HIGH_AREA

    def isaverarea(self):
        return self.whicharea()==AVER_AREA

    def ismidlowarea(self):
        return self.whicharea()==MIDLOW_AREA

    def ismidhigharea(self):
        return self.whicharea()==MIDHIGH_AREA

    def islowhigharea(self):
        return self.whicharea()==LOWHIGH_AREA

    def getaccent(self):
        color = np.histogram(self.jch[:,2],bins=(0,110,290,360))[0]
        color = color*100/(np.sum(color))
        return color.astype('int')


    def whichaccent(self):
        color = self.getaccent()
        if color[1]>=75:
            return COLD_ACCE
        elif color[1]<25:
            return WARM_ACCE
        else:
            return MID_ACCE

    def iswarmaccent(self):
        return self.whichaccent()==WARM_ACCE

    def iscoldaccent(self):
        return self.whichaccent()==COLD_ACCE

    def ismidaccent(self):
        return self.whichaccent()==MID_ACCE



def fromimage(image):
    """
    从PIL.Image格式 生成img
    """
    if image.mode != "RGB":
        image = image.convert("RGB")
    rgb = np.array(image)
    shape = rgb.shape
    jch = nprgb2jch(rgb.reshape(-1,3))#.astype('int16')
    n   = Img()
    n.shape = shape
    n.jch   = jch
    return n

def fromarray(arr):
    """
    从numpy.array格式 生成img
    arr 需要以jch信息提供
    """
    n = Img()
    n.shape = arr.shape
    n.jch   = arr.reshape(-1,3)
    return n
        #self.shape = ()

        #self.jch   = np.array([],dtype='int16')

def pict(name):
    from base_relations import image_path
    a = Image.open(image_path+name)
    s = fromimage(a)
    a.close()
    return s

def tst(img,flood=50):
    from base_relations import image_path
    #a = Image.open(image_path + name)
    s = img.copy()#fromimage(a)
    #a.close()
    from effects import strengthen_tst
    j = s.jch[:,0].reshape(s.shape[:-1])
    j = strengthen_tst(j,flood)
    j = np.where(j>100,100,j)
    s.jch[:,0] = j.reshape(-1)
    return s

def tst2(img):
    from base_relations import image_path
    #a = Image.open(image_path + name)
    s = img.copy()#fromimage(a)
    #a.close()
    from effects import strengthen_tst2
    j = s.jch[:,0].reshape(s.shape[:-1])
    j = strengthen_tst2(j)
    j = np.where(j>100,100,j)
    s.jch[:,0] = j.reshape(-1)
    return s

def tst3(img):
    from base_relations import image_path
    s = img.copy()#fromimage(a)
    from effects import strengthen_tst3
    j = s.jch[:,0].reshape(s.shape[:-1])
    j = strengthen_tst3(j)
    j = np.where(j>100,100,j)
    s.jch[:,0] = j.reshape(-1)
    return s

def ad_c_range(img,low,high):
    from base_relations import image_path
    s = img.copy()
    from effects import adjust_range
    j = s.jch[:,1].reshape(s.shape[:-1])
    j = adjust_range(j,low,high)
    s.jch[:,1] = j.reshape(-1)
    return s

def ad_c_range_exp(img,maxvalue=115):
    from base_relations import image_path
    s = img.copy()
    from effects import adjust_range_exp
    j = s.jch[:,1].reshape(s.shape[:-1])
    j = adjust_range_exp(j,maxvalue=maxvalue)
    s.jch[:,1] = j.reshape(-1)
    return s

if __name__=="__main__":
    from base_relations import image_path
    a = None
    if len(sys.argv)>1:
        a = Image.open(image_path+sys.argv[1])  #'a.jpg')
    else:
        a = Image.open(image_path+'a.jpg')

    s = fromimage(a)
    a.close()
    s.showinfo()
    print(s)#.statcolor())
    s.show()
    #s.showmaskmap()
