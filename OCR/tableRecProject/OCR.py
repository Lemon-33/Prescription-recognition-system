import pytesseract
import cv2
from PIL import Image
from urllib import request
import time
import os
import difflib
import json


class CoordinateCoupleInformation:
    order = int  # 顺序
    key = str  # 关键字
    coordinate1 = str  # 坐标1
    coordinate2 = str  # 坐标2

    def __init__(self, order, key, coordinate1, coordinate2):
        self.order = order
        self.key = key
        self.coordinate1 = coordinate1
        self.coordinate2 = coordinate2


class ModuleInformation:  # 整个模板信息
    CoordinateCoupleInfoList = list

    def __init__(self):
        self.CoordinateCoupleInfoList = []


def getFileName(file_dir):
    for root, dirs, fileNames in os.walk(file_dir):
        return fileNames


def adjustFileName(fileName):
    fileName = fileName.replace(" ", "")
    fileName = fileName.replace(".PNG", "")
    fileName = fileName.replace(".png", "")
    fileName = fileName.replace(".JPG", "")
    fileName = fileName.replace(".jpg", "")
    fileName = fileName.replace("（", "(")
    fileName = fileName.replace("）", ")")
    fileName = fileName.replace("：", ":")
    return fileName


def adjustOCRResult(result):
    result = result.replace("\n", "")
    result = result.replace(" ", "")
    result = result.replace("", "")
    return result


def getStringSimilar(s1, s2):
    return difflib.SequenceMatcher(None, s1, s2).quick_ratio()


def stringEditor_TakeFirstRequiredTextFromString(stringText, startText, endText):
    startIndex = stringText.find(startText, 0, len(stringText))
    if startIndex == -1:
        return ''
    stringText = stringText[startIndex:]
    endIndex = stringText.find(endText, 0, len(stringText))
    if endIndex == -1:
        return ''
    return stringText[len(startText):endIndex]


def convertPictureToText(folderRoute, folderName, column, row, moduleJson):
    #  处理文件夹内文件
    print('----------OCR-PART-----------')
    os.system('chmod 777 ' + folderRoute + folderName)
    fileNames = getFileName(folderRoute + folderName)
    fileNames.sort()
    fileNum = len(fileNames)
    output = {}
    keyword = []
    print(moduleJson)
    print('----------GET-KEY-----------')
    for i in range(column + 1):
        if i == 0:
            continue
        keyword.append(stringEditor_TakeFirstRequiredTextFromString(moduleJson, '"order": ' + str(i) + ', "key": "',
                                                                    '", "coordinate1"'))
    for i in range(fileNum):
        #  读取图片文件
        image = Image.open(folderRoute + folderName + "/" + fileNames[i])
        #  OCR获取识别结果
        text = pytesseract.image_to_string(image, lang='chi_sim+eng')
        #  优化识别结果
        text = adjustOCRResult(text)
        fileNames[i] = adjustFileName(fileNames[i])
        #  判断行列
        order = int(fileNames[i])
        print('------order' + str(order) + '-------')
        row_ = int(order / column) + 1
        print('row:' + str(row_))
        column_ = order % column
        if column_ == 0:
            column_ = column
        print('column:' + str(column_))
        #  获取关键字
        if (row_ == row):
            output[fileNames[i]] = text
        else:
            text = keyword[column_ - 1] + "|" + text
            output[fileNames[i]] = text
    print(output)
    return output
