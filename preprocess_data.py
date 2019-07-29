#-*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd

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

    if name == '开关1信号' or '开关2信号' or '告警信号1':
        df[name + '时间占比'] = data.sum()/len(data)
    elif name == '温度信号' or '流量信号':
        df[name + '均值'] = data.mean()
        df[name + '标准差'] = data.std()
    elif name == '累积量参数1' or '累积量参数2':
        df[name] = data.max()
    elif name == '电流信号':
        length = len(data)
        low_current = list(num for num in data if 0 <= num < 20)
        mid_current = list(num for num in data if 20 <= num < 120)
        high_current = list(num for num in data if 120 <= num < 140)
        low_percentage = np.sum(low_current) / length
        mid_percentage = np.sum(mid_current) / length
        high_percentage = np.sum(high_current) / length
        df[name + '低电流段均值'] = np.mean(low_current) * low_percentage
        df[name + '中电流段均值'] = np.mean(mid_current) * mid_percentage
        df[name + '高电流段均值'] = np.mean(high_current) * high_percentage
        df[name + '低电流段标准差'] = np.std(low_current) * low_percentage
        df[name + '中电流段标准差'] = np.std(mid_current) * mid_percentage
        df[name + '高电流段标准差'] = np.std(high_current) * high_percentage
    elif name == '压力信号1':
        length = len(data)
        low_pressure = list(num for num in data if 65 <= num <=75)
        high_pressure = list(num for num in data if 180 <= num <= 400)
        low_percentage = np.sum(low_pressure) / length
        high_percentage = np.sum(high_pressure) / length
        df[name + '信号1低压力段标准差'] = np.std(low_pressure) * low_percentage
        df[name + '信号1高压力段标准差'] = np.std(high_pressure) * high_percentage
    elif name == '压力信号2':
        length = len(data)
        low_pressure = list(num for num in data if 0 <= num <=100)
        high_pressure = list(num for num in data if 150 <= num)
        low_percentage = np.sum(low_pressure) / length
        high_percentage = np.sum(high_pressure) / length
        df[name + '信号2低压力段标准差'] = np.std(low_pressure) * low_percentage
        df[name + '信号2高压力段标准差'] = np.std(high_pressure) * high_percentage
    elif name == '转速信号1':
        length = len(data)
        low_pressure = list(num for num in data if 0 <= num <=100)
        high_pressure = list(num for num in data if 150 <= num)
        low_percentage = np.sum(low_pressure) / length
        high_percentage = np.sum(high_pressure) / length
        df[name + '信号1低转速段标准差'] = np.std(low_pressure) * low_percentage
        df[name + '信号1高转速段标准差'] = np.std(high_pressure) * high_percentage
    elif name == '转速信号2':
        length = len(data)
        low_pressure = list(num for num in data if 0 <= num <=100)
        high_pressure = list(num for num in data if 150 <= num)
        low_percentage = np.sum(low_pressure) / length
        high_percentage = np.sum(high_pressure) / length
        df[name + '信号2低转速段标准差'] = np.std(low_pressure) * low_percentage
        df[name + '信号2高转速段标准差'] = np.std(high_pressure) * high_percentage

#处理单个训练样本
def process_single_sample (e,train_percentage):
    data = pd.read_csv(e)
    work_life = data['部件工作时长'].max()
    data['部件工作时长'] = 

#主进程
if __name__ == '__main__':

    path = 'train'
    train_list = get_filelist(path,[])
    data = {'1':[1,2,3,4,5,6,7,8,9],'2':[1,2,3,4,4,5,6,7,8]}
    a = [1,2,3,4,5,6,7,7,8,9]
    frame = pd.DataFrame(data)
    print (train_list)