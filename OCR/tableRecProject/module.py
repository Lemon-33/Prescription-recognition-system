import cv2
import math
import numpy as np
import pylab as plt
import copy
from PIL import Image

#冒泡排序
def bubbleSort(arr):
    n = len(arr)
    # 遍历所有数组元素
    for i in range(n):
        # Last i elements are already in place
        for j in range(0, n-i-1):
            if (arr[j] > arr[j+1]) :
                arr[j], arr[j+1] = arr[j+1], arr[j]


def recognize(img_route):
    img = cv2.imread(img_route)  # 读取图片
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 自适应阈值二值化
    img_Threshold = cv2.adaptiveThreshold(~img_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 161, -2)
    img = img_Threshold
    # plt.title('img')
    # plt.imshow(img,cmap="gray")
    # plt.show()

    # plt.subplot(212)
    # plt.title('adaptiveThreshold')
    # plt.imshow(img_Threshold)
    # cv2.imwrite('D:/test2_img_Threshold.jpg',img_Threshold)

    #  opencv
    # ###2 腐蚀erode膨胀dilate
    # original_img = cv2.imread('flower.png')
    # res = cv2.resize(original_img,None,fx=0.6, fy=0.6,
    #                  interpolation = cv2.INTER_CUBIC) #图形太大了缩小一点
    # B, G, R = cv2.split(res)                    #获取红色通道
    # img = R
    # _,RedThresh = cv2.threshold(img,160,255,cv2.THRESH_BINARY)
    # OpenCV定义的结构矩形元素

    scale = 20
    rows = img.shape[0]
    cols = img.shape[1]

    row_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (int(rows / scale), 1))
    col_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int(cols / scale)))

    # #先腐蚀再膨胀
    row_eroded = cv2.erode(img_Threshold, row_kernel)  # 腐蚀图像
    row_dilated = cv2.dilate(row_eroded, row_kernel)  # 膨胀图像
    # 先膨胀再腐蚀
    # row_dilated = cv2.dilate(img_Threshold,row_kernel)      #膨胀图像
    # row_eroded = cv2.erode(row_dilated,row_kernel)        #腐蚀图像

    lines = cv2.HoughLinesP(row_dilated, 1, np.pi / 180, 20, minLineLength=20, maxLineGap=600)
    #print(lines.shape[0])
    # for i in range(lines.shape[0]):
    #     l=lines[i,0]

    # #先腐蚀再膨胀
    col_eroded = cv2.erode(img_Threshold, col_kernel)  # 腐蚀图像
    col_dilated = cv2.dilate(col_eroded, col_kernel)  # 膨胀图像
    # #先膨胀再腐蚀
    # col_dilated = cv2.dilate(img_Threshold,col_kernel)      #膨胀图像
    # col_eroded = cv2.erode(col_dilated,col_kernel)        #腐蚀图像

    lines = cv2.HoughLinesP(col_eroded, 1, np.pi / 360, 20, minLineLength=20, maxLineGap=600)
    #print(lines.shape[0])

    # points_pic为二值化图片 检测到所有的点
    points_pic = cv2.bitwise_and(col_dilated, row_dilated)  # 进行与操作
    # 把点当作圆进行检测 检测失败
    # circles = cv2.HoughCircles(points_pic,cv2.HOUGH_GRADIENT,1,10,
    #                             param1=10,param2=10,minRadius=20,maxRadius=40)

    # 遍历像素点
    points_row = []  # 每一行的横坐标
    all_col = []  # 所有点的纵坐标
    all_col_last = []  # 最后一行的纵坐标
    points_col = []  # 每一行的纵坐标(除去最后一行) 去重后的结果
    points_col_last = []  # 最后一行的纵坐标 去重后的结果
    # points=[]
    # points.append((1,2))
    # points.append((3,4))
    # points.append((6,5))
    # print(points[1])#(3,4)
    # print(points[1][1])#4
    i_row = 0
    j_col = 0
    # diff_row=50
    for i in range(rows):
        for j in range(cols):
            value = points_pic[i, j]
            if (value == 255):
                all_col.append(j)
                if (abs(i - i_row) >= 30):  # 换行了
                    i_row = i
                    points_row.append(i)

    for i in range(rows):
        for j in range(cols):
            value = points_pic[i, j]
            if (value == 255):
                if (abs(i - points_row[-1]) <= 30):  # 是最后一行
                    all_col_last.append(j)

    # 去重第一行到倒数第二行
    bubbleSort(all_col)  # 冒泡排序
    for i in range(len(all_col)):
        if (i == 0):
            points_col.append(all_col[i])
        else:
            if (abs(all_col[i] - points_col[-1]) >= 15):
                points_col.append(all_col[i])

    # 去重最后一行
    bubbleSort(all_col_last)  # 冒泡排序
    for i in range(len(all_col_last)):
        if (i == 0):
            points_col_last.append(all_col_last[i])
        else:
            if (abs(all_col_last[i] - points_col_last[-1]) >= 15):
                points_col_last.append(all_col_last[i])

    #print('每一行的横坐标')
    #print(len(points_row))
    #print(points_row)
    #print('第一行到倒数第二行的纵坐标')
    #print(len(points_col))
    #print(points_col)
    #print('最后一行的纵坐标')
    #print(len(points_col_last))
    #print(points_col_last)

    diff_points_row = []
    diff_points_col = []
    diff_points_col_last = []
    # plt.subplot(311)
    # plt.title('row')
    # plt.imshow(row_dilated,cmap="gray")         #显示膨胀后的图像

    # plt.subplot(312)
    # plt.title('col')
    # plt.imshow(col_dilated,cmap="gray")         #显示膨胀后的图像

    # plt.subplot(313)
    plt.title('points_pic')
    plt.imshow(points_pic, cmap="gray")  # 显示膨胀后的图像

    # for i in range(len(points_col)):
    #     circles = cv2.cv2.circle(img_gray, (points_col[i],points_row[0]), 20, (0,0,255), 0)
    # for i in range(len(points_col_last)):
    #     circles = cv2.cv2.circle(img_gray, (points_col_last[i],points_row[len(points_row)-1]), 20, (0,0,255), 0)
    # for i in range(len(points_row)):
    #     circles = cv2.cv2.circle(img_gray, (points_col[0],points_row[i]), 20, (0,0,255), 0)

    # plt.title('img_gray')
    # plt.imshow(img_gray)         #显示膨胀后的图像

    # plt.show()

    diff_points_row = []
    diff_points_col = []
    diff_points_col_last = []
    for i in range(len(points_col)):
        diff_points_col.append((points_col[i] - points_col[0]) / (points_col[-1] - points_col[0]))
    for i in range(len(points_col_last)):
        diff_points_col_last.append(
            (points_col_last[i] - points_col_last[0]) / (points_col_last[-1] - points_col_last[0]))
    for i in range(len(points_row)):
        diff_points_row.append((points_row[i] - points_row[0]) / (points_row[-1] - points_row[0]))

    result = {'diff_points_row':diff_points_row,'diff_points_col':diff_points_col,'diff_points_col_last':diff_points_col_last,'rows':len(diff_points_row) ,'columns':len(diff_points_col),'points_row':points_row, 'points_col':points_col,'points_col_last':points_col_last }
    return result


def match(template_row,template_col,template_col_last,test_row,test_col,test_col_last):
    ans = 1  # 最终结果 1表示成功 0表示失败
    k = 0  # row错位标记
    m = 0  # col错位标记
    n = 0  # col_last错位标记
    print(len(template_row) - len(test_row))
    print(len(template_col) - len(test_col))
    if ((len(template_row) - len(test_row)<= 1) and (len(template_col) - len(test_col) <= 1)):
        for i in range(len(test_row)):
            if (template_row[i - k] - test_row[i] > 0.02):
                k = k + 1
                if (k > 1):
                    ans = 0
                    print('row失败')
                    break
        for i in range(len(test_col)):
            if (template_col[i - m] - test_col[i] > 0.02):
                m = m + 1
                if (m > 1):
                    ans = 0
                    print('col失败')
                    break
        for i in range(len(test_col_last)):
            if (template_col_last[i - n] - test_col_last[i] > 0.02):
                n = n + 1
                if (n > 1):
                    ans = 0
                    print('col_last失败')
                    break
    else:
        ans = 0
    return ans

def delete_points(template_row,template_col,template_col_last,test_row,test_col,test_col_last,points_row,points_col,points_col_last):
    ans = 1  # 最终结果 1表示成功 0表示失败
    k = 0  # row错位标记
    m = 0  # col错位标记
    n = 0  # col_last错位标记
    #print(len(template_row) - len(test_row))
    #print(len(template_col) - len(test_col))
    if ((len(template_row) - len(test_row)<= 1) and (len(template_col) - len(test_col) <= 1)):
        for i in range(len(test_row)):
            if (template_row[i - k] - test_row[i] > 0.03):
                del(points_row[i])
                k = k + 1
                if (k > 1):
                    ans = 0
                    print('row失败')
                    break
        for i in range(len(test_col)):
            if (template_col[i - m] - test_col[i] > 0.03):
                del(points_col[i])
                m = m + 1
                if (m > 1):
                    ans = 0
                    print('col失败')
                    break
        for i in range(len(test_col_last)):
            if (template_col_last[i - n] - test_col_last[i] > 0.03):
                del(points_col_last[i])
                n = n + 1
                if (n > 1):
                    ans = 0
                    print('col_last失败')
                    break
    else:
        ans = 0
    result = {'points_row': points_row, 'points_col':points_col, 'points_col_last':points_col_last}
    return result

#recognize("/home/whu-ee/Documents/test/4b1f7808-50b4-11eb-8fa3-3197b768aa9e123.jpg")
