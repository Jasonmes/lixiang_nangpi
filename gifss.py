import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 定义三元三次函数
def f(x, y, z):
    return x**3 + 2*y**3 - 3*z**3 + 2*x*y - 4*y*z + 6*x*z + 5

# 创建一个图形和坐标轴
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# 定义x和y的范围
x = np.linspace(-2, 2, 30)
y = np.linspace(-2, 2, 30)
x, y = np.meshgrid(x, y)

# 初始化图形
def init():
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('f(x, y, z)')
    ax.set_title('f(x, y, z) = x^3 + 2y^3 - 3z^3 + 2xy - 4yz + 6xz + 5')

# 更新图形
def update(z):
    ax.cla()
    init()
    z_value = z / 10
    ax.plot_surface(x, y, f(x, y, z_value), cmap='viridis')
    ax.set_zlim(-100, 100)

# 创建动画
ani = FuncAnimation(fig, update, frames=range(-20, 21), init_func=init)

# 保存为GIF
ani.save('3d_function.gif', writer='imagemagick', fps=10)

# 显示图形（可选，如果你想在交互式窗口中看到图形）
plt.show()
