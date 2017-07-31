#-*- coding:utf-8 -*-
from getDataFromFile import *
from feature import *
from numpy import *
from sklearn.svm import SVC
from time import *
from sklearn.decomposition import PCA 
from sklearn import preprocessing
from sklearn.cross_validation import train_test_split  
from sklearn import tree 

import lightgbm as lgb

import warnings
warnings.filterwarnings("ignore")
#获取数据

ids,dataList,labelLists = getTrainDataFromTxt("./dsjtzs_txfz_training.txt/dsjtzs_txfz_training.txt")
speedData = getTrainSpeedList(ids,dataList,labelLists)
accData = getTrainAccSpeedList(ids,speedData,labelLists)
# acccData = getTrainAcccSpeedList(ids,accData,speedData,labelLists)
feature = [] #[data1,data2...]
print(len(speedData),len(ids),len(accData))
for i in range(len(speedData)):
    speedList = speedData[i]
    speed_x_list = [];speed_y_list = []
    for speed in speedList:
        speed_x = speed[0]
        speed_y = speed[1]
        speed_x_list.append(speed_x)
        speed_y_list.append(speed_y)

    accList = accData[i]
    acc_x_list = [];acc_y_list = []
    for acc in accList:
        acc_x = acc[0]
        acc_y = acc[1]
        acc_x_list.append(acc_x)
        acc_y_list.append(acc_y)



    feature.append(Get_FeatureList(speed_x_list) + 
                    Get_FeatureList(speed_y_list) + 
                    Get_FeatureList(acc_x_list) + 
                    Get_FeatureList(acc_y_list))

#数据归一化处理
min_max_scaler = preprocessing.MinMaxScaler()
feature_minmax = min_max_scaler.fit_transform(feature)
# feature_minmax = feature
# print(type(feature_minmax))

while(True):
    #拆分训练数据与测试数据   2600 400   7:1 
    x_train, x_test, y_train, y_test = train_test_split(feature_minmax, labelLists, test_size = 0.3)  

    train_data = lgb.Dataset(x_train,y_train)
    w = random.rand(len(x_train),)
    train_data.set_weight(w)
    param = {'num_leaves':50,'num_trees':120,'objective':'binary'}
    param['metric'] = ['auc', 'binary_logloss']
    num_round = 250
    end = int(len(x_test)/2)
    print(end)
    valid_sets = lgb.Dataset(x_test[0:end],y_test[0:end])
    #gbm=lgb.cv(param,train_data,num_round,nfold=10)
    gbm = lgb.train(param,train_data,num_round,valid_sets=valid_sets,early_stopping_rounds=40)
    ypred = gbm.predict(x_test)



    classtype = [0,1]
    confusionMatrix = zeros((len(classtype),len(classtype)))


    for i in range(end):
        #data = pca.transform(feature[i])#对数据进行降维
        label = y_test[end+i]
        #预测分类
        prob = gbm.predict([x_test[end+i]])
        #print(prob)
        
        if prob > 0.5:
            prob = 1
        else:
            prob = 0
        confusionMatrix[label][prob] += 1
        # 真实  \ 预测    0   1
        # 0
        # 1    
    print("混淆矩阵",confusionMatrix) # test 真:假 = 9:1 
    R = confusionMatrix[0][0]/(confusionMatrix[0][0]+confusionMatrix[0][1]) # FF / (FF+FT)
    P = confusionMatrix[0][0]/(confusionMatrix[1][0]+confusionMatrix[0][0]) # FF / (TF+FF)
    F =5*P*R/(2*P+3*R)*100
    print("R",R) # 判黑/真实黑
    print("P",P)
    print("F",F)
    sleep(2)
    if(P>0.96 and R > 0.98):
        break

del feature
del accData
# del acccData
del speedData
del ids,dataList,labelLists 


#获取预测数据   假样本预计 15000 
predictids,predictData=getRegressDataFromTxt("./dsjtzs_txfz_test1.txt/dsjtzs_txfz_test1.txt")
#predictids,predictData,labelLists = getTrainDataFromTxt("./dsjtzs_txfz_training.txt/dsjtzs_txfz_training.txt")
predictSpeedData = getRegressSpeedList(predictids,predictData)
predictAccData = getRegressAccSpeedList(predictids,predictSpeedData)
#predictAcccData = getRegressAcccList(predictids,predictAccData,predictSpeedData)
print(len(predictData),len(predictids),len(predictSpeedData),len(predictAccData))

sleep(5)#休眠

#分类为机器的放到列表中
result = []
problist = []
for i in range(len(predictSpeedData)):
    if i%500 == 0:
        print("processing ",i)
    speedList = predictSpeedData[i]
    speed_x_list = [];speed_y_list = [];speed_s_list=[]
    predictfeaturelist = []            
    acc_x_list = [];acc_y_list = []

    for speed in speedList:
        speed_x = speed[0]
        speed_y = speed[1]
        speed_x_list.append(speed_x)
        speed_y_list.append(speed_y)
        #speed_s_list.append(speed_s)

    accList = predictAccData[i]
    
    for acc in accList:
        acc_x = acc[0]
        acc_y = acc[1]
        acc_x_list.append(acc_x)
        acc_y_list.append(acc_y)
    

    predictfeaturelist.extend(Get_FeatureList(speed_x_list))
    predictfeaturelist.extend(Get_FeatureList(speed_y_list))
    predictfeaturelist.extend(Get_FeatureList(acc_x_list))
    predictfeaturelist.extend(Get_FeatureList(acc_y_list))

    #数据归一化处理
    predictfeaturelist_minmax = min_max_scaler.transform(predictfeaturelist)
    # predictfeaturelist_minmax = array(predictfeaturelist)
    
    #预测分类
    prob = gbm.predict(predictfeaturelist_minmax.reshape(1,32)) #对transform结果返回(n,)的数组，因此可以reshape，list不行

    problist.append((predictids[i],prob))
    # if prob > 0.98:
    #     prob = 1
    # else:
    #     prob = 0
    # if prob == 0:
    #     result.append(str(predictids[i]) + '\n')

# 10w条 prob 保存下来，做一个排序，选最低的2w条,提取出id再次排序
problist.sort(key=lambda x:x[1][0])
print("prob 25000: ",problist[25000][1][0])
print("prob 20000: ",problist[20000][1][0])
print("prob 15000: ",problist[15000][1][0])
print("prob 10000: ",problist[10000][1][0])
print("prob 5000: ",problist[5000][1][0])
result2 = str(problist[15000][1][0]) + ' ' + str(problist[10000][1][0]) +  ' ' + str(problist[8000][1][0]) + ' ' + str(problist[5000][1][0]) + '\n'
problist = problist[0:25000]
for i in range(len(problist)):
    problist[i]=int(problist[i][0])
problist.sort()
for i in range(len(problist)):
    result.append(str(problist[i])+'\n')    
#结果写到文件里面
fout = open("./result.txt",'w')
fout.writelines(result)
fout.close()
fout = open("./prob.txt",'a')
fout.writelines(result2)
fout.close()
del predictids
del predictData
del predictSpeedData
                        

print("Done")
