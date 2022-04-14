import os
import numpy as np
import pandas as pd

# ex = 350nm或者附近处的em-fl向量(em从365 - 430nm, 或者附近) 
# interval是em的间隔,比如间隔是1nm/5nm/10nm等
# 拉曼积分
def raman_integral(fl_vector: list, interval: int):
    integral = 0. # 拉曼积分值
    for i in range(len(fl_vector) - 1):
        # 使用梯形面积累加计算拉曼积分
        integral = integral + ((fl_vector[i] + fl_vector[i + 1]) * interval) / 2.
    return integral

# 直接返回拉曼单位
def raman_standard(blank, data):
    blank_fl = blank[1:, 1:] # 取出空白样品的fl矩阵数据 去掉blank的第一行EX第一列EM
    fl = data[1:, 1:]  # 这是测量的正常样本的fl矩阵
    integral_region = (blank_fl.T)[15] # ex = 350  这里根据你自己的样本的情况，计算一下ex=350nm是第几列，我的是第16列，索引从0开始，就是15.
    integral_region = integral_region[23: 36 + 1] # em 365  - 430 含头不含尾，从数组中截取出EM = 365至430处的数据。
    integral = raman_integral(fl_vector= integral_region, interval= 5) # 调用2.1定义的函数，获得积分值
    integral = round(integral, 2) # 积分数值 # 保留小数2位
    fl = np.array(fl) / integral  # 拉曼归一化，核心的一步
    # 先单独取出ex和em数组
    ex = (data[0]) # 注意没有去掉第一个NaN值，因为先拼接em, ex需要前面补一位
    em = (data.T)[0][1:]
    # 把ex和em和拉曼归一化后的fl矩阵进行融合，生成完整的F-EEM矩阵
    fl = np.c_[em, fl]
    fl = np.c_[ex, fl.T]
    fl = fl.T

    return fl # 携带ex em


blank = np.array(pd.read_excel('./blank.xls', header=None, index_col=None))
# 这里的样本是扣除空白之后的, 注意一下
samples = ['k_sample-1.xls', 'k_sample-2.xls', 'k_sample-3.xls']
# 拉曼归一化
for sample in samples:
    data =  np.array(pd.read_excel(sample, header=None, index_col=None))
    fl = raman_standard(blank, data)
    df = pd.DataFrame(fl)
    df.to_excel('raman_' + sample, header=False, index=False)