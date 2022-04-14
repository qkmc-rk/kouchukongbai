import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

def drawContourMap(X, Y, Z, toPath, fileName, Z_MIN=0, Z_MAX=500, Z_STEP=1, LINE_STEP=10):
    print(Z_MIN,Z_MAX,Z_STEP,LINE_STEP)
    '''
        XYZ画图参数  fileName保存成文件的文件名  toPath 保存文件的路径
    '''
    #将原始数据变成网格数据形式
    X, Y = np.meshgrid(X, Y)
    N = np.arange(Z_MIN, Z_MAX, Z_STEP)
    CS = plt.contourf(X,Y,Z,N,linewidth=1,cmap=mpl.cm.jet)
    plt.colorbar(CS)
    plt.savefig(toPath + fileName + '_without_line.jpg')
    plt.contour(X,Y,Z,LINE_STEP)
    plt.savefig(toPath + fileName + '.jpg')
    plt.close()
    plt.show()

def read3DdataFromExcel(file):
    '''
    file 是excel文件的位置
    这个函数的作用是读入xls文件，然后把EX和EM取出来作为X和Y，FL数组作为Z，然后返回
    '''
    sample = pd.read_excel(file, header=None, index_col=None)
    ar = np.array(sample)
    X = (ar[0])[1:]  # 第一行中除去第一个元素 EX作X
    Y = ((ar.T)[0])[1:]  # 第一列中除去第一个元素 EM 作 Y
    Z = ((ar[1:].T)[1:]).T  # 除去第一行和第一列 fl 作 数据
    return X, Y, Z

files = os.listdir('./')
samples_has_scatter = []
samples_no_scatter = []
for file in files:
    # 使用简单的过滤操作把去除散射前后的文件过滤出来
    if 'rm_scatter' in file and 'raman_k' in file:
        samples_no_scatter.append(file)
    if 'rm_scatter'  not in file and 'raman_k' in file:
        samples_has_scatter.append(file)

# 开始绘图
# 先绘制有散射的图
for sample in samples_has_scatter:
    X, Y, Z = read3DdataFromExcel(sample)
    # 这里注意, 因为我们进行了拉曼归一化操作,所以不能使用默认的ZMIN和ZMAX,需要我们自己定义
    Z_MIN = np.nanmin(Z) # 这个函数可以忽略nan值
    Z_MAX = np.nanmax(Z) # 这个函数可以忽略nan值
    Z_STEP = (Z_MAX - Z_MIN) / 100.
    drawContourMap(X, Y, Z, './pic/', sample, Z_MIN=Z_MIN, Z_MAX=Z_MAX, Z_STEP=Z_STEP, LINE_STEP=10)

# 然后绘制没有散射的图
for sample in samples_no_scatter:
    X, Y, Z = read3DdataFromExcel(sample)
    # 这里注意, 因为我们进行了拉曼归一化操作,所以不能使用默认的ZMIN和ZMAX,需要我们自己定义
    Z_MIN = np.nanmin(Z) # 这个函数可以忽略nan值
    Z_MAX = np.nanmax(Z) # 这个函数可以忽略nan值
    Z_STEP = (Z_MAX - Z_MIN) / 100.
    drawContourMap(X, Y, Z, './pic/', sample, Z_MIN=Z_MIN, Z_MAX=Z_MAX, Z_STEP=Z_STEP, LINE_STEP=10)