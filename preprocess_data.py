#-*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from multiprocessing import Pool

#获取文件地址
def get_filelist (dir,flielist):

    new_dir = dir
    if os.path.isfile(dir):
        flielist.append(dir)
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            new_dir = os.path.join(dir,s)
            get_filelist(new_dir,flielist)
    return flielist

#处理数据
def preprocess (data,df,name):

    #根据样本选择或处理特征

    #开关与告警信号取其在总数据中的占比
    if name == '开关1信号' or name == '开关2信号' or name == '告警信号1':
        df[name + '时间占比'] = data.sum()/len(data)
    
    #温度信号取其均值与标准差为特征
    elif name == '温度信号' or name == '流量信号':
        df[name + '均值'] = data.mean()
        df[name + '标准差'] = data.std()
    
    #累积量参数不明白其意义，但随时间增加而增加，暂取最大值为特征
    elif name == '累积量参数1' or name == '累积量参数2':
        df[name] = data.max()

    #电流信号主要集中分布在三段区间中，分别列出取均值与方差，加权后取为特征
    elif name == '电流信号':
        length = len(data)
        low_current = list(num for num in data if 0 <= num < 20)
        mid_current = list(num for num in data if 500 <= num < 750)
        high_current = list(num for num in data if 800 <= num < 1800)
        low_percentage = np.sum(low_current) / length
        mid_percentage = np.sum(mid_current) / length
        high_percentage = np.sum(high_current) / length
        df[name + '低电流段均值'] = np.mean(low_current) * low_percentage
        df[name + '中电流段均值'] = np.mean(mid_current) * mid_percentage
        df[name + '高电流段均值'] = np.mean(high_current) * high_percentage
        df[name + '低电流段标准差'] = np.std(low_current) * low_percentage
        df[name + '中电流段标准差'] = np.std(mid_current) * mid_percentage
        df[name + '高电流段标准差'] = np.std(high_current) * high_percentage

    #流量信号主要集中分布在三段区间中，分别列出取均值与方差，加权后取为特征
    elif name == '流量信号':
        length = len(data)
        low_current = list(num for num in data if 0 <= num < 9)
        mid_current = list(num for num in data if 10 <= num < 120)
        high_current = list(num for num in data if 125 <= num < 145)
        low_percentage = np.sum(low_current) / length
        mid_percentage = np.sum(mid_current) / length
        high_percentage = np.sum(high_current) / length
        df[name + '低流量段均值'] = np.mean(low_current) * low_percentage
        df[name + '中流量段均值'] = np.mean(mid_current) * mid_percentage
        df[name + '高流量段均值'] = np.mean(high_current) * high_percentage
        df[name + '低流量段标准差'] = np.std(low_current) * low_percentage
        df[name + '中流量段标准差'] = np.std(mid_current) * mid_percentage
        df[name + '高流量段标准差'] = np.std(high_current) * high_percentage
    
    #压力信号1主要分布在两段区间上，同上取均值与方差加权后取为特征
    elif name == '压力信号1':
        length = len(data)
        low_pressure = list(num for num in data if 65 <= num <=75)
        high_pressure = list(num for num in data if 180 <= num <= 400)
        low_percentage = np.sum(low_pressure) / length
        high_percentage = np.sum(high_pressure) / length
        df[name + '信号1低压力段标准差'] = np.std(low_pressure) * low_percentage
        df[name + '信号1高压力段标准差'] = np.std(high_pressure) * high_percentage
    
    #压力信号2主要分布在一段区间上，剩余值较小，处理同上
    elif name == '压力信号2':
        length = len(data)
        low_pressure = list(num for num in data if 0 <= num <=100)
        high_pressure = list(num for num in data if 150 <= num)
        low_percentage = np.sum(low_pressure) / length
        high_percentage = np.sum(high_pressure) / length
        df[name + '信号2低压力段标准差'] = np.std(low_pressure) * low_percentage
        df[name + '信号2高压力段标准差'] = np.std(high_pressure) * high_percentage

    #同压力信号2
    elif name == '转速信号1':
        length = len(data)
        low_pressure = list(num for num in data if 0 <= num <=100)
        high_pressure = list(num for num in data if 150 <= num)
        low_percentage = np.sum(low_pressure) / length
        high_percentage = np.sum(high_pressure) / length
        df[name + '信号1低转速段标准差'] = np.std(low_pressure) * low_percentage
        df[name + '信号1高转速段标准差'] = np.std(high_pressure) * high_percentage
    
    #同压力信号2
    elif name == '转速信号2':
        length = len(data)
        low_pressure = list(num for num in data if 0 <= num <=100)
        high_pressure = list(num for num in data if 150 <= num)
        low_percentage = np.sum(low_pressure) / length
        high_percentage = np.sum(high_pressure) / length
        df[name + '信号2低转速段标准差'] = np.std(low_pressure) * low_percentage
        df[name + '信号2高转速段标准差'] = np.std(high_pressure) * high_percentage

    return df

#处理单个训练样本
def process_single_sample (e,train_percentage):

    data = pd.read_csv(e)
    #获取该零件寿命
    work_life = data['部件工作时长'].max()
    #获取在寿命一定百分比时间的数据
    data=data[data['部件工作时长']<=work_life*train_percentage]
    #创建数据集
    dict_data = { 'train_file_name': os.path.basename(e) + str(train_percentage),
                       'device': data['设备类型'][0],
                       'rest_life':work_life-data['部件工作时长'].max()
                     }
    for item in ['部件工作时长',
                    '累积量参数1',
                    '累积量参数2',
                    '转速信号1',
                    '转速信号2',
                    '压力信号1',
                    '压力信号2',
                    '温度信号',
                    '流量信号',
                    '电流信号',
                    '开关1信号',
                    '开关2信号',
                    '告警信号1']:
        dict_data=preprocess(data[item],dict_data,item)
    features = pd.DataFrame(dict_data, index=[0])  

    return features

#整合处理训练集与测试集,并采用多线程
def integrated_process (cpu,path_list,test_or_not,func):
    
    if test_or_not == True:
        train_percentage_list = [1]
        apply_object = []
        pool = Pool(cpu)
        for path in path_list:
            for train_percentage in train_percentage_list:
                apply_object.append(pool.apply_async(func, args=(path,train_percentage,)))
        pool.close()
        pool.join()
        apply_object = [i.get() for i in apply_object]
        features = apply_object[0]
        for i in apply_object[1:]:
            features = pd.concat([features, i], axis=0)
        columns=features.columns.tolist()
        for col in ['train_file_name','life']:
            columns.remove(col)
        columns=['train_file_name']+columns+['life']
        features['train_file_name']=features['train_file_name'].apply(lambda x:x[:-1])
        features=features.reindex(columns=columns)

def asd (x):
    x = x+1
    return x

#主进程，调试使用
if __name__ == '__main__':

    #获取路径集
    path_name= 'train'
    train_list = get_filelist(path,[])

    #绘制图像观测数据分布特征
    plt.figure()
    for csv_path in train_list:
        raw_data = pd.read_csv(csv_path)
        plt.scatter(raw_data['部件工作时长'],raw_data['温度信号'])

        #窗口最大化
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed') #works fine on Windows!

        plt.show()