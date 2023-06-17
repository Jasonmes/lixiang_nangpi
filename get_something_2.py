import cv2
import numpy as np

# 读取图片
image = cv2.imread('image/14.bmp')

# 转换到灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 进行二值化处理
threshold_value = 127  # 可以根据需要调整阈值
_, binary_image = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

# 显示二值化处理后的图像
cv2.imwrite('binary_image.jpg', binary_image)
cv2.imshow('Binary Image', binary_image)
cv2.waitKey(0)

# 寻找轮廓
contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 在原图上绘制轮廓
cv2.drawContours(image, contours, -1, (0, 0, 250), 2)  # 使用红色绘制轮廓

# 显示处理后的图像
cv2.imwrite('Contours.jpg', image)
cv2.imshow('Contours', image)
cv2.waitKey(0)

# 找到最大的轮廓
# max_contour = max(contours, key=cv2.contourArea)

# 在原图上绘制最大轮廓
# cv2.drawContours(image, [max_contour], -1, (0, 255, 0), 2)  # 使用绿色绘制轮廓

# 显示处理后的图像
# cv2.imshow('Max Contour', image)
# cv2.waitKey(0)

# 使用高斯模糊平滑图像以减少检测错误的圆
smoothed_gray = cv2.GaussianBlur(gray, (9, 9), 2)

# 减小图像大小
smaller = cv2.resize(smoothed_gray, (0,0), fx=0.1, fy=0.1) 

# 使用Hough变换检测圆
circles = cv2.HoughCircles(smaller, cv2.HOUGH_GRADIENT, dp=1, minDist=900,
                           param1=50, param2=50, minRadius=100, maxRadius=0)





print(circles)

# 创建一个新图像用于绘制检测到的圆
image_with_circles = np.copy(image)

# 如果检测到圆，绘制它们
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # 画出外圆
        cv2.circle(image_with_circles, (i[0], i[1]), i[2], (255, 255, 0), 2)
        # 画出圆心
        # cv2.circle(image_with_circles, (i[0], i[1]), 2, (0, 0, 255), 3)


# 显示处理后的图像
# cv2.imshow('Detected Circles', image)
cv2.imwrite('image_with_circles.jpg', image_with_circles)
cv2.waitKey(0)