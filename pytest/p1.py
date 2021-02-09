import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import jieba 
import re
import sklearn
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from numpy import array
from numpy import argmax
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from wordcloud import WordCloud
from sklearn.tree import ExtraTreeClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score
from sklearn import preprocessing


from matplotlib.font_manager import FontProperties
myfont=FontProperties(fname=r'C:\Windows\Fonts\simhei.ttf',size=14)
sns.set(font=myfont.get_name())

text = open(r'C:/git/a/b/p3-1.txt', encoding='utf-8').read()


df_1=pd.read_csv(r'C:/git/a/b/p3-1.csv',error_bad_lines=False,\
                 header=None,names=['销量','价格','厂家','d','e','f','g'])


del df_1['d']
df_1['内容'] = df_1['e']
del df_1['e']
xl = df_1['销量']
def reduce_xl(x):
    x = re.sub(' 去看二手',' ',x)
    x = re.match(r'(.*)(\d)(.*)(\+)',x)
    if x: 
        x = re.sub(' ','',x.group(0))
        if(re.match(r'.*万',x[:-1])):
            x=re.match(r'.*万',x[:-1]).group(0)[:-1]
            x = float(x)*10000
        else:
            x = float(x[:-1])
        return x
    else:
        return 0
xl = xl.apply(lambda x:  reduce_xl(x))

jg = df_1['价格']
def reduce_jg(x):
    if (x!=0):
        x = re.sub(' ￥','',x)
        x = re.sub('.00','',x)
    else:
        x = 0
    return float(x)
jg = jg.apply(lambda x:  reduce_jg(x))

cj = df_1['厂家']
def reduce_cj(x):
    x=jieba.lcut(x[1:])
    if x:
        return x[0]
    else:
        return ' '
cj = cj.apply(lambda x:  reduce_cj(x))

nr = df_1['内容']
def reduce_nr(x):
    x = re.sub(r' +',' ',x)
    x = re.sub(r'【.+】','',x)
    x = re.split(r' ',x[1:])
    gb = w = mah = hz = g5 = ''
    for i in x:
        G5 = re.search(r'5G',i)
        if G5:
            if g5 == '':
                g5 = i
        Hz = re.search(r'Hz',i)
        if Hz:
            hz = i
        mAh = re.search(r'mAh',i)
        if mAh :
            mah = i
        W = re.search(r'\d+W',i)
        if W :
            w = i
        GB = re.search(r'\d+GB',i)
        if GB :
            gb = i
    return [g5,hz,mah,w,gb]
nr_1 = nr.apply(lambda x:  reduce_nr(x))

df_2 = nr_1.to_frame()
df_2['g5'] = df_2['内容'].apply(lambda x: x[0]) 
df_2['hz'] = df_2['内容'].apply(lambda x: x[1]) 
df_2['mah'] = df_2['内容'].apply(lambda x: x[2]) 
df_2['w'] = df_2['内容'].apply(lambda x: x[3]) 
df_2['gb'] = df_2['内容'].apply(lambda x: x[4]) 

def reduce_df_21(x):
    if x == '':
        x = 0
    else:
        x = 1
    return x
s_g5 = df_2['g5'].apply(lambda x: reduce_df_21(x))
def reduce_df_22(x):
    x = re.search(r'(\d+)Hz',x)
    if x:
        x = float(x.group(0)[:-2])
    else:
        x = 0
    return x
s_hz = df_2['hz'].apply(lambda x: reduce_df_22(x))
def reduce_df_23(x):
    x = re.search(r'(\d+)mAh',x)
    if x:
        x = float(x.group(0)[:-3])
    else:
        x = 0
    return x
s_mah = df_2['mah'].apply(lambda x: reduce_df_23(x))
def reduce_df_24(x):
    x = re.search(r'(\d+)W',x)
    if x:
        x = float(x.group(0)[:-1])
    else:
        x = 0
    return x
s_w = df_2['w'].apply(lambda x: reduce_df_24(x))
def reduce_df_25(x):
    x = re.search(r'(\d+)',x)
    if x:
        x = float(x.group(0))
        if x>32:
            x = 0
    else:
        x = 0
    return x
s_gb = df_2['gb'].apply(lambda x: reduce_df_25(x))
data = pd.DataFrame({'gb':s_gb,'g5':s_g5,'hz':s_hz,'mah':s_mah,\
              'w':s_w,'jg':jg,'cj':cj,'xl':xl})



def reduce_f(x):
    x = re.sub(r'： ?',':',x)
    x = re.split(r' ',x)[1:]
    shop = name = pid = weight = made = cpu = nc = cc = cck = sxt = hxs = qxs = pmcc = fbl = pmbl = pmqszh = cdq = os = ''
    for i in x:
        Shop = re.search(r'品牌:(.*)',i)
        if Shop:
                shop = Shop.group(1)
        Name = re.search(r'商品名称:(.*)',i)
        if Name:
            name = Name.group(1)
        Pid = re.search(r'商品编号:(.*)',i)
        if Pid :
            pid = Pid.group(1)
        Weight = re.search(r'商品毛重:(.*)',i)
        if Weight :
            weight = Weight.group(1)
        Made = re.search(r'商品产地:(.*)',i)
        if Made :
            made = Made.group(1)
        Cpu = re.search(r'CPU型号:(.*)',i)
        if Cpu :
            cpu = Cpu.group(1)
        Nc = re.search(r'运行内存:(.*)',i)
        if Nc :
            nc = Nc.group(1)
        Cc = re.search(r'机身存储:(.*)',i)
        if Cc :
            cc = Cc.group(1)
        Cck = re.search(r'存储卡:(.*)',i)
        if Cck :
            cck = Cck.group(1)
        Sxt = re.search(r'摄像头数量:(.*)',i)
        if Sxt :
            sxt = Sxt.group(1)
        Hxs = re.search(r'后摄主摄像素:(.*)',i)
        if Hxs :
            hxs = Hxs.group(1)
        Qxs = re.search(r'前摄主摄像素:(.*)',i)
        if Qxs :
            qxs = Qxs.group(1)
        Pmcc = re.search(r'主屏幕尺寸（英寸）:(.*)',i)
        if Pmcc :
            pmcc = Pmcc.group(1)
        Fbl = re.search(r'分辨率:(.*)',i)
        if Fbl :
            fbl = Fbl.group(1)
        Pmbl = re.search(r'屏幕比例:(.*)',i)
        if Pmbl :
            pmbl = Pmbl.group(1)
        Pmqszh = re.search(r'屏幕前摄组合:(.*)',i)
        if Pmqszh :
            pmqszh = Pmqszh.group(1)
        Cdq = re.search(r'充电器:(.*)',i)
        if Cdq :
            cdq = Cdq.group(1)
        Os = re.search(r'操作系统:(.*)',i)
        if Os :
            os = Os.group(1)
    return [shop,name,pid,weight,made,cpu,nc,cc,cck,sxt,\
            hxs,qxs,pmcc,fbl,pmbl,pmqszh,cdq,os]
s_f = df_1['f'].apply(lambda x: reduce_f(x))
n = -1
df_3 = s_f.to_frame()
testList = ['shop','name','pid','weight','made','cpu','nc','cc','cck','sxt',\
              'hxs','qxs','pmcc','fbl','pmbl','pmqszh','cdq','os']
for i,x in enumerate(testList):
                  df_3[x] = s_f.apply(lambda x: x[i])


shop = df_3[df_3.columns[5]].value_counts()

def reduce_weight(x):
    x = re.search(r'\d+.?\d+',x)
    x = x.group(0)
    x = float(x)
    if x<=10:
        x = x*1000
    return x
df_3['weight1'] = df_3['weight'].apply(lambda x: reduce_weight(x))

def reduce_nc(x):
    x = re.search(r'\d+',x)
    if x:
        x = x.group(0)
        x = float(x)
    else:
        x = 0
    return(x)
df_3['nc1'] = df_3['nc'].apply(lambda x: reduce_nc(x))

def reduce_cc(x):
    x = re.search(r'\d+',x)
    if x:
        x = x.group(0)
        x = float(x)
    else:
        x = 0
    return(x)
df_3['cc1'] = df_3['cc'].apply(lambda x: reduce_cc(x))

def reduce_cck(x):
    if x == '支持MicroSD(TF)':
        x = 'MicroSD(TF)'
    if x == '其它存储卡':
        x = '其它存储卡'
    if x == 'NM存储卡':
        x = 'NM存储卡'
    if x == '不支持存储卡':
        x = '不支持存储卡'
    if x == '':
        x = '不支持存储卡'
    return(x)
df_3['cck1'] = df_3['cck'].apply(lambda x: reduce_cck(x))
def reduce_sxt(x):
    if x == '后置五摄':
        x = 5
    if x == '后置四摄':
        x = 4
    if x == '后置三摄':
        x = 3
    if x == '后置单摄':
        x = 1
    if x == '后置双摄':
        x = 2
    if x == '其他':
        x = 0
    if x == '':
        x = 0
    return float(x)
df_3['sxt1'] = df_3['sxt'].apply(lambda x: reduce_sxt(x))

def reduce_xs(x):
    x = re.search(r'\d+',x)
    if x:
        x = float(x.group(0))
        if x<=1:
            x = x*10000
    else:
        x = 0
    return x
df_3['hxs1'] = df_3['hxs'].apply(lambda x: reduce_xs(x))
df_3['qxs1'] = df_3['qxs'].apply(lambda x: reduce_xs(x))

def reduce_pmcc(x):
    x = re.search(r'\d+.?\d+',x)
    if x:
        x = float(x.group(0))
    else:
        x = 0
    return x
df_3['pmcc1'] = df_3['pmcc'].apply(lambda x: reduce_pmcc(x))
jg_1 = pd.qcut(data['jg'], q=3, labels=['low', 'medium', 'high'])
xl_1 = pd.qcut(data['xl'], q=3, labels=['low', 'medium', 'high'])












