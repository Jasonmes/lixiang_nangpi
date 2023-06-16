import numpy as np
import pandas as pd

# 原始数据
donations = [
    [242, 282, 254, 345],
    [253, 290, 262, 352],
    [270, 286, 271, 378]
]

# 季节性因子
seasonal_factors = [0.96, 1.08, 0.99, 1.35]

# 去除季节性效应
deseasonalized = [[donations[y][q] / seasonal_factors[q] for q in range(4)] for y in range(3)]

# 展平数据
flat_deseasonalized = [deseasonalized[y][q] for y in range(3) for q in range(4)]

# 初始化结果表格
results = pd.DataFrame(columns=['Method', 'MAD (Seasonal)', 'MSE (Seasonal)'])

# 上期值法
predictions = [flat_deseasonalized[0]] + flat_deseasonalized[:-1]
errors = [predictions[i] - flat_deseasonalized[i] for i in range(len(flat_deseasonalized))]
mad = np.mean(np.abs(errors))
mse = np.mean(np.square(errors))
results.loc[len(results)] = ['Naive Method', mad, mse]

# 平均值法
mean = np.mean(flat_deseasonalized[:-1])
predictions = [mean for _ in range(len(flat_deseasonalized))]
errors = [predictions[i] - flat_deseasonalized[i] for i in range(len(flat_deseasonalized))]
mad = np.mean(np.abs(errors))
mse = np.mean(np.square(errors))
results.loc[len(results)] = ['Average Method', mad, mse]

# 移动平均法 (基于最近的4个季度)
predictions = [np.mean(flat_deseasonalized[max(0, i-4):i]) for i in range(1, len(flat_deseasonalized) + 1)]
errors = [predictions[i] - flat_deseasonalized[i] for i in range(len(flat_deseasonalized))]
mad = np.mean(np.abs(errors))
mse = np.mean(np.square(errors))
results.loc[len(results)] = ['Moving Average Method', mad, mse]

# 指数平滑法
alpha = 0.2
smoothed = [flat_deseasonalized[0]]
for i in range(1, len(flat_deseasonalized)):
    smoothed.append(alpha * flat_deseasonalized[i-1] + (1-alpha) * smoothed[i-1])
errors = [smoothed[i] - flat_deseasonalized[i] for i in range(len(flat_deseasonalized))]
mad = np.mean(np.abs(errors))
mse = np.mean(np.square(errors))
results.loc[len(results)] = ['Exponential Smoothing', mad, mse]

# 趋势性指数平滑法
alpha = 0.2
# beta = 0.2
# level = [flat_deseasonalized[0]]
# trend =
# 趋势性指数平滑法
beta = 0.2
level = [flat_deseasonalized[0]]
trend = [flat_deseasonalized[1] - flat_deseasonalized[0]]
holt = [level[0] + trend[0]]

for i in range(1, len(flat_deseasonalized)):
    level.append(alpha * flat_deseasonalized[i] + (1-alpha) * (level[i-1] + trend[i-1]))
    trend.append(beta * (level[i] - level[i-1]) + (1-beta) * trend[i-1])
    holt.append(level[i] + trend[i])

errors = [holt[i] - flat_deseasonalized[i] for i in range(len(flat_deseasonalized))]
mad = np.mean(np.abs(errors))
mse = np.mean(np.square(errors))
results.loc[len(results)] = ['Holt\'s Linear Method', mad, mse]

# 将预测值调整回原始的尺度并重新计算MAD和MSE
for index, row in results.iterrows():
    method = row['Method']
    
    if method == 'Naive Method':
        adjusted_predictions = [predictions[i] * seasonal_factors[i % 4] for i in range(len(flat_deseasonalized))]
    elif method == 'Average Method':
        adjusted_predictions = [mean * seasonal_factors[i % 4] for i in range(len(flat_deseasonalized))]
    elif method == 'Moving Average Method':
        adjusted_predictions = [predictions[i] * seasonal_factors[i % 4] for i in range(len(flat_deseasonalized))]
    elif method == 'Exponential Smoothing':
        adjusted_predictions = [smoothed[i] * seasonal_factors[i % 4] for i in range(len(flat_deseasonalized))]
    elif method == 'Holt\'s Linear Method':
        adjusted_predictions = [holt[i] * seasonal_factors[i % 4] for i in range(len(flat_deseasonalized))]
    
    adjusted_errors = [adjusted_predictions[i] - donations[y][q] for i, (y, q) in enumerate([(y, q) for y in range(3) for q in range(4)])]
    adjusted_mad = np.mean(np.abs(adjusted_errors))
    adjusted_mse = np.mean(np.square(adjusted_errors))
    results.at[index, 'MAD (Seasonal)'] = adjusted_mad
    results.at[index, 'MSE (Seasonal)'] = adjusted_mse

# 显示结果表格
print(results)
