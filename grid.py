import numpy as np
import pandas as pd


jmax = 122.247149
jmin =120.856804
wmax = 31.872716
wmin = 30.675593
div = 0.1

# num_j = int((jmax-jmin)//div)
# num_w = int((wmax-wmin)//div)
# re = np.zeros([num_j,num_w]) #re存放落在每一个网格内的边界坐标个数
# border = pd.read_csv(r'D:\ecolab\amap_boundary.csv',header=None) #border.csv存储边界坐标,有经纬度两列。




# # 左下 121.346646,30.675593 右上 122.247149,31.419332

def generate_grids(start_long,start_lat,end_long,end_lat,resolution):
    """
    根据起始的经纬度和分辨率，生成需要需要的网格.
    方向为左上，右下，所以resolution应为 负数，否则未空
    :param start_long:
    :param start_lat:
    :param end_long:
    :param end_lat:
    :param resolution:  划分的网格长度，单位为KM
    :return:
    """
    assert start_long < end_long,'需要从左上到右下设置经度，start的经度应小于end的经度'
    assert start_lat > end_lat,'需要从左上到右下设置纬度，start的纬度应大于end的纬度'
    assert resolution>0,'resolution应大于0'


    grids_lib=[]
    longs = np.arange(start_long,end_long,resolution)
    if longs[-1] != end_long:
        longs = np.append(longs,end_long)

    lats = np.arange(start_lat,end_lat,-resolution)
    if lats[-1] != end_lat:
        lats = np.append(lats,end_lat)
    for i in range(len(longs)-1):
        for j in range(len(lats)-1):
            grids_lib.append([round(float(longs[i]),6),round(float(lats[j]),6),round(float(longs[i+1]),6),round(float(lats[j+1]),6)])
            #yield [round(float(longs[i]),6),round(float(lats[j]),6),round(float(longs[i+1]),6),round(float(lats[j+1]),6)]
    return grids_lib



grids_lib = generate_grids(120.856804, 31.872716,  122.247149, 30.675593, 0.0125)
df = pd.DataFrame(grids_lib)
print(df)
df.to_csv(r'D:\ecolab\grid.csv')
# print(grids_lib)