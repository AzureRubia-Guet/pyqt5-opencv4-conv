import os
import win32ui
import win32con
from PyQt5.QtCore import Qt
from PyQt5.Qt import QWidget, QPixmap, QStandardItem, QHeaderView, QStandardItemModel
from ConvThread import ConvThread
import cv2
import numpy
from ui import Ui_Form


class MyWin(QWidget, Ui_Form):
    def __init__(self):  # 把各种东西初始化
        super().__init__()
        self.picture = None
        self.logic_thread = None
        self.init_ui()
        self.init_line_edit()
        self.init_tableview()
        self.init_combobox()
        self.init_connect()
        return

    def init_ui(self): # 画出ui界面
        self.setupUi(self)
        self.retranslateUi(self)
        #   选择文件按钮：self.pushButton
        #   显示文件路径的框：self.lineEdit_2
        #   选择卷积核的按钮：self.comboBox
        #   显示原始图片的框：self.label_2
        #   显示卷积后图片的框：self.label_3
        #   显示卷积核的框：self.tableView
        #   图像卷积按钮：self.pushButton_2
        return

    def init_line_edit(self):  # 显示文件路径的框
        self.lineEdit_2.setEnabled(False)
        #   将显示框设置为不可编辑
        return

    def init_tableview(self):  # 设置卷积核显示
        self.tableView.model = QStandardItemModel()
        self.tableView.setModel(self.tableView.model)  # 放任意的类型
        self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        for row in range(3):  # 全部初始化成'1'
            for column in range(3):
                item = QStandardItem('1')
                self.tableView.model.setItem(row, column, item)
        return

    def init_combobox(self):  # 设置combobox的显示
        self.comboBox.addItems(['默认', '轮廓', '浮雕', '锐化'])
        return

    def init_connect(self):  # 绑定各个动作的的槽函数
        self.pushButton.clicked.connect(self.click_of_choose_file)
        #   绑定选择文件按钮槽函数
        self.pushButton_2.clicked.connect(self.click_of_conv)
        #   绑定卷积按钮槽函数
        self.logic_thread = ConvThread()
        self.logic_thread.my_signal.connect(self.logic_thread.logic_of_request)
        #   绑定子线程信号
        self.logic_thread.start()
        #   开始线程
        self.comboBox.currentIndexChanged.connect(self.click_of_choose_kernel)
        #   绑定选择卷积核
        return

    def click_of_choose_file(self):  # 点击选择文件之后的动作，主要是生成一个选择文件的对话框
        default_name = ''
        # 默认输入文件名 (一般 "保存/另存为" 为文件名加后缀, "打开" 为空字符串)
        file_type = '|*.png;*.jpg|'
        # 可选的文件类型
        api_flag = win32con.OFN_OVERWRITEPROMPT | win32con.OFN_FILEMUSTEXIST
        dlg = win32ui.CreateFileDialog(True, None, default_name, api_flag, file_type)
        # true为打开,false为保存
        dlg.SetOFNTitle("选择您的图片文件")
        # "SetOFNTitle()": 设置标题
        #  dlg.SetOFNInitialDir(os.path.abspath(__file__))
        # "SetOFNInitialDir()": 设置默认路径(需绝对路径) ("os.path.abspath()" 获取绝对路径)
        dlg.DoModal()
        # "DoModal()": 开始运行对话框, 阻滞程序
        filename = dlg.GetPathName()
        if filename is None:
            return
        self.picture = cv2.imdecode(numpy.fromfile(filename, dtype=numpy.uint8), -1)
        #   读取图片的数据,cv2.imread不能支持中文路径名
        if self.picture is None:
            return
        self.picture = cv2.cvtColor(self.picture, cv2.COLOR_BGR2RGB)
        #   将颜色通道转化成正常的情况下
        self.lineEdit_2.setText(filename)
        #   显示文件路径在QLineEdit
        pix = QPixmap(filename)
        self.label_2.setPixmap(pix)
        #   加载原始图片
        self.label_2.setScaledContents(True)
        #   自适应label
        return

    def click_of_conv(self):  # 点击卷积按钮之后
        kernel = self.get_kernel()
        if kernel is None or self.picture is None:
            return
        self.logic_thread.my_signal.emit([self.picture, kernel], self.label_3)
        return

    def click_of_choose_kernel(self):
        sharpen = [[0, -1, 0], [-1, 5, -1], [0, -1, 0]]  # 锐化核
        relief = [[-2, 1, 0], [-1, 1, 1], [0, 1, 2]]  # 浮雕核
        outline = [[-1, -1, -1, ], [-1, 8, -1], [-1, -1, -1]]  # 轮廓核
        default = [[1, 1, 1], [1, 1, 1], [1, 1, 1]]  # 默认
        now_select = self.comboBox.currentText()  # 自动填充的选项
        if now_select == '锐化':
            for row in range(3):
                for column in range(3):
                    item = QStandardItem(str(sharpen[row][column]))
                    self.tableView.model.setItem(row, column, item)
        if now_select == '浮雕':
            for row in range(3):
                for column in range(3):
                    item = QStandardItem(str(relief[row][column]))
                    self.tableView.model.setItem(row, column, item)
        if now_select == '轮廓':
            for row in range(3):
                for column in range(3):
                    item = QStandardItem(str(outline[row][column]))
                    self.tableView.model.setItem(row, column, item)
        if now_select == '默认':
            for row in range(3):
                for column in range(3):
                    item = QStandardItem(str(default[row][column]))
                    self.tableView.model.setItem(row, column, item)
        return

    def get_kernel(self):
        kernel = []  # 卷积核
        for row in range(3):
            new_list = []
            for column in range(3):
                index = self.tableView.model.index(row, column)  # 获得每一个单元格的信息
                new_list.append(float(self.tableView.model.data(index)))
            kernel.append(new_list)
        return numpy.array(kernel, numpy.float64)  # 转化成numpy.array
