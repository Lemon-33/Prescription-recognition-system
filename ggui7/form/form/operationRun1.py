import sys
import time
import random
import cv2
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QPainter, QPen
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QLabel, \
    QHeaderView

#import img_processing
from operation1 import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, event=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.table()
        # self.picture()
        self.buttons()
        self.lb = MyLabel(self)  # 重定义的label
        #self.lb.setGeometry(QRect(30, 50, 2000, 700))
        self.lb.setGeometry(QRect(30, 50, 1500, 500))
        self.lb.setCursor(Qt.CrossCursor)

    def table(self):
        self.tableWidget.setColumnCount(10)
        self.tableWidget.setRowCount(6)
        name = ['药品名称', '药品规格', '单位', '单价', '数量', '总金额', '批号', '有效期', '产地及厂家', '批准文号']
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
        self.tableWidget.setHorizontalHeaderLabels(name)
        self.tableWidget.cellClicked.connect(self.tabfun)  # 绑定标签点击时的信号与槽函数

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

    def buttons(self):
        pix = QPixmap('white.jpg') # 先显示一张白色的图
        self.label_5.setPixmap(pix)
        self.label_5.setScaledContents(True)

        self.pushButton_2.clicked.connect(self.close)
        self.pushButton_6.clicked.connect(self.getPicShow)
        self.pushButton_5.clicked.connect(self.wipeData)

    def getPicShow(self):
        self.name = self.lineEdit.text()  # 获取文本框内容
        print(self.name)
        pix = QPixmap(self.name)  # 显示图片
        self.label_5.setPixmap(pix)
        self.label_5.setScaledContents(True)
        self.lineEdit_2.setText('2020/07/01')
        self.lineEdit_3.setText('上药控股安徽有限公司')

    def wipeData(self):
        self.tableWidget.clearContents()


class MyLabel(QLabel):
    x0 = 0
    y0 = 0
    x1 = 0
    y1 = 0
    flag = False

    # 鼠标点击事件
    def mousePressEvent(self, event):
        self.flag = True
        self.x0 = event.x()
        self.y0 = event.y()

    # 鼠标释放事件
    def mouseReleaseEvent(self, event):
        self.flag = False

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
