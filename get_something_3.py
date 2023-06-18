import cv2
import numpy as np

# 读取图片
image = cv2.imread('image/new.bmp')

# 转换到灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 进行二值化处理
threshold_value = 54  # 可以根据需要调整阈值
_, binary_image = cv2.threshold(gray, threshold_value, 255, cv2.THRESH_BINARY)

# 显示二值化处理后的图像
cv2.imwrite('new_binary_image.jpg', binary_image)
cv2.imshow('new_Binary Image', binary_image)
cv2.waitKey(0)

# 寻找轮廓
contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# 在原图上绘制轮廓
# cv2.drawContours(image, contours, -1, (0, 0, 250), 2)  # 使用红色绘制轮廓

# 显示处理后的图像
# cv2.imwrite('new_Contours.jpg', image)
# cv2.imshow('new_Contours', image)
# cv2.waitKey(0)

# 找到最大的近似椭圆形状的轮廓
max_area = 0
max_ellipse_contour = None
for contour in contours:
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

# 高斯模糊以减少噪音和错误检测
blur = cv2.GaussianBlur(gray, (9, 9), 2)

# 使用Hough Circle Transform检测圆
# 900和1000是关键
circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=50,
                           param1=50, param2=30, minRadius=900, maxRadius=1100)

import random

# 初始化边界矩形的坐标
x_min = y_min = np.inf
x_max = y_max = 0


# 初始化圆心坐标的和
sum_x = 0
sum_y = 0
count = 0


# 确保至少找到一个圆
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        # 随机生成颜色
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        
        # 画出外圆
        # cv2.circle(image, (i[0], i[1]), i[2], color, 10)
        
        # 画出圆心
        # cv2.circle(image, (i[0], i[1]), 2, color, 10)

        # 累加圆心坐标
        sum_x += i[0]
        sum_y += i[1]
        count += 1

        
        # 更新边界矩形的坐标
        x_min = min(x_min, i[0] - i[2])
        y_min = min(y_min, i[1] - i[2])
        x_max = max(x_max, i[0] + i[2])
        y_max = max(y_max, i[1] + i[2])


        # # 显示处理后的图像
        # cv2.imshow('Hough Circles', image)
        # cv2.waitKey(0)


    # 计算圆心的平均值
    if count > 0:
        # avg_x = sum_x / count
        # avg_y = sum_y / count

        avg_x = int(round(sum_x / count))
         
        avg_y = int(round(sum_y / count))

        print(f"Average center of the circles is at ({avg_x}, {avg_y})")
        # 以平均圆心为中心，画一个半径为980的圆
        cv2.circle(image, (avg_x, avg_y), 940, (255, 255, 255), 10)
        # 以平均圆心为中心，画一个半径为980的圆
        cv2.circle(image, (avg_x, avg_y), 980, (255, 255, 255), 10)

        # 显示处理后的图像
        cv2.imshow('外圆和内圆', image)
        cv2.waitKey(0)


    # 使用合并的边界矩形截取ROI
    roi = image[y_min:y_max, x_min:x_max]

    # 显示ROI
    cv2.imshow('ROI', roi)
    cv2.waitKey(0)

    # 保存ROI到文件
    cv2.imwrite('ROI.jpg', roi)

cv2.destroyAllWindows()



# # 显示处理后的图像
# cv2.imwrite('multi.jpg', image)
# # cv2.imshow('Hough Circles', image)
# # cv2.waitKey(0)
# cv2.destroyAllWindows()
