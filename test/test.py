import numpy as np

# 原始数组
arr = np.array([[1, 2, 3], [2, 3, 4]])
print(arr.shape)

# 计算相邻元素的平均值
result = (arr[:, :-1] + arr[:, 1:]) / 2
print(result)
