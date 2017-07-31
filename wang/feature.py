#-*- coding:utf-8 -*-
'''
feature.py
'''

import scipy.stats
#最大数
def Get_Max(list):
    return max(list)
#最小数
def Get_Min(list):
    return min(list)

#众数(返回多个众数的平均值)
def Get_Most(list):
    most=[]
    item_num = dict((item, list.count(item)) for item in list)
    for k,v in item_num.items():
        if v == max(item_num.values()):
           most.append(k)
    return sum(most)/len(most)


#获取平均数
def Get_Average(list):
	sum = 0
	for item in list:
		sum += item
	return sum/len(list)


#获取方差
def Get_Variance(list):
	sum = 0
	average = Get_Average(list)
	for item in list:
		sum += (item - average)**2
	return sum/len(list)

#获取n阶原点距
def Get_NMoment(list,n):
    sum=0
    for item in list:
        sum += item**n
    return sum/len(list)

#峰度
def Get_kurtosis(list):
    return scipy.stats.kurtosis(list)

#偏度
def Get_skew(list):
    return scipy.stats.skew(list)


#返回特征列表 1x9
def Get_FeatureList(list):
    #return [Get_Min(list),Get_Max(list),Get_Most(list),Get_Average(list),Get_Variance(list),Get_NMoment(list,1),Get_NMoment(list,2), Get_kurtosis(list),Get_skew(list)]
    return [Get_Min(list),Get_Max(list),Get_Average(list),Get_Variance(list),Get_NMoment(list,2), Get_kurtosis(list),Get_skew(list),Get_Most(list)]

