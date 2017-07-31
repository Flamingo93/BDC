#-*- coding:utf-8 -*-
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
import math


def drawScatter():

    fr = open("E:\\bisai\\bigdata\\dsjtzs_txfz_training.txt\\dsjtzs_txfz_training.txt",'r')
    count = 1
    arrayOfLines = fr.readlines()
    for arrayOfLine in arrayOfLines:
        #空格，分号，逗号
        xyt_list = arrayOfLine.split()[1].split(";")
        classlabel = arrayOfLine.split()[3]
        nums = len(xyt_list)-1
        mat = zeros((nums,3))
        index = 0
        for xyt in xyt_list[:-1]:
            mat[index, :] = xyt.split(",")
            index += 1
        
        fig = plt.figure()
        ax=fig.add_subplot(111)
        plt.plot(mat[:, 0], mat[:, 1], "b--", linewidth=1)
        plt.xlabel("X")  # X轴标签
        plt.ylabel("Y")  # Y轴标签
        plt.title("Line plot")  # 图标题
        plt.show()
        plt.savefig(".\\scatter\\"+str(count)+"_"+str(classlabel)+".png")
        plt.close() # 一定要关掉图片,不然python打开图片20个后会崩溃
        count+=1

        
        
def getTrainDataFromTxt(src):

    fr = open(src,'r') #src=".\\dsjtzs_txfz_training.txt\\dsjtzs_txfz_training.txt"
    arrayOfLines = fr.readlines()
    ids = [];#存放数据序号
    dataList = []; #存放数据
    labelList = [];#存放标签
    
    for arrayOfLine in arrayOfLines:
        #空格，分号
        id = arrayOfLine.split()[0]
        targetPoint = arrayOfLine.split()[2] # 目标点 '1420.5,202'
        xyt_list = arrayOfLine.split()[1].split(";") # 轨迹点 ['x0,y0,t0','x1,y1,t1',...]
        classlabel = arrayOfLine.split()[3] #c1
        
        #数据预处理
        #减去目标点的到相对位置点
        data = []
        for xyt in xyt_list[:-1]:#xyt_list最后一个为'',因此去掉
            #逗号
            x = float(xyt.split(",")[0]) - float(targetPoint.split(",")[0]) #x坐标
            y = float(xyt.split(",")[1]) - float(targetPoint.split(",")[1]) #y坐标
            t = float(xyt.split(",")[2]) # t坐标
            data.append([x,y,t])
        
        ids.append(id)
        dataList.append(data) #data=[[x0,y0,t0],[x1,y1,t1]...]] dataList = [data1,data2...]
        labelList.append(int(classlabel)) #[c1,c2...]
    return ids,dataList,labelList
    
#获取训练的速度数据
def getTrainSpeedList(ids,dataList,labelList): # dataList = [data1,data2...]
    speedData=[]
    delete = []#
    for k in range(len(dataList)):
        data=dataList[k]# data=[[x0,y0,t0],[x1,y1,t1]...]]
        speedList=[]
        for i in range(len(data) - 1):
            xinc = data[i+1][0] - data[i][0]
            yinc = data[i+1][1] - data[i][1]
            tinc = data[i+1][2] - data[i][2]
            if tinc <= 0:
                continue
            speed_x = abs(xinc/tinc) #x方向的速度 speed_x = 40
            speed_y = abs(yinc/tinc) #y方向的速度 speed_y = 30
            speed_t = data[i+1][2]
            speedList.append([speed_x,speed_y,speed_t]) #speedList=[[40,30,50],...]
        # if len(speedList)>=5:
        #     speedList[0][0] = (speedList[0][0] + speedList[1][0] + speedList[2][0]) / 3
        #     speedList[1][0] = (speedList[0][0] + speedList[1][0] + speedList[2][0] + speedList[3][0]) / 4
        #     speedList[-1][0] = (speedList[-1][0] + speedList[-2][0] + speedList[-3][0]) / 3
        #     speedList[-2][0] = (speedList[-1][0] + speedList[-2][0] + speedList[-3][0] + speedList[-4][0]) / 4
        #     for dot_num in range(2, len(speedList) - 2):
        #         speedList[dot_num][0] = (speedList[dot_num - 2][0] + speedList[dot_num - 1][0] + speedList[dot_num][0] + speedList[dot_num + 1][0] + speedList[dot_num + 2][0]) / 5
            
        #     speedList[0][1] = (speedList[0][1] + speedList[1][1] + speedList[2][1]) / 3
        #     speedList[1][1] = (speedList[0][1] + speedList[1][1] + speedList[2][1] + speedList[3][1]) / 4
        #     speedList[-1][1] = (speedList[-1][1] + speedList[-2][1] + speedList[-3][1]) / 3
        #     speedList[-2][1] = (speedList[-1][1] + speedList[-2][1] + speedList[-3][1] + speedList[-4][1]) / 4
        #     for dot_num in range(2, len(speedList) - 2):
        #         speedList[dot_num][1] = (speedList[dot_num - 2][1] + speedList[dot_num - 1][1] + speedList[dot_num][1] + speedList[dot_num + 1][1] + speedList[dot_num + 2][1]) / 5
        
        if len(speedList)>=5:
            speedData.append(speedList) #[speedList1,sppedList2,...]
        else:
            delete.append(k)#需要删去的数据    
    for i in range(len(delete)):
        del(ids[delete[i]-i])
        del(labelList[delete[i]-i])
        del(dataList[delete[i]-i])

    return speedData

 #获取训练数据的加速度
def getTrainAccSpeedList(ids,speedData,labelList):
    return getTrainSpeedList(ids,speedData,labelList)
    
#获取回归预测数据
def getRegressDataFromTxt(src):

    fr = open(src,'r') #src=".\\dsjtzs_txfz_test1.txt\\dsjtzs_txfz_test1.txt"
    arrayOfLines = fr.readlines()
    ids = [];#存放数据序号
    dataList = []; #存放数据
    
    for arrayOfLine in arrayOfLines:
        #空格，分号
        id = arrayOfLine.split()[0]
        targetPoint = arrayOfLine.split()[2] # 目标点 '1420.5,202'
        xyt_list = arrayOfLine.split()[1].split(";") # 轨迹点 ['x0,y0,t0','x1,y1,t1',...]
        
        #数据预处理
        #减去目标点的到相对位置点
        data = []
        for xyt in xyt_list[:-1]:#xyt_list最后一个为'',因此去掉
            #逗号
            x = float(xyt.split(",")[0]) - float(targetPoint.split(",")[0]) #x坐标
            y = float(xyt.split(",")[1]) - float(targetPoint.split(",")[1]) #y坐标
            t = float(xyt.split(",")[2]) #t坐标
            data.append([x,y,t])
        
        ids.append(id)
        dataList.append(data) #data=[[x0,y0,t0],[x1,y1,t1]...]] dataList = [data1,data2...]
    return ids,dataList
    
#获取回归预测的速度数据
def getRegressSpeedList(ids,dataList): # dataList = [data1,data2...]
    speedData=[]
    delete = []
    for k in range(len(dataList)):
        data=dataList[k]# data=[[x0,y0,t0],[x1,y1,t1]...]]
        speedList=[]
        for i in range(len(data) - 1):
            xinc = data[i+1][0] - data[i][0]
            yinc = data[i+1][1] - data[i][1]
            tinc = data[i+1][2] - data[i][2]
            if tinc <= 0:
                continue
            speed_x = abs(xinc/tinc) #x方向的速度 speed_x = 40
            speed_y = abs(yinc/tinc) #y方向的速度 speed_y = 30
            speed_t = data[i+1][2]
            speedList.append([speed_x,speed_y,speed_t]) #speedList=[[40,30,50],...]
        if len(speedList)>=5:
            speedData.append(speedList) #[speedList1,sppedList2,...]
        else: 
            delete.append(k)    
    for i in range(len(delete)):
        del(ids[delete[i]-i])
        del(dataList[delete[i]-i])

    return speedData

 #获取测试数据的加速度
def getRegressAccSpeedList(ids,speedData):
    return getRegressSpeedList(ids,speedData)
 
# ids,dataList,labelLists = getTrainDataFromTxt("./dsjtzs_txfz_training.txt/dsjtzs_txfz_training.txt")
# speedData = getTrainSpeedList(ids,dataList,labelLists)
# accData = getTrainAccSpeedList(ids,speedData,labelLists)
# predictids,predictData=getRegressDataFromTxt("./dsjtzs_txfz_test1.txt/dsjtzs_txfz_test1.txt")
# predictSpeedData = getRegressSpeedList(predictids,predictData)
# predictAccData = getRegressAccSpeedList(predictids,predictSpeedData)