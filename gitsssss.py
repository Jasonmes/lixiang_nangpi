import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 定义一元二次函数
def f(x, a, b, c):
    return a * x**2 + b * x + c

# 创建一个图形和坐标轴
fig, ax = plt.subplots()

# 定义x的范围
x = np.linspace(-10, 10, 100)

# 初始化图形
line, = ax.plot(x, f(x, 1, 0, 0), 'r-')

# 设置坐标轴标签和标题
ax.set_xlabel('X')
ax.set_ylabel('f(x)')
ax.set_title('f(x) = ax^2 + bx + c')

# 更新图形
def update(frame):
    a = np.sin(frame / 10)
    b = np.cos(frame / 20)
    c = np.sin(frame / 30)
    line.set_ydata(f(x, a, b, c))
    return line,

# 创建动画
ani = FuncAnimation(fig, update, frames=range(0, 100), blit=True)

# 保存为GIF（需要安装ImageMagick）
ani.save('quadratic_function.gif', writer='imagemagick', fps=10)

# 显示图形（可选，如果你想在交互式窗口中看到图形）
plt.show()
