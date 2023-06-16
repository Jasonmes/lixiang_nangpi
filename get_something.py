import cv2
import numpy as np

# 读取图片
image = cv2.imread('image/14.bmp')

# 转换到灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# cv2.imshow('gray', gray)
# cv2.waitKey(0)


# 阈值化以找到与黑色接近的部分
lower_bound = np.array([25, 25, 25])
upper_bound = np.array([125, 125, 125])  # 你可以调整这个上限来定义“接近黑色”的范围
mask = cv2.inRange(image, lower_bound, upper_bound)
cv2.imshow('mask', mask)
cv2.waitKey(0)


# 寻找轮廓
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 过滤和画出轮廓
for contour in contours:
    # 可以使用cv2.approxPolyDP()来近似轮廓形状
    # 使用cv2.contourArea()和cv2.arcLength()来过滤掉太小或形状不对的轮廓
    if cv2.contourArea(contour) > 100:  # 这个阈值可以根据需要调整
        # 计算轮廓的圆度，接近1表示接近圆形
        perimeter = cv2.arcLength(contour, True)
        area = cv2.contourArea(contour)
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if 0.7 < circularity < 1.2:  # 这个范围可以根据需要调整
            cv2.drawContours(image, [contour], 0, (0, 255, 0), 2)  # 在原图上以绿色画出轮廓

# 显示处理后的图像
cv2.imshow('Detected Circular Object', image)
cv2.waitKey(0)


# 对找到的轮廓拟合椭圆
for contour in contours:
    if len(contour) >= 5:  # 需要至少5个点来拟合椭圆
        ellipse = cv2.fitEllipse(contour)
        
        # 检查椭圆的尺寸和位置
        center, axes, angle = ellipse
        if axes[0] >= 0 and axes[1] >= 0:
            # 绘制椭圆
            cv2.ellipse(image, ellipse, (0, 255, 0), 2)  # 在原图上以绿色画出椭圆轮廓

# 显示处理后的图像
cv2.imshow('Fitted Ellipse', image)
cv2.waitKey(0)


# 找到最大的椭圆
max_area = 0
max_ellipse = None
for contour in contours:
    if len(contour) >= 5:  # 需要至少5个点来拟合椭圆
        ellipse = cv2.fitEllipse(contour)
        
        # 计算椭圆的面积
        center, axes, angle = ellipse
        area = np.pi * (axes[0] / 2) * (axes[1] / 2)
        
        # 更新最大的椭圆
        if area > max_area:
            max_area = area
            max_ellipse = ellipse

# 如果找到了最大的椭圆，绘制它
if max_ellipse is not None:
    cv2.ellipse(image, max_ellipse, (255, 255, 255), 8)  # 以绿色画出最大的椭圆轮廓

# 显示处理后的图像
cv2.imshow('Largest Fitted Ellipse', image)
cv2.waitKey(0)




cv2.destroyAllWindows()
    

