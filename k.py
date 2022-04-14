# 导入我们要用到的工具包
import pandas as pd # pandas用来读取excel和写入excel数据
import numpy as np # numpy用来进行矩阵的运算,加减乘除
import os


# 准备样本列表

blank = 'blank.xls'  # 空白样品的文件名
# 读取当前目录中的文件列表
sample_list = os.listdir('.')
# 移除空白样本
sample_list.remove('blank.xls')
# 移除k.py
sample_list.remove('k.py')

# 接下来我们需要定义两个函数
# 第一个是读取excel到代码中
# 第二个是将代码数据写到excel中

def excel_to_matrix(file):
    '''
    函数的参数file:传入文件名
    '''
    # pandas读取excel文件
    df    = pd.read_excel(file, header=None, index_col=None)
    # numpy将pandas读取的文件转化为numpy的数组数据
    odata = np.array(df)
    # 矩阵的第一行的第二个数据到最后一个数据，是ex列表
    ex = (odata[0])[1: ]   # 取ex
    # 矩阵转置后的第一行的第二个数据到最后一个数据，是em列表
    em = ((odata.T)[0])[1: ] # 取em
    # 去掉矩阵的第一行和第一列,剩下的就是荧光强度
    fl = (((odata[1: ]).T)[1: ]).T   # 取 fl
    # 返回ex, em, 荧光强度
    return ex, em, fl

def martrix_to_excel(file, ex, em, fl):
    '''
    函数的参数file:这里的file是输出的文件名,千万注意不要同已有的
    文件名相同, 不然会覆盖掉已经存在的文件
    '''
    # 在fl这个矩阵的第一行插入一行,ex
    fl = np.insert(fl, 0, ex, 0)
    # 转置一下(转置后ex变成了列)
    fl = fl.T
    # 在fl的第一行插入em行
    em = np.insert(em, 0, 0)
    fl = np.insert(fl, 0, em, 0)
    # 转置一下,把ex变成行,em变成列
    fl = fl.T
    # 包装成pandas的dataframe,便于写入excel
    df = pd.DataFrame(fl)
    # 写入到excel文件
    df.to_excel(file, header=False, index=False)  

# 函数定义完成, 进行操作

# 读入空白样品数据
ex0, em0, fl0 = excel_to_matrix(blank)

# 利用for循环, 循环读取样本数据
for sample in sample_list:
    ex, em, fl = excel_to_matrix(sample)
    # 核心代码, 读取当前样本的fl荧光强度,减去空白样本的荧光强度
    # 这就是扣除空白
    fl = fl - fl0
    # 保存一下,扣除空白后, 加个前缀
    martrix_to_excel('k_' + sample, ex, em, fl)
