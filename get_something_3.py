import cv2
import numpy as np

# 读取图片
image = cv2.imread('image/new.bmp')

# 转换到灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 进行二值化处理
threshold_value = 127  # 可以根据需要调整阈值
_, binary_image = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

# 显示二值化处理后的图像
cv2.imwrite('new_binary_image.jpg', binary_image)
cv2.imshow('new_Binary Image', binary_image)
cv2.waitKey(0)

# 寻找轮廓
contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 在原图上绘制轮廓
cv2.drawContours(image, contours, -1, (0, 0, 250), 2)  # 使用红色绘制轮廓

# 显示处理后的图像
cv2.imwrite('new_Contours.jpg', image)
cv2.imshow('new_Contours', image)
cv2.waitKey(0)



# 找到最大的近似椭圆形状的轮廓
max_area = 0
max_ellipse_contour = None
for contour in contours:
    # 计算轮廓的圆度，接近1表示接近圆形
    # 计算轮廓的圆度，接近1表示接近圆形
    perimeter = cv2.arcLength(contour, True)
    area = cv2.contourArea(contour)
    if perimeter > 0:
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if 0.7 < circularity < 1.3 and area > max_area:  # 这个范围可以根据需要调整
            max_area = area
            max_ellipse_contour = contour


# 在原图上绘制最大的椭圆形状的轮廓
if max_ellipse_contour is not None:
    cv2.drawContours(image, [max_ellipse_contour], -1, (0, 255, 0), 20)  # 使用绿色绘制轮廓


# 显示处理后的图像
cv2.imwrite('Max-Ellipse-Contour.jpg', image)
cv2.imshow('Max Ellipse Contour', image)
cv2.waitKey(0)
cv2.destroyAllWindows()


