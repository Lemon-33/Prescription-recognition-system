import os
import fitz
import numpy as np
import pickle
import json
import time
import random
import cv2

from start import Ui_MainWindow
from choose import Ui_choose
from register1 import Ui_register
from operation1 import Ui_medrecog
import process

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import sys
import requests
import tkinter
import tkinter.messagebox

# url of server
url = 'http://192.168.31.162:7000/'
uname=''
token = ''
id_img=''


# 登录界面
class uistart(QMainWindow, Ui_MainWindow):
  def __init__(self):
    super(uistart,self).__init__()
    self.setupUi(self)
    self.pushButton.clicked.connect(self.choose_clicked)
    self.pushButton_2.clicked.connect(self.register_clicked)

  # 登录按钮
  def choose_clicked(self):
    global uname
    global token
    # 获取用户名、密码
    uname=self.lineEdit.text()
    pwd=self.lineEdit_2.text()
    # 将用户名密码传送给后端
    data1={'uname':uname,'pwd':pwd}
    login_r = requests.post(url + 'login', data=data1)
    login_text=login_r.text
    r_cut=''
    token=''

    if (len(login_text)>10):
        # 获取前面的几个字符串
        for index1 in range(0, 10):
            r_cut = r_cut + login_text[index1]
        # print(r_cut)

        # 获取token
        for index2 in range(10, len(login_text)):
            token = token + login_text[index2]
        # print(token)
    # 根据后端的返回值做出不同的操作
    # 成功
    if(r_cut=='successful'):
      uichoose.show()
      self.close()
    # 密码错误
    elif (login_r.text == 'Password mistake'):
      self.label_3.setText('密码错误')
    # 数据库错误
    elif(login_r.text=='mysql mistake'):
      self.label_3.setText('数据库错误')
    elif(login_r.text=='No_user'):
      self.label_3.setText('没有该用户')
      
  # 注册按钮
  def register_clicked(self):
    uiregister.show()
    self.close()


# 选择界面
class uichoose(QDialog, Ui_choose):
  def __init__(self):
    super(uichoose,self).__init__()
    self.setupUi(self)     
    self.setWindowTitle('choose window')
    self.pushButton.clicked.connect(self.medicine_clicked)

  # 药库单选择按钮
  def medicine_clicked(self):
    uirecog.show()
    self.close()


# 注册界面
class uiregister(QDialog,Ui_register):
  def __init__(self):
    super(uiregister,self).__init__()
    self.setupUi(self)     
    self.setWindowTitle('register window')
    self.pushButton.clicked.connect(self.regclicked)

  def regclicked(self):
    # 获取用户名、密码
    uname=self.lineEdit.text()
    pasw1=self.lineEdit_2.text()
    pasw2=self.lineEdit_3.text()
    # print('0')

    if(pasw1==pasw2):
      pwd=pasw1
      data2={'uname':uname,'pwd':pwd}
      print('密码一致')
      register_r=requests.post(url + 'register', data=data2)
      # 根据后端的不同返回值有不同的操作
      # 成功
      print(register_r.text)
      if(register_r.text=='successful'):
        uistart.show()
        self.close()
      # 重名
      elif(register_r.text=='Failed_name'):
        self.label_4.setText('重名')
      # 注册失败
      elif(register_r.text=='ACCOUNT_REGISTER_FAILED'):
        self.label_4.setText('注册失败')
    else:
      self.label_4.setText('密码错误')
      

# 用户操作界面
class uirecog(QMainWindow, Ui_medrecog):
    def __init__(self, parent=None, event=None):
        super(uirecog, self).__init__(parent)
        self.setupUi(self)
        self.table()
        # self.picture()
        self.buttons()
        self.lb = MyLabel(self)  # 重定义的label
        # self.lb.setGeometry(QRect(30, 50, 2000, 700))
        self.lb.setGeometry(QRect(10, 50, 1180, 400))
        self.lb.setCursor(Qt.CrossCursor)
        file_handle = open('data.txt', mode='a+')
        file_handle.seek(0)
        file_handle.truncate()

    def table(self):
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(5)
        # name = ['药品名称', '药品规格', '单位', '单价', '数量', '总金额', '批号', '有效期', '产地及厂家', '批准文号']
        # for j in range(0, len(name)):
        #     self.tableWidget.setItem(0, j, QTableWidgetItem(name[j]))
        # item1 = ['卡托普利片（异形）', '75mg*100s', '瓶', '20.8000', '100', '2080.00', '20031012', '2022/03/0', '常州制药厂有限公司', '国药准字H32023731', '2020/07/01', '上药控股安徽有限公司']
        # for j in range(0, len(item1) - 1):
        #     self.tableWidget.setItem(1, j, QTableWidgetItem(item1[j]))
        # item2 = ['格列吡嗪控释片', '5mg*7s*3板/盒', '盒', '26.2600', '200', '5250.00', '21911111', '2022/03/0', '北京红林制药有限公司',
        #          '国药准字H32023731', '2020/07/01', '上药控股安徽有限公司']
        # for j in range(0, len(item2) - 1):
        #     self.tableWidget.setItem(2, j, QTableWidgetItem(item2[j]))
        # item3 = ['卡丙戊酸钠片', '0.2g*100s', '瓶', '20.8000', '100', '2080.00', '20031012', '2022/03/0', '湖南湘中制药有限公司',
        #          '国药准字H32023731', '2020/07/01', '上药控股安徽有限公司']
        # for j in range(0, len(item3) - 1):
        #     self.tableWidget.setItem(3, j, QTableWidgetItem(item3[j]))
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        # self.tableWidget.setColumnWidth(0, 80)
        # minimumSectionSize = self.tableWidget.horizontalHeader().minimumSectionSize()
        # self.tableWidget.setRowHeight(0, minimumSectionSize)
        # self.tableWidget.setRowHeight(1, minimumSectionSize)
        # self.tableWidget.setRowHeight(2, minimumSectionSize)
        # self.tableWidget.horizontalHeader().setVisible(False)  # 隐藏水平表头
        # self.tableWidget.setHorizontalHeaderLabels(name)
        # self.tableWidget.cellClicked.connect(self.tabfun)  # 绑定标签点击时的信号与槽函数

    def tabfun(self, x, y):
        t = random.uniform(0.5, 1.5)
        time.sleep(t)  # 休眠1秒
        items = [['卡托普利片（异形）', '75mg*100s', '瓶', '20.8000', '100', '2080.00', '20031012', '2022/03/09', '常州制药厂有限公司', '国药准字H32023731'],
                 ['格列吡嗪控释片', '5mg*7s*3板/盒', '盒', '26.2600', '200', '5250.00', '21911111', '2021/10/31', '北京红林制药有限公司', '国药准字H20084634'],
                 ['卡丙戊酸钠片', '0.2g*100s', '瓶', '17.3000', '100', '1730.00', '1H200406', '2022/09/30', '湖南湘中制药有限公司', '国药准字H430200874'],
                 ['溴米那普鲁卡因注射液（爱茂尔）', '2ml:2mg*10支', '盒', '8.4000', '20', '168.00', '20011082', '2022/01/09', '山东方明药业集团股份有限公司', '国药准字H37023895'],
                 ['盐酸利多卡因注射液', '5ml:0.1g*5支/盒', '盒', '9.98000', '240', '2395.20', '2001092D1', '2021/12/31', '郑州卓峰制药2有限公司', '国药准字H20044283']
                ]
        print(x, y)
        newItem = QTableWidgetItem(items[x][y])

        self.tableWidget.setItem(x, y, newItem)
        newItem.setTextAlignment(Qt.AlignHCenter|Qt.AlignVCenter)

    # 各按钮关联关系
    def buttons(self):
        pix = QPixmap('white.jpg') # 先显示一张白色的图
        self.label_5.setPixmap(pix)
        self.label_5.setScaledContents(True)
        # 2 完成 3 返回 4 保存 5 清空 6 打开 7 确认
        self.pushButton_7.clicked.connect(self.finish_bnt)  # 点击完成
        self.pushButton_6.clicked.connect(self.getPicShow)  # 点击打开
        self.pushButton_5.clicked.connect(self.wipeData)  # 点击清空
        self.pushButton_4.clicked.connect(self.readTxt)
        self.pushButton_3.clicked.connect(self.backpage)
        self.pushButton_2.clicked.connect(self.close)  # 点击完成

    def backpage(self):
        uistart.show()
        self.close()

    def close(self):
        self.close()

    # “打开”按钮
    def getPicShow(self):
      global uname
      global token
      global id_img
      global img_format

      imgType=''
      # 获取图片
      imgName = self.lineEdit.text() # 获取文本框内容
      if imgName == '':
        imgName,imgType=QFileDialog.getOpenFileName(self,"打开图片","","*.jpg;;*.png;;All Files(*)")     
      self.lineEdit.setText(str(imgName))
      print(str(imgName))


      # 图片预处理
      # print(imgName)
      process_img=process.main(imgName)
      cv2.imwrite('heibai.jpg',process_img)
      # print(process_img)
     



      # 显示图片
      # pix = QPixmap('heibai.jpg')
      pix = QPixmap('11.jpg')
      self.label_5.setPixmap(pix)
      self.label_5.setScaledContents(True)
      # self.lineEdit_2.setText('2020/07/01')
      # self.lineEdit_3.setText('上药控股安徽有限公司')



      # 发送图片
      form_type=0
      img_format=''
      for index3 in range(1,len(imgType)):
        img_format=img_format+imgType[index3]

      # file_send = open('heibai.jpg', 'rb')
      file_send = open('11.jpg', 'rb')
      files = {'file_send': file_send}
      file_info = {'uname':uname,'form_type':form_type,'img_format':img_format,'token':token}
      uploadfiles_r = requests.post(url + 'uploadfiles',data=file_info,files=files)
      uploadfiles_text=uploadfiles_r.text
      print(uploadfiles_text)


      up_cut=''
      id_img=''

      if (len(uploadfiles_text)>10):
          # 获取前面的几个字符串
          for index3 in range(0, 13):
              up_cut = up_cut + uploadfiles_text[index3]
          print(up_cut)

          # 获取id_img
          for index4 in range(13, len(uploadfiles_text)):
              id_img = id_img + uploadfiles_text[index4]
          print(id_img)
      # print("1")


      # 根据后端的不同回应做出响应
      if(uploadfiles_text=='Login_failure'):
        uistart.show()
        self.close()
        QMessageBox.information(QtWidgets.QWidget(), '信息提示对话框', '登录失效', QMessageBox.Yes)
      elif(up_cut=='Module_failed'):
        QMessageBox.information(QtWidgets.QWidget(), '信息提示对话框', '没有模板', QMessageBox.Yes)

      else:
          # 转换数据类型
          return_ocr = []
          for i in range(1, 69):
              stringText = "\"" + str(i) + "\"" + ":" + " " + "\""
              endText = "\""
              return_ocr.append(self.stringEditor_TakeFirstRequiredTextFromString(uploadfiles_text, stringText, endText))
          print(return_ocr)

          tital = ['xvhao', 'yaopinmingcheng', 'yaoqinguige', 'danwei', 'shangshixvkechiyouren', 'shuliang',
                   'danjia', 'jine', 'pihao', 'youxiaoqizhi', 'pizhunwenhao']
          tital1 = ['药品名称', '药品规格', '单位', '上市许可持有人（含生产厂家）', '数量', '单价', '金额', '批号', '有效期至', '批准文号']
          self.tableWidget.setHorizontalHeaderLabels(tital1)

          for i in range(1, 6):
              for j in range(1, 11):
                  start = tital[j] + "|"
                  ori_str = return_ocr[i * 11 + j]
                  item = self.stringEditor_TakeFirstRequiredTextFromString_2(ori_str, start)
                  self.tableWidget.setItem(i-1, j-1, QTableWidgetItem(item))


      # 显示文字

        
      
    #“清空”按钮
    def wipeData(self):
        self.tableWidget.clearContents()

    def convertIntoString(self,uname, c1, length, width, PicureID, img_format, coordinateAmount, key, Coordinate1,Coordinate2):
        string = '{"uname":"' + str(uname) + '","c1":"' + str(c1) + '","length":' + str(length) + ',"width":' + str(width) + ',"PictureID":"' + str(PicureID) + '","img_format":"' + str(img_format) + '","coordinateAmount":' + str(coordinateAmount) + ','
        i = 0
        while (i < coordinateAmount):
            if i < coordinateAmount - 1:
                string = string + '"order":' + str(i+1)+ ',"key":"' + str(key[i]) + '","Coordinate1":"' + str(Coordinate1[i]) + '","Coordinate2":"' + str(Coordinate2[i] )+ '",'
            else:
                string = string + '"order":' + str(i+1) + ',"key":"' +str(key[i]) + '","Coordinate1":"' + str(Coordinate1[i]) + '","Coordinate2":"' + str(Coordinate2[i]) + '"}'
            i=i+1
        return string

    # 点击"保存"按钮
    # 将框线发送给服务器，并从服务器获取数据显示在表格中
    def readTxt(self):
        global uname
        global id_img
        global img_format
        # 框选方法
        # 先横着向右框选，再竖着向下框选(请勿重复框选)，最后框底部横条框
        # 目前只适用于自制表格
        # 返回类型
        # list
        # {顶点坐标}
        # [{（长，宽）},
        # {序号，关键字（使用拼音），左上坐标，右下坐标},
        # {序号，关键字（last1），左上坐标，右下坐标},
        # {序号，关键字（last2），左上坐标，右下坐标}]
        data = np.loadtxt('data.txt', dtype=int)

        # 把坐标转化为1800*1350
        data_ori = []
        for i in range(0, len(data), 2):
            data_ori.append((data[i] / 1180) * 1800)
            data_ori.append((data[i + 1] / 400) * 1350)

        data = data_ori

        # 寻找左上角角点
        x0 = data[0]
        y0 = data[1]
        print(len(data))
        for i in range(1, len(data)):
            if abs(data[i] - x0) < 7:
                turn_index = i
                break

        x_max = data[turn_index - 2] - x0  # 横轴Max
        y_max = int((data[len(data) - 5] + data[len(data) - 1]) / 2) - y0  # 纵轴Max
        ratio = round(x_max / y_max, 6)

        data_abs = []
        keywords0 = ['序号', '药品名称', '药品规格', '单位', '上市许可持有人（含生产厂家）', '数量', '单价', '金额', '批号', '有效期至', '批准文号', '11',
                     '12', '13', '14', '15', 'last1', 'last2']
        keywords = ['xvhao', 'yaopinmingcheng', 'yaoqinguige', 'danwei', 'shangshixvkechiyouren', 'shuliang',
                    'danjia', 'jine', 'pihao', 'youxiaoqizhi', 'pizhunwenhao', '11', '12', '13', '14', '15',
                    'lastContent', 'lastContent']
        for i in range(0, len(data), 2):
            data_abs.append(round(((data[i] - x0) / x_max), 6))
            data_abs.append(round(((data[i + 1] - y0) / y_max), 6))

        # 按格式输出
        c1 = [data[0], data[1]]
        length = x_max
        width = y_max
        amount = len(data_abs) // 4
        upleft = []
        downright = []

        for i in range(0, len(data_abs), 4):
            upleft.append(str(data_abs[i]) + "," + str(data_abs[i + 1]))
            downright.append(str(data_abs[i + 2]) + "," + str(data_abs[i + 3]))

            # lists = [j+1, keywords[j], (data_abs[i], data_abs[i+1]), (data_abs[i+2], data_abs[i+3])]
            # returnlist.append(lists)
        # print(uname)
        # print(id_img)
        # print(img_format)
        teststr = self.convertIntoString(uname, c1, length, width, id_img, img_format, amount, keywords, upleft,
                                         downright)

        print(teststr)

        json1 = {'json': teststr}
        r = requests.post(url + 'save', data=json1)
        print(r.text)


        # 转换数据类型
        return_ocr = []
        for i in range(1, 69):
            stringText = "\'" + str(i) + "\'" + ":" + " " + "\'"
            endText = "\'"
            return_ocr.append(self.stringEditor_TakeFirstRequiredTextFromString(r.text, stringText, endText))

        tital = ['xvhao', 'yaopinmingcheng', 'yaoqinguige', 'danwei', 'shangshixvkechiyouren', 'shuliang',
                    'danjia', 'jine', 'pihao', 'youxiaoqizhi', 'pizhunwenhao']
        tital1 = ['序号', '药品名称', '药品规格', '单位', '上市许可持有人（含生产厂家）', '数量', '单价', '金额', '批号', '有效期至', '批准文号']
        self.tableWidget.setHorizontalHeaderLabels(tital1)

        for i in range(1, 6):
            for j in range(1, 11):
                start = tital[j] + "|"
                ori_str = return_ocr[i * 11 + j]
                item = self.stringEditor_TakeFirstRequiredTextFromString_2(ori_str, start)
                self.tableWidget.setItem(i - 1, j - 1, QTableWidgetItem(item))

    # “完成”按钮
    def finish_bnt(self):
        global uname
        global id_img
        ocr_result=self.get_label_data()
        print('ocr_rsult is')
        print(ocr_result)
        finish_str = {"uname": uname, "PictureID": id_img, "ocr_result": ocr_result}
        finish_r = requests.post(url + 'finish', data=finish_str)
        # print(finish_r.text)

        #根据后端的结果的不同响应
        if(finish_r.text=='mysql mistake'):
            QMessageBox.information(QtWidgets.QWidget(), '信息提示对话框', '数据库未连接成功', QMessageBox.Yes)
        elif(finish_r.text=='Save_success'):
            QMessageBox.information(QtWidgets.QWidget(), '信息提示对话框', '识别结果保存成功', QMessageBox.Yes)



    # 获取表格内容
    # 每个读取的内容后面跟着$ (空格）以区分每个内容
    def get_label_data(self):
        correct = ''
        for i in range(0, 5):
            for j in range(0, 10):
                correct = correct + str(self.tableWidget.item(i, j).text())+'$ '
        # print(correct)
        # print('142')
        return correct

    def stringEditor_TakeFirstRequiredTextFromString(self, stringText, startText, endText):
        startIndex = stringText.find(startText, 0, len(stringText))
        if startIndex == -1:
            return ''
        stringText = stringText[startIndex+len(startText):]
        endIndex = stringText.find(endText, 0, len(stringText))
        if endIndex == -1:
            return ''
        a = stringText[0:endIndex]
        return a

    def stringEditor_TakeFirstRequiredTextFromString_2(self, stringText, startText):
        startIndex = stringText.find(startText, 0, len(stringText))
        if startIndex == -1:
            return ''
        stringText = stringText[startIndex+len(startText):]
        a = stringText[0:]
        return a








class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False
    point = []

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()
        global xx0
        global yy0
        xx0 = self.x0
        yy0 = self.y0
        result1txt = str(xx0)
        result2txt = str(yy0)
        file_handle = open('data.txt', mode='a+')
        file_handle.write(result1txt)  # 写入
        file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据
        file_handle.write(result2txt)  # 写入
        file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False
        self.x2 = event.x()
        self.y2 = event.y()
        global xx2
        global yy2
        xx2 = self.x2
        yy2 = self.y2
        result1txt = str(xx2)
        result2txt = str(yy2)
        file_handle = open('data.txt', mode='a+')
        file_handle.write(result1txt)  # 写入
        file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据
        file_handle.write(result2txt)  # 写入
        file_handle.write('\n')  # 有时放在循环里面需要自动转行，不然会覆盖上一条数据

    # 鼠标移动事件
    def mouseMoveEvent(self, event):
        if self.flag:
            self.x1 = event.x()
            self.y1 = event.y()
            self.update()

    # 绘制事件
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = QRect(self.x0, self.y0, abs(self.x1-self.x0), abs(self.y1-self.y0))
        painter = QPainter(self)
        painter.setPen(QPen(Qt.red, 4, Qt.SolidLine))
        painter.drawRect(rect)
      
      
  
 
if __name__ == '__main__':
  QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
  app = QApplication(sys.argv)
  uichoose = uichoose()
  uistart=uistart()
  uiregister=uiregister()
  uirecog=uirecog()
  uistart.show()
  sys.exit(app.exec_())
