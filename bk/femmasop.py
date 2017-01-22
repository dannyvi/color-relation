#!/usr/local/bin/python3.4
#-*-coding:utf-8-*-

from functools import reduce
import numpy as np
from dimension.colorconvertc import jch2rgb


nian_yue = np.array(((2,3,2,3,4,5,6,7,8,9,0,1),\
                     (4,5,4,5,6,7,8,9,0,1,2,3),\
                     (6,7,6,7,8,9,0,1,2,3,4,5),\
                     (8,9,8,9,0,1,2,3,4,5,6,7),\
                     (0,1,0,1,2,3,4,5,6,7,8,9)))

#日干定时
ri_shi = np.array( ((0,1,2,3,4,5,6,7,8,9,0,1),\
                    (2,3,4,5,6,7,8,9,0,1,2,3),\
                    (4,5,6,7,8,9,0,1,2,3,4,5),\
                    (6,7,8,9,0,1,2,3,4,5,6,7),\
                    (8,9,0,1,2,3,4,5,6,7,8,9)))

#年份排序表
year_queue = np.array((( 0,  0, 50,  0, 40,  0, 30,  0, 20,  0, 10,  0),\
                       ( 0,  1,  0, 51,  0, 41,  0, 31,  0, 21,  0, 11),\
                       (12,  0,  2,  0, 52,  0, 42,  0, 32,  0, 22,  0),\
                       ( 0, 13,  0,  3,  0, 53,  0, 43,  0, 33,  0, 23),\
                       (24,  0, 14,  0,  4,  0, 54,  0, 44,  0, 34,  0),\
                       ( 0, 25,  0, 15,  0,  5,  0, 55,  0, 45,  0, 35),\
                       (36,  0, 26,  0, 16,  0,  6,  0, 56,  0, 46,  0),\
                       ( 0, 37,  0, 27,  0, 17,  0,  7,  0, 57,  0, 47),\
                       (48,  0, 38,  0, 28,  0, 18,  0,  8,  0, 58,  0),\
                       ( 0, 49,  0, 39,  0, 29,  0, 19,  0,  9,  0, 59)))

# 天干地支名
tian_gan =np.array( ("甲","乙","丙","丁","戊","己","庚","辛","壬","癸"))
di_zhi   =np.array( ("子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"))

tian_math=np.array(('٩','٨','٧','٦','٥','٤','٣','٢','١','٠'))
#tian_math=np.array(('1','2','3','4','5','6','7','8','9','0'))
di_math=np.array(('१','२','३','४','५','६','७','८','९','०','ा','ः'))
#干支吉凶
tian_di_state =np.array( (
    ("沐","冠","临","帝","衰","病","死","墓","绝","胎","养","生"),\
    ("病","衰","帝","临","冠","沐","生","养","胎","绝","墓","死"),\
    ("胎","养","生","沐","冠","临","帝","衰","病","死","墓","绝"),\
    ("绝","墓","死","病","衰","帝","临","冠","沐","生","养","胎"),\
    ("胎","养","生","沐","冠","临","帝","衰","病","死","墓","绝"),\
    ("绝","墓","死","病","衰","帝","临","冠","沐","生","养","胎"),\
    ("死","墓","绝","胎","养","生","沐","冠","临","帝","衰","病"),\
    ("生","养","胎","绝","墓","死","病","衰","帝","临","冠","沐"),\
    ("帝","衰","病","死","墓","绝","胎","养","生","沐","冠","临"),\
    ("临","冠","沐","生","养","胎","绝","墓","死","病","衰","帝")))

def maxChromebyJH(j,h):
    c = 0.0
    while True:
        R,G,B = jch2rgb([j,c,h])
        if R>255 or G>255 or B>255 or R<0 or G<0 or B<0 or j<=0 or j>=100:
            break
        c += 1.0
    return c

ufunc_maxChromeByJH = np.frompyfunc(maxChromebyJH,2,1)

def CircleAdd(var,num,lower,higher):
    var+=num
    while var<lower or var>=higher:
        if var<lower:
            var=var + (higher-lower)
        elif var>=higher:
            var=var - (higher-lower)
    return var

def nCircleAdd(num,lower,higher):
    def f(var):
        var= var + num
        while var<lower or var>=higher:
            if var<lower:
                var=var + (higher-lower)
            elif var>=higher:
                var=var - (higher-lower)
        return var
    return np.frompyfunc(f,1,1)

def nLimitAdd(num,lower,higher):
    def f(var):
        var= var + num
        while var<lower or var>higher:
            if var<lower:
                var=lower #var + (higher-lower)
            elif var>higher:
                var=higher#var - (higher-lower)
        return var
    return np.frompyfunc(f,1,1)


def randomOcword():
    ev = np.random.randint(0,2,4)
    ga = np.random.randint(0,5,4)
    ea = np.random.randint(0,6,4)
    gaa = ga*2 + ev
    eaa = ea*2 + ev
    octa = np.array([gaa,eaa]).T
    octa[1][0] = nian_yue[octa[0][0] % 5][octa[1][1]]
    octa[3][0] = ri_shi[octa[2][0]%5][octa[3][1]]
    return octa.astype('int')

#def ocWord(T=)

class Ocword(np.ndarray):
    def __new__(cls,input_array=randomOcword()):
        obj = np.asarray(input_array,dtype='int').reshape(4,2).view(cls)
        return obj
    def __repr__(self):
    #    #print(self)
        return \
            tian_gan[self[0,0]]+di_zhi[self[0,1]]+" "+\
            tian_gan[self[1,0]]+di_zhi[self[1,1]]+" "+\
            tian_gan[self[2,0]]+di_zhi[self[2,1]]+" "+\
            tian_gan[self[3,0]]+di_zhi[self[3,1]]+"\n"+\
            str(self[0,0])+"-"+str(self[0,1]) + " " + \
            str(self[1,0])+"-"+str(self[1,1]) + " " + \
            str(self[2,0])+"-"+str(self[2,1]) + " " + \
            str(self[3,0])+"-"+str(self[3,1]) + "\n" +\
            tian_di_state[self[0,0]][self[0,1]]+" "+\
            tian_di_state[self[1,0]][self[1,1]]+" "+\
            tian_di_state[self[2,0]][self[2,1]]+" "+\
            tian_di_state[self[3,0]][self[3,1]]+"\n"



def ocwordSeq(octav,num,lang=[[0,60],[0,60],[0,12],[1,10]]):
    carry_seq = np.zeros(num,dtype='int')
    octav_seq = np.zeros(num*8,dtype ='int').reshape(-1,4,2)
    for i in range(4):
        g_baseseq = np.linspace(octav[3-i][0],\
                                (num-1)*lang[3-i][0]+octav[3-i][0],\
                                num,dtype='int') + carry_seq
        z_baseseq = np.linspace(octav[3-i][1],\
                                (num-1)*lang[3-i][0]+octav[3-i][1],\
                                num,dtype='int') + carry_seq
        w_num = year_queue[octav[3-i][0]][octav[3-i][1]]
        w_baseseq = np.linspace(w_num,(num-1)*lang[3-i][0]+w_num,num,\
                                dtype='int') + carry_seq
        gan_seq   = g_baseseq%10
        zhi_seq   = z_baseseq%12

        if lang[3-i][1] == 10:
            carry_seq = g_baseseq//10
        elif lang[3-i][1] == 12:
            carry_seq = z_baseseq//12
        elif lang[3-i][1] == 60:
            carry_seq = w_baseseq//60
        elif lang[3-i][1] > 0 and lang[3-i][1]<60 and isinstance(lang[3-i][1],int):
            carry_seq = w_baseseq//lang[3-i][1]
        else:
            carry_seq = w_baseseq*0
        octav_seq[:,3-i,0] = gan_seq.copy()
        octav_seq[:,3-i,1] = zhi_seq.copy()
    return octav_seq

class Ocgenerator(object):
    def __init__(self,ocword=Ocword(randomOcword()),leng=64,method=[[0,60],[1,60],[1,12],[1,10]]):
        self.oc_seed= ocword
        self.cur_seed = self.oc_seed
        self.gen_method = method
        self.seq_length = leng
        self.last_seq   = None

    def __repr__(self):
        return "OcGenerator:\n\nseed:\n"+self.oc_seed.__repr__()+\
            "\ncur_seed:\n" + self.cur_seed.__repr__()+"\n"

    def genSeq(self):
        num       = self.seq_length
        octav     = self.cur_seed
        lang      = self.gen_method
        carry_seq = np.zeros(num+1,dtype='int')
        octav_seq = np.zeros((num+1)*8,dtype ='int').reshape(-1,4,2)
        for i in range(4):
            g_baseseq = np.linspace(octav[3-i][0],\
                                    (num)*lang[3-i][0]+octav[3-i][0],\
                                    num+1,dtype='int') + carry_seq
            z_baseseq = np.linspace(octav[3-i][1],\
                                    (num)*lang[3-i][0]+octav[3-i][1],\
                                    num+1,dtype='int') + carry_seq
            w_num = year_queue[octav[3-i][0]][octav[3-i][1]]
            w_baseseq = np.linspace(w_num,(num)*lang[3-i][0]+w_num,num+1,\
                                    dtype='int') + carry_seq
            gan_seq   = g_baseseq%10
            zhi_seq   = z_baseseq%12

            if lang[3-i][1] == 10:
                carry_seq = g_baseseq//10
            elif lang[3-i][1] == 12:
                carry_seq = z_baseseq//12
            elif lang[3-i][1] == 60:
                carry_seq = w_baseseq//60
            elif lang[3-i][1] > 0 and lang[3-i][1]<60 \
            and isinstance(lang[3-i][1],int):
                carry_seq = w_baseseq//lang[3-i][1]
            else:
                carry_seq = w_baseseq*0
            octav_seq[:,3-i,0] = gan_seq.copy()
            octav_seq[:,3-i,1] = zhi_seq.copy()
        self.cur_seed = octav_seq[-1]
        self.last_seq = octav_seq[:-1].copy()
        return self.last_seq

    def resetSeq(self):
        self.cur_seed = self.oc_seed
        self.last_seq = None

    def setMethod(self,method=[[0,60],[0,60],[0,12],[1,10]]):
        self.gen_method = method

    def setLength(self,length):
        self.seq_length = length

#class Ocseq(object):
#    def __init__(self,ocword=Ocword(randomOcword()),leng=64,method=[[1,60],[1,60],[1,12],[1,10]]):
#        super(Ocseq,self).__init__()
#        self.oc_seed    = Ocword(ocword)
        #self.cur_seed = self.oc_seed
#        self.gen_method = method
#        self.seq_len    = leng
        #self.oc_seq   = None
#        self.oc_seq     = self.genSeq()
class Ocseq(np.ndarray):
    def __new__(cls,ocword=Ocword(randomOcword()),leng=64,method=[[0,60],[1,60],[1,12],[1,10]]):
#        obj = np.asarray(np.zeros(leng*8,dtype='int')).view(cls)
        obj = np.asarray(ocwordSeq(Ocword(ocword),leng,method)).view(cls)
        obj.oc_seed = Ocword(ocword)
        obj.gen_method = method
        obj.seq_len    = leng
        return obj

    def __array_finalize__(self,obj):
        if obj is None: return
        self.oc_seed = getattr(obj,'oc_seed',None)
        self.gen_method = getattr(obj,'gen_method',None)
        self.seq_len    = getattr(obj,'seq_len',None)

    def __array_wrap__(self,out_arr,context = None):
        return np.ndarray.__array_wrap__(self,out_arr,context)

    def __repr__(self):
        s = np.chararray(shape=len(self),unicode=True,itemsize=13)
        s = s + \
            tian_gan[self[:,0,0]] + di_zhi[self[  :,0,1]]+' '+\
            tian_gan[self[:,1,0]] + di_zhi[self[  :,1,1]]+' '+\
            tian_gan[self[:,2,0]] + di_zhi[self[  :,2,1]]+' '+\
            tian_gan[self[:,3,0]] + di_zhi[self[  :,3,1]]
        return '\n'.join(s) + '\n总数:' + str(len(s))

    def value(self):
        return np.array(self)

    def asans(self,head=0,tail=0):
        if tail==0: tail=self.seq_len
        s = np.chararray(shape=(tail-head,4),unicode=True,itemsize=2)
        tfunc = np.core.defchararray.asarray
        s=s+np.array([tfunc(tian_math[self[head:tail,0,0]])+\
                      tfunc(di_math[self[head:tail,0,1]]),
                      tfunc(tian_math[self[head:tail,1,0]])+\
                      tfunc(di_math[self[head:tail,1,1]]),
                      tfunc(tian_math[self[head:tail,2,0]])+\
                      tfunc(di_math[self[head:tail,2,1]]),
                      tfunc(tian_math[self[head:tail,3,0]])+\
                      tfunc(di_math[self[head:tail,3,1]])]).T
        return s

    def chinc(self,head=0,tail=0):
        if tail==0: tail=self.seq_len
        s = np.chararray(shape=(tail-head,4),unicode=True,itemsize=2)
        tfunc = np.core.defchararray.asarray
        s=s+np.array([tfunc(tian_gan[self[head:tail,0,0]])+\
                      tfunc(di_zhi[self[head:tail,0,1]]),
                      tfunc(tian_gan[self[head:tail,1,0]])+\
                      tfunc(di_zhi[self[head:tail,1,1]]),
                      tfunc(tian_gan[self[head:tail,2,0]])+\
                      tfunc(di_zhi[self[head:tail,2,1]]),
                      tfunc(tian_gan[self[head:tail,3,0]])+\
                      tfunc(di_zhi[self[head:tail,3,1]])]).T
        return s

#    def genSeq(self):
#        return  ocwordSeq(self.oc_seed,self.seq_len,self.gen_method)
        #return self.oc_seq

#    def resetSeq(self):
#        self.oc_seq = self.genSeq()

#    def setMethod(self,method=[[0,60],[0,60],[0,12],[1,10]]):
#        self.gen_method = method
#        self = np.asarray(ocwordSeq(self.oc_seed,self.seq_len,self.gen_method)).view(Ocseq)
        #self = ocwordSeq(self.oc_seed,self.seq_len,self.gen_method)
        #return self

#    def setLength(self,length):
#        self.seq_len = length
#        self = np.asarray(ocwordSeq(self.oc_seed,self.seq_len,self.gen_method)).view(Ocseq)
        #self = np.asarray(ocwordSeq(Ocword(ocword),leng,method)).view(self)
        #self = ocwordSeq(self.oc_seed,self.seq_len,self.gen_method)
        #return self

#    def setSeed(self,seed):
#        self.oc_seed = Ocword(seed)
#        self = np.asarray(ocwordSeq(self.oc_seed,self.seq_len,self.gen_method)).view(Ocseq)
        #self = np.asarray(ocwordSeq(Ocword(ocword),leng,method)).view(self)
        #self = ocwordSeq(self.oc_seed,self.seq_len,self.gen_method)
        #return self




def biasN(bias,balance,low_limit,up_limit):
    def func(x):
        if x < balance:
            return CircleAdd(x,bias,low_limit,up_limit)
        else: return CircleAdd(x,-bias,low_limit,up_limit)
    return np.frompyfunc(func,1,1)

def fractByGan(gan,zhi):
    return (0.5 + gan/10.0 + zhi/12.0)%1.0

frac_index_zhi = np.array([3/4,2/3,7/12,6/12,5/12,11/12,0,1/12,1/6,1/4,1/3,5/6])
frac_sindex_gan =np.array([-5/120,-1/30,-1/40,-1/60,-1/120,0,1/120,1/60,1/40,1/30])

def fractByZhi(gan,zhi):
    return (frac_index_zhi[zhi]+frac_sindex_gan[gan]+1)%1

def fractByWheel(gan,zhi):
    return year_queue[gan,zhi]/60.0

fr_policy = [fractByGan,fractByZhi,fractByWheel]
#ufunc_fractGan = np.frompyfunc(fractByGan,2,1)
#ufunc_fractZhi = np.frompyfunc(fractByZhi,2,1)
#ufunc_fractWheel = np.frompyfunc(fractByWheel,2,1)
def tolerGen(mod_type=2,mod=60,base=59,limit=0):
    def seed(gan,zhi):
        if mod_type == 0:
            a = (gan%mod)/base
            if limit == 0: return a
            else: return a%limit
        elif mod_type == 1:
            a = (zhi%mod)/base
            if limit == 0:
                return a
            else:
                return a%limit
        elif mod_type==2:
            a = (year_queue[gan,zhi]%mod)/base
            if limit == 0:
                return a
            else:
                return a%limit
        else:
            return 0
    return np.frompyfunc(seed,2,1)

class colorSeq(object):
    def __init__(self,ocseq=Ocseq(),fr_pol=[2,1,2],\
                 t1=[3,60,61,0],t2=[3,60,61,1/12],\
                 t3=[3,60,23,1/9],inscale=[1,1,1]):
        super(colorSeq,self).__init__()
        self.origin  = ocseq                     #.oc_seq
        self.fr_pol  = fr_pol                    #[2,1,2]
        self.to_mod1 = t1     #[3,60,61,0]
        self.to_mod2 = t2     #[3,60,61,1/12]
        self.to_mod3 = t3     #[3,60,23,1/9]
        self.inter_scaler  = inscale     #[1,1,1]

    def setFractPolicy(self,arg):
        self.fr_pol = arg

    def setTolerMode(self,arg):
        self.to_mod1 = arg[0]
        self.to_mod2 = arg[1]
        self.to_mod3 = arg[2]

    def setScaler(self,scaler):
        self.inter_scaler  = scaler

#    def getHJC(self):
#        a = self.origin
#        t1 = self.to_mod1
#        t2 = self.to_mod2
#        t3 = self.to_mod3
#
#        J_seq =(fr_policy[self.fr_pol[0]].__call__(a[:,1,0],a[:,1,1])+\
#                tolerGen(t1[0],t1[1],t1[2],t1[3]).__call__(a[:,0,0],a[:,0,1]))\
#            *self.inter_scaler[0]%1*100
#        H_seq = (fr_policy[self.fr_pol[1]].__call__(a[:,2,0],a[:,2,1])+\
#                tolerGen(t2[0],t2[1],t2[2],t2[3]).__call__(a[:,0,0],a[:,0,1]))\
#            *self.inter_scaler[1]%1*360
#        C_seq1= (fr_policy[self.fr_pol[2]].__call__(a[:,3,0],a[:,3,1])+\
#                tolerGen(t3[0],t3[1],t3[2],t3[3]).__call__(a[:,0,0],a[:,0,1]))\
#            *self.inter_scaler[2]%1*100
#        C_seq2= ufunc_maxChromeByJH(J_seq,H_seq)
#
#        C_seq = np.minimum(C_seq1,C_seq2)
#        return np.array([H_seq,J_seq,C_seq]).T.astype('float')

    def getJCH(self):
        a = self.origin
        t1 = self.to_mod1
        t2 = self.to_mod2
        t3 = self.to_mod3

        J_seq =(fr_policy[self.fr_pol[0]].__call__(a[:,1,0],a[:,1,1])+\
                tolerGen(t1[0],t1[1],t1[2],t1[3]).__call__(a[:,0,0],a[:,0,1]))\
            *self.inter_scaler[0]%1*100
        H_seq = (fr_policy[self.fr_pol[1]].__call__(a[:,2,0],a[:,2,1])+\
                tolerGen(t2[0],t2[1],t2[2],t2[3]).__call__(a[:,0,0],a[:,0,1]))\
            *self.inter_scaler[1]%1*360
        C_seq1= (fr_policy[self.fr_pol[2]].__call__(a[:,3,0],a[:,3,1])+\
                tolerGen(t3[0],t3[1],t3[2],t3[3]).__call__(a[:,0,0],a[:,0,1]))\
            *self.inter_scaler[2]%1*100
        C_seq2= ufunc_maxChromeByJH(J_seq,H_seq)

        C_seq = np.minimum(C_seq1,C_seq2)
        return np.array([J_seq,C_seq,H_seq]).T.astype('float')

    def getAreaJCH(self,jar=[[20,90]],har=[[0,20],[130,210],[340,359]],car=[[0,100]]):
        jar = np.array(jar)/100
        har = np.array(har)/360
        car = np.array(car)/100
        j_len_list =list(map(lambda x: (x[1]-x[0]),jar))
        h_len_list =list(map(lambda x: (x[1]-x[0]),har))
        c_len_list =list(map(lambda x: (x[1]-x[0]),car))
        j_len = reduce(lambda x,y: x+y,j_len_list)
        h_len = reduce(lambda x,y: x+y,h_len_list)
        c_len = reduce(lambda x,y: x+y,c_len_list)

        #print(j_len_list,h_len_list,c_len_list,j_len,h_len,c_len)
        def func(clen,clenli,clenar):
            def cvt(color):
                i = 0
                color = color * clen
                while(color>0):
                    color = color - clenli[i]
                    i += 1
                i -=1
                color = color + clenli[i]
                return color + clenar[i][0]
            return np.frompyfunc(cvt,1,1)

        cvt_j = func(j_len,j_len_list,jar)
        cvt_h = func(h_len,h_len_list,har)
        cvt_c = func(c_len,c_len_list,car)

        a = self.origin
        t1 = self.to_mod1
        t2 = self.to_mod2
        t3 = self.to_mod3

        J_seq =(fr_policy[self.fr_pol[0]].__call__(a[:,1,0],a[:,1,1])+\
                tolerGen(t1[0],t1[1],t1[2],t1[3]).__call__(a[:,0,0],a[:,0,1]))\
            *self.inter_scaler[0]%1
        H_seq = (fr_policy[self.fr_pol[1]].__call__(a[:,2,0],a[:,2,1])+\
                tolerGen(t2[0],t2[1],t2[2],t2[3]).__call__(a[:,0,0],a[:,0,1]))\
            *self.inter_scaler[1]%1
        C_seq= (fr_policy[self.fr_pol[2]].__call__(a[:,3,0],a[:,3,1])+\
                tolerGen(t3[0],t3[1],t3[2],t3[3]).__call__(a[:,0,0],a[:,0,1]))\
            *self.inter_scaler[2]%1
        J_ = cvt_j(J_seq)*100
        H_ = cvt_h(H_seq)*360
        C_1 = cvt_c(C_seq)*360
        C_2= ufunc_maxChromeByJH(J_,H_)

        C_ = np.minimum(C_1,C_2)
        #print(J_,H_,C_1,C_2)
        return np.array([J_,C_,H_]).T.astype('float')

    def getBiasJCH(self,J_bias,C_bias,H_bias):
        s = self.getJCH()
        J = s[:,0]
        C = s[:,1]
        H = s[:,2]
        bJ = biasN(J_bias,50,0,100)(J)
        bC = biasN(C_bias,50,0,100)(C)
        bH = biasN(H_bias,180,0,360)(H)
        return np.array([bJ,bC,bH]).T.astype('float')

    def getParallerJCH(self,J_bias,C_bias,H_bias):
        s = self.getJCH()
        J = s[:,0]
        C = s[:,1]
        H = s[:,2]
        bJ = nCircleAdd(J_bias,0,100)(J)
        bC = nCircleAdd(C_bias,0,100)(C)
        bH = nCircleAdd(H_bias,0,360)(H)
        return np.array([bJ,bC,bH]).T.astype('float')

    def getLimitParalJCH(self,J_bias,C_bias,H_bias):
        s = self.getJCH()
        J = s[:,0]
        C = s[:,1]
        H = s[:,2]
        bJ = nLimitAdd(J_bias,0,100)(J)
        bC = nLimitAdd(C_bias,0,100)(C)
        bH = nLimitAdd(H_bias,0,360)(H)
        return np.array([bJ,bC,bH]).T.astype('float')

    def getScaledJCH(self,center=[50,0,0],scale=10):
        #a = self.origin
        #t1 = self.to_mod1
        #t2 = self.to_mod2
        #t3 = self.to_mod3

#        J_seq =((fr_policy[self.fr_pol[0]].__call__(a[:,1,0],a[:,1,1])+\
#                tolerGen(t1[0],t1[1],t1[2],t1[3]).__call__(a[:,0,0],a[:,0,1]))\
#                *self.inter_scaler[0]%1 -0.5 )* scale
#        H_seq1 = ((fr_policy[self.fr_pol[1]].__call__(a[:,2,0],a[:,2,1])+\
#                tolerGen(t2[0],t2[1],t2[2],t2[3]).__call__(a[:,0,0],a[:,0,1]))\
#                 *self.inter_scaler[1]%1 )
#        C_seq1= (fr_policy[self.fr_pol[2]].__call__(a[:,3,0],a[:,3,1])+\
#                tolerGen(t3[0],t3[1],t3[2],t3[3]).__call__(a[:,0,0],a[:,0,1]))\
#                 *self.inter_scaler[2]%1
#        C_seq2= ufunc_maxChromeByJH(J_seq*100,H_seq1*360)
#
#        C_seq = ((np.minimum(C_seq1*100,C_seq2*100)/100)*scale).astype('float')
#        H_seq = (H_seq1 * np.pi*2).astype('float')
        s = self.getJCH()
        J_seq = s[:,0]
        C_seq = s[:,1]
        H_seq = s[:,2]/180*np.pi

        Z_seq = (J_seq.astype('float')-50)*scale/100
        X_seq = C_seq * np.cos(H_seq)*scale/100
        Y_seq = C_seq * np.sin(H_seq)*scale/100
        Z_center = center[0]
        X_center = center[1]*np.cos(center[2]/180*np.pi)
        Y_center = center[1]*np.sin(center[2]/180*np.pi)
        J = nLimitAdd(0,0,100)(Z_seq + Z_center)
        C = np.sqrt(np.square(Y_seq+Y_center)+np.square(X_seq+X_center))
        H = nCircleAdd(0,0,360)(np.arctan2(Y_seq+Y_center,X_seq+X_center)*180/np.pi)
        #C2= ufunc_maxChromeByJH(J,H)
        #C = np.minimum(C1,C2)
        #C2 =
        return np.array([J,C,H]).T.astype('float')

#def biasN(bias,balance,low_limit,up_limit):
mat_1_3_3 = np.array([[4,9,2],[3,5,7],[8,1,6]])-1
mat_1_4_4 = np.array([[16,3,2,13],[5,10,11,8],[9,6,7,12],[4,15,14,1]])-1
mat_2_4_4 = np.array([[7,12,1,14],[2,13,8,11],[16,3,10,5],[9,6,15,14]])-1
mat_3_4_4 = np.array([[4,14,7,9],[15,1,12,6],[10,8,13,3],[5,11,2,16]])-1
mat_4_4_4 = np.array([[2,16,13,3],[11,5,8,10],[7,9,12,6],[14,4,1,15]])-1
mat_5_4_4 = np.array([[4,9,15,16],[14,7,11,2],[15,6,10,3],[1,12,8,13]])-1
mat_1_5_5 = np.array([[17,24,1,8,15],\
                      [23,5,7,14,16],\
                      [4,6,13,20,22],\
                      [10,12,19,21,3],\
                      [11,18,25,2,9]])-1
mat_1_8_8 = np.array([[1,32,49,48,19,14,35,62],\
                      [56,41,8,25,38,59,22,11],\
                      [13,20,61,36,31,2,47,50],\
                      [60,37,12,21,42,55,26,7],\
                      [6,27,54,43,24,9,40,57],\
                      [51,46,3,30,33,64,17,16],\
                      [10,23,58,39,28,5,44,53],\
                      [63,34,15,18,45,52,29,4]])-1
mat_2_8_8 = np.array([[52,61,4,13,20,29,36,45],\
                      [14,3,62,51,46,35,30,19],\
                      [53,60,5,12,21,28,37,44],\
                      [11,6,59,54,43,38,27,22],\
                      [55,58,7,10,23,25,39,42],\
                      [9,8,57,56,41,40,25,24],\
                      [50,63,2,15,18,31,34,47],\
                      [16,1,64,49,48,33,32,17]])-1

def getFixedQueue(leng=8,ver=1):
    if ver == 1:
        if   leng == 3: return mat_1_3_3
        elif leng == 4: return mat_1_4_4
        elif leng == 5: return mat_1_5_5
        elif leng == 8: return mat_1_8_8
        else: return mat_1_8_8
    elif ver == 2 and leng == 4: return mat_2_4_4
    elif ver == 2 and leng == 8: return mat_2_8_8
    elif ver == 3 and leng == 4: return mat_3_4_4
    elif ver == 4 and leng == 4: return mat_4_4_4
    elif ver == 5 and leng == 4: return mat_5_4_4
    else: return mat_1_8_8

class posMat(np.ndarray):
    def __new__(cls,input_array):
        obj = np.asarray(input_array,dtype='int').view(cls)
        return obj

    def noalter(self):
        return self

    def mirrorX(self):
        return self[:,::-1,:]

    def mirrorY(self):
        return self[::-1,:,:]

    def mirrorXY(self):
        return self[::-1,::-1,:]

    def rot90(self):
        return self.transpose(1,0,2)[::-1,:,:]

    def asflip(self):
        return self.transpose(1,0,2)

    def osflip(self):
        return self.transpose(1,0,2)[::-1,::-1,:]

    def rot270(self):
        return self.transpose(1,0,2)[:,::-1,:]

    def alter(self,number):
        a = [self.noalter, self.mirrorX,  self.mirrorY,  self.mirrorXY, \
             self.rot90,   self.asflip,   self.osflip,   self.rot270]
        return a[number]



#    def __new__(cls,input_array=randomOcword()):
#        obj = np.asarray(input_array,dtype='int').reshape(4,2).view(cls)
#        return obj

class placeSeq(object):
    def __init__(self,ocseq=Ocseq()):
        super(placeSeq,self).__init__()
        self.origin = ocseq
        self.length = ocseq.seq_len

    def getMat(self,leng=8,ver=1):
        queue = getFixedQueue(leng,ver)
        q1 = (queue//leng).flatten()
        q2 = (queue%leng).flatten()
        m = posMat(np.array([q1,q2]).T.reshape(leng,leng,2))
        return m

    def genQueue(self,uleng=8,ver=1,mat=(4,2),interv=0,typet=0):
        m = self.getMat(uleng,ver)
        mm = np.zeros((m.shape[0]*mat[0])*(m.shape[1]*mat[1])*2).reshape(-1,2).astype('float')
        le = uleng**2
        if typet == 0 or True:
            for i in range(mat[0]*mat[1]):
                mm[i*le:(i+1)*le,:]=(m+[(i%mat[0])*(uleng+interv),\
                                        (i//mat[0])*(uleng+interv)]).reshape(-1,2)
        return mm
