# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 15:01:34 2021

@author: ddc
"""

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


X = data[['jg3','gb','g5','hz']]
y = data['xl3']
X_train, X_test, y_train, y_test = \
 train_test_split( X, y, test_size=0.33, random_state=42)
from sklearn import tree
clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train,y_train)
score = clf.score(X_test,y_test)




 
X = data[['jg3','gb','g5','hz']]
y = data['xl3']
X_train, X_test, y_train, y_test = \
 train_test_split( X, y, test_size=0.33, random_state=42)
from sklearn.naive_bayes import GaussianNB
gnb = GaussianNB()
gnb = gnb.fit(X_train,y_train)
score = gnb.score(X_test,y_test)





















