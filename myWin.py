from PyQt5.QtCore import Qt
from PyQt5.Qt import QWidget, QPixmap, QStandardItem, QHeaderView, QStandardItemModel, QFileDialog
from myConvThread import ConvThread
from PIL import Image
from numpy import float64, asarray, array, ndarray
from ui import Ui_Form


class MyWin(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.picture = None
        self.logic_thread = None
        self.init_ui()  # 调用Ui_Form类的函数
        self.init_line_edit()  # 设置显示文件路径的框
        self.init_tableview()  # 设置卷积核显示的表格
        self.init_combobox()  # 设置自动填充卷积核的按钮
        self.init_connect()  # 绑定槽函数
        return


    def init_ui(self)->None: # 画出ui界面
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


    def init_line_edit(self)->None:  # 显示文件路径的框
        self.lineEdit_2.setEnabled(False)
        #   将显示框设置为不可编辑
        return


    def init_tableview(self)->None:  # 设置卷积核显示
        self.tableView.model = QStandardItemModel()
        self.tableView.setModel(self.tableView.model)  # 放任意的类型
        self.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 禁用水平滚动条
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 所有列自动拉伸，充满界面
        for row in range(3):  # 全部初始化成'1'
            for column in range(3):
                item = QStandardItem('1')
                self.tableView.model.setItem(row, column, item)
        return


    def init_combobox(self)->None:  # 设置combobox的显示
        self.comboBox.addItems(['默认', '轮廓', '浮雕', '锐化'])
        return


    def init_connect(self)->None:  # 绑定各个动作的的槽函数
        self.pushButton.clicked.connect(self.click_of_choose_file) #   绑定选择文件按钮槽函数
        self.pushButton_2.clicked.connect(self.click_of_conv) #   绑定卷积按钮槽函数
        self.logic_thread = ConvThread() #    创建了一个子线程的类
        self.logic_thread.my_signal.connect(self.logic_thread.logic_of_request) #   绑定子线程信号
        self.logic_thread.start() #   开始线程
        self.comboBox.currentIndexChanged.connect(self.click_of_choose_kernel) #   绑定选择卷积核按钮
        return


    def click_of_choose_file(self)->None:  # 点击选择文件之后的动作，主要是生成一个选择文件的对话框
        file_type = 'ImagFile(*.png *.jpg *.jpge)' # 可选的文件类型
        file_path, _ = QFileDialog.getOpenFileName(parent = self, caption = 'Choose picture file',
                                                    directory = r'D:\jupyter-workspace\opencv\picture', filter = file_type)
        if file_path is None:
            return
        else:
            img = Image.open(file_path)
            img_channel = asarray(img.convert('RGB')) # 调整通道顺序并转化为array
            self.picture = img_channel #   读取图片的数据
        self.lineEdit_2.setText(file_path) #   显示文件路径在QLineEdit
        pix = QPixmap(file_path)
        self.label_2.setPixmap(pix) #   加载原始图片
        self.label_2.setScaledContents(True) #   自适应label
        return


    def click_of_conv(self)->None:  # 点击卷积按钮之后
        kernel = self.get_kernel()  # 获取卷积核
        self.logic_thread.my_signal.emit([self.picture, kernel], self.label_3)
        # 向正在死循环的子线程发送信息，调用myConvThread.logic_of_request函数
        return


    def click_of_choose_kernel(self)->None:  # 按照选择的内容把对应的卷积核显示出来
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


    def get_kernel(self)->ndarray:  # 点了卷积之后获取显示在表格上的卷积核
        kernel = []  # 卷积核
        for row in range(3):
            new_list = []
            for column in range(3):
                index = self.tableView.model.index(row, column)  # 获得每一个单元格的信息
                new_list.append(float(self.tableView.model.data(index)))
            kernel.append(new_list)
        return array(kernel, float64)  # 转化成numpy.ndarray
