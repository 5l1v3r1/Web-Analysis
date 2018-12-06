# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 10:24:55 2018

@author: eweixux
输入：第一行为标题，接下来每一行均为一个样本即一个url抽取的得到的向量
输出：模型的预测结果
"""


import numpy as np
import pandas as pd
import urllib
import pickle
import sklearn
from sklearn.svm import SVC
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.grid_search import GridSearchCV  
from sklearn.naive_bayes import MultinomialNB 
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.externals import joblib


import itertools
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
class_names = np.array(['0','1'])

def draw_matrix(predicted,y_test,name):
    cnf_matrix =confusion_matrix(y_test,predicted) 
# Compute confusion matrix
#cnf_matrix = confusion_matrix(y_test, y_pred)
    np.set_printoptions(precision=2)

# Plot non-normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names,
                      title=name+'Confusion matrix')

# Plot normalized confusion matrix
    plt.figure()
    plot_confusion_matrix(cnf_matrix, classes=class_names, normalize=True,
                      title=name+ 'confusion matrix')

    plt.show()
   
    
def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion matrix, without normalization')

    print(cm)

    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()


def read_data2_feature_matrix(train_data='train_1115.xlsx', test_data='test_1115.xlsx'):
    '''
    加载数据的功能
    输入：训练数据和测试数据的路径
    输出：四个矩阵，分别为：训练数据的特征数据矩阵、标签矩阵、测试数据的特征数据矩阵、标签矩阵
    '''
    #加载数据得到训练数据的特征矩阵
    dataset = pd.read_excel(train_data,header = None)
    dataset.dropna(inplace=True)
    print(dataset)
    X_train = dataset[[0,1,2,3,4,5,6,7,8,9,10,11,12]]
    y_train = dataset[13]
    print('训练样本数是------>'+str(len(y_train)))

    #加载数据得到测试笔数据的特征矩阵
    dataset = pd.read_excel(test_data,header = None)
    dataset.dropna(inplace=True)
    X_test = dataset[[0,1,2,3,4,5,6,7,8,9,10,11,12]]
    y_test = dataset[13]
    print('测试样本数是------>'+ str(len(y_test)))
    return X_train, y_train, X_test, y_test

#
def SVM_model_test(X_train, y_train, X_test, y_test, model_file='svm.m'):
    '''
    使用SVM训练模型和测试,并且使用joblib持久化保存了得到的svm_model，读出保存的模型用于检测，其余模型均可以这样做
    '''
    print('**************************************************SVM（支持向量机）**********************************')
    model = SVC()
    model.fit(X_train, y_train)
    print ('SVM模型为：')
    print(model)
#    with open(model_file, 'w') as f:
    joblib.dump(model, 'svm.m')
#    svm_model_file=file('model/svm.pkl')
    svm_model=joblib.load('svm.m')
    expected = y_test
    predicted = svm_model.predict(X_test)
    draw_matrix(predicted,y_test,name='SVM ')
    
#    predicted = model.predict(X_test)
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    print(np.linalg.matrix_rank)



def SVMCV_model_test(X_train, y_train, X_test, y_test):
    '''
    使用SVMCV模型训练和测试模型，这里使用的是径向基核函数
    '''
    print('********************************SVMCV**************************************')
    model = SVC(kernel='rbf', probability=True)  
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}  
    grid_search = GridSearchCV(model, param_grid, n_jobs = 1, verbose=1)  
    grid_search.fit(X_train, y_train)  
    print('SVMCV模型参数信息为：')
    best_parameters = grid_search.best_estimator_.get_params()  
    for para, val in best_parameters.items():  
        print(para, val)  
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)  
    model.fit(X_train, y_train)
    print('SVMCV模型为：')  
    print(model)  
    print('--------------------------SVMCV 测试准确度为-------------------------------------------')
    expected = y_test
    predicted = model.predict(X_test)
    draw_matrix(predicted,y_test,name='SVMCV ')
    print(predicted)
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
#
#
#
def GBDT_model_test(X_train, y_train, X_test, y_test):
    '''
    使用GBDT训练和测试模型
    '''
    print('**********************************GBDT**************************************') 
    model = GradientBoostingClassifier(n_estimators=200)  
    model.fit(X_train, y_train)
    print('GBDT模型为：')
    print(model)
    print('--------------------------GBDT  测试准确度为-------------------------------------------')
    expected = y_test
    predicted = model.predict(X_test)
    draw_matrix(predicted,y_test,name='GBDT ')
    print(predicted)
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted)) 



def RF_model_test(X_train, y_train, X_test, y_test):
    '''
    使用RF来训练和测试模型
    '''
    print ('**********************************RF**************************************' )  
    model = RandomForestClassifier(n_estimators=8)  
    model.fit(X_train, y_train)
    print ('RF模型为：')
    print(model)
    print ('--------------------------RF测试准确度为-------------------------------------------')
    expected = y_test
    predicted = model.predict(X_test)
    draw_matrix(predicted,y_test,name='RF ')
    print(predicted)
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))   

#
#
def NB_model_test(X_train, y_train, X_test, y_test):
    '''
    使用NB来训练和测试模型
    '''
    print ('*********************************************朴素贝叶斯***************************************************')
    model = GaussianNB()
    model.fit(X_train, y_train)
    print ('NB模型为：')
    print(model)
    print ('------------------------------------------朴素贝叶斯测试准确度为-------------------------------------------')
    expected = y_test
    predicted = model.predict(X_test)
    draw_matrix(predicted,y_test,name='Naive Bayes ')
    print(predicted)
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))

#
#def MultinomialNB_model_test(X_train, y_train, X_test, y_test):
#    '''
#    使用MultinomialNB训练和测试模型
#    '''
#    print ('**********************************MultinomialNB**************************************')    
#    model = MultinomialNB(alpha=0.01)  
#    model.fit(X_train, y_train)  
#    print ('MultinomialNB模型为：')
#    print(model)  
#    print ('--------------------------MultinomialNB   测试准确度为-------------------------------------------')
#    expected = y_test
#    predicted = model.predict(X_test)
#    print(metrics.classification_report(expected, predicted))
#    print(metrics.confusion_matrix(expected, predicted))   
#      
#

def KNN_model_test(X_train, y_train, X_test, y_test):
    '''
    使用KNN训练和测试模型
    '''
    print ('**********************************KNN**************************************')   
    model = KNeighborsClassifier()  
    model.fit(X_train, y_train) 
    print ('KNN模型为：')
    print (model)  
    print ('--------------------------KNN   测试准确度为-------------------------------------------')
    expected = y_test
    predicted = model.predict(X_test)
    draw_matrix(predicted,y_test,name='KNN ')
    print(predicted)
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted)) 

      

def CART_model_test(X_train, y_train, X_test, y_test):
    '''
    使用CART训练和测试模型
    '''
    print ('*****************************************决策树,分类和回归树（CART）******************************')
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    print ('CART模型为：')
    print(model)
    print ('-------------------------------------------决策树,分类和回归树（CART）----------------------------------')
    expected = y_test
    predicted = model.predict(X_test)
    draw_matrix(predicted,y_test,name='Decision Tree ')
    print(predicted)
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    print ('********************************特征重要性为***************************************')
    print(model.feature_importances_)


def LR_model_test(X_train, y_train, X_test, y_test):
    '''
    使用LR训练和测试模型
    '''
    print ('*************************************逻辑回归*********************************')
    model = LogisticRegression()  # 参数可以设置
    model.fit(X_train, y_train)
    print ('LR模型为：')
    print(model)
    joblib.dump(model, 'LR_model.m')
    expected = y_test
    predicted = model.predict(X_test)
    draw_matrix(predicted,y_test,name = 'LR ')
    print(predicted)
    print(metrics.classification_report(expected, predicted))
    print(metrics.confusion_matrix(expected, predicted))
    print('-------------------------------------------逻辑回归测试精度为----------------------------------')
    print (model.get_params([3]))
    print (model.coef_)
    print (model.intercept_)
#

if __name__=='__main__':
    X_train, y_train, X_test, y_test=read_data2_feature_matrix(train_data='train_1115.xlsx', test_data='test_1115.xlsx')

    SVM_model_test(X_train, y_train, X_test, y_test, model_file='svm.m')
    SVMCV_model_test(X_train, y_train, X_test, y_test)
    GBDT_model_test(X_train, y_train, X_test, y_test)
    RF_model_test(X_train, y_train, X_test, y_test)
    NB_model_test(X_train, y_train, X_test, y_test)
#    MultinomialNB_model_test(X_train, y_train, X_test, y_test)
    KNN_model_test(X_train, y_train, X_test, y_test)
    CART_model_test(X_train, y_train, X_test, y_test)
    LR_model_test(X_train, y_train, X_test, y_test)
