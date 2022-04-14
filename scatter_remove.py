import pandas as pd
import numpy as np

# 先定义一个函数，用来把切掉散射的数据保存到excel文件中
def martrix_to_excel(name, ex, em, fl):
    '''
    参数说明：
        name: 保存文件的路径 + 名称,我们这里直接保存到根目录
    '''
    fl = np.insert(fl, 0, ex, 0)
    fl = fl.T
    em = np.insert(em, 0, 0)
    fl = np.insert(fl, 0, em, 0)
    fl = fl.T
    df = pd.DataFrame(fl)
    df.to_excel(name, header=False, index=False)

samples = ['raman_k_sample-1.xls','raman_k_sample-2.xls','raman_k_sample-3.xls']

for sample in samples:
    # 备份一个文件名
    name = sample

    # 转换成矩阵
    sample = pd.read_excel(sample, header=None, index_col=None)
    sample = np.array(sample)
    
    EX = (sample[0])[1: ]   # 取ex
    EM = ((sample.T)[0])[1: ] # 取em
    FL = (((sample[1: ]).T)[1: ]).T   # 取 fl

    # 第二步根据ex和em找到散射峰位置然后直接去散射
    FL = FL.T
    for i in range(len(FL)): # 遍历ex
        for j in range(len(FL[i])): # 遍历em
            ex = 200 + i * 10
            em = 250 + j * 5
            if(ex >= em - 20 and ex <= em + 20): #  and ex <= em + 20
                FL[i, j] = None # 不能使用0, 因为0是有意义的数据
            if(em >= 2 * ex - 20 and em <= 2 * ex + 20): #  and em <= 2 * ex + 20
                FL[i, j] = None # 不能使用0, 因为0是有意义的数据
            if(em < 1.55 *ex -190 and em > 1.55*ex -240): # and ex > 380 and em <= 2 * ex + 20     1.4x - 115
                FL[i, j] = None  # 不能使用0, 因为0是有意义的数据
    FL = FL.T

    # 保存文件
    martrix_to_excel('rm_scatter_' + name, EX, EM, FL)