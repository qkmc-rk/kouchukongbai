# Python处理三维荧光数据的一些教程

# 文章地址：
https://www.zhihu.com/people/ruankun/posts

该实验中，原始数据有4个, blank.xls为超纯水样本, sample-1.xls, sample-2.xls, sample-3.xls为3个河水荧光样本数据

1. 运行k.py后得到扣除空白的三个文件k_**.xls
2. 运行raman_norm.py后得到拉曼矫正后的三个文件raman_***.xls
3. 运行scatter_remove.py后得到去除散射的三个文件rm_scatter_***.xls
4. 运行draw.py后在pic目录下生成去除散射前后的等高线图.
