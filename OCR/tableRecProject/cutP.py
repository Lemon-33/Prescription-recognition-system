import cv2
import math
import numpy as np
import pylab as plt
import copy
import os
from PIL import Image

from skimage import morphology


# 单个裁图
# def cutP(img1,shape_0, shape_1,shape_2,xup,yup,xdown,ydown):# xup yup是左上角的  xdown,ydown是右下角的
#     img2 = np.frombuffer(img1, np.uint8)
#     img = np.reshape(img2, (shape_0, shape_1, shape_2))
#     cropped = img[yup:ydown,xup:xdown]  # 裁剪坐标为[y0:y1, x0:x1]
#     return cropped
def cutP(img, xup, yup, xdown, ydown):  # xup yup是左上角的  xdown,ydown是右下角的
    cropped = img[yup:ydown, xup:xdown]  # 裁剪坐标为[y0:y1, x0:x1]
    return cropped


# 单个图片保存到本地
def saveP(img, num, uID):
    # cv2.imwrite("/home/whu-ee/Documents/test/"+str(num)+".jpg",img)
    cut_route = "/home/whu-ee/Documents/"
    foldername = uID
    dic = {'cut_route': cut_route, 'foldername': foldername}
    print('-------------------------------------')
    print(cut_route + foldername + '/' + str(num) + ".jpg")
    cv2.imwrite(cut_route + foldername + '/' + str(num) + ".jpg", img)
    return dic
    # cv2.imwrite("D:/syn/cut_test/"+str(num)+".jpg",img)


# 裁剪图片
def cutALL(img_route, points_row, points_col, points_col_last, uID):
    cut_route = "/home/whu-ee/Documents/"
    foldername = uID
    os.mkdir(cut_route + foldername)

    print('-------------------------------------')
    print(points_row)
    print(type(points_row))
    print(points_col)
    print(points_col_last)
    print(img_route)
    img = cv2.imread(img_route)
    print(img)

    for i in range(len(points_row) - 1):
        print(i)
        if i != (len(points_row) - 2):
            for j in range(len(points_col) - 1):
                # 前几行 单个裁图
                print(points_col[j])
                ans = cutP(img, points_col[j], points_row[i], points_col[j + 1],
                           points_row[i + 1])  # xup yup是左上角的  xdown,ydown是右下角的
                num = i * (len(points_col) - 1) + j + 1
                dic = saveP(ans, num, uID)
        else:
            for n in range(len(points_col_last) - 1):
                # 最后一行 单个截图
                ans = cutP(img, points_col_last[n], points_row[i], points_col_last[n + 1],
                           points_row[i + 1])  # xup yup是左上角的  xdown,ydown是右下角的
                num = i * (len(points_col) - 1) + n + 1
                dic = saveP(ans, num, uID)
    print(dic)
    return dic

# img = cv2.imread("./data/cut/thor.jpg")
# print(img.shape)
# cropped = img[0:128, 0:512]  # 裁剪坐标为[y0:y1, x0:x1]
# cv2.imwrite("./data/cut/cv_cut_thor.jpg", cropped)

# pts1 = np.float32([[xpoint[0], ypoint[0]], [xpoint[1], ypoint[1]], [xpoint[2], ypoint[2]], [xpoint[3], ypoint[3]]])
# pts2 = np.float32([[0, 0], [2900, 0], [0, 900], [2900, 900]])
# M = cv2.getPerspectiveTransform(pts1, pts2)
# dst = (img, M, (2900, 900))
# cv2.imwrite('perspective.jpg',dst)
