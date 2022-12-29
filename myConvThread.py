import time
from PyQt5.Qt import QThread, pyqtSignal, QImage, QPixmap, QLabel
from myOpencv import conv


class ConvThread(QThread):
    my_signal = pyqtSignal(list, QLabel)  # 接收主函数的消息
    # list[0]是图像，list[1]是卷积核

    def __init__(self):
        super().__init__()
        return

    def logic_of_request(self, list_of_conv, show_after_conv):  # 在接收到主函数的消息之后这个函数开始工作
        dst = conv(list_of_conv)
        # 调用卷积的函数，把卷积的结果传回来
        if dst is None:
            return
        label_width = show_after_conv.width()
        label_height = show_after_conv.height()
        # 将图片转换为QImage
        temp_img_src = QImage(dst, dst.shape[1], dst.shape[0], dst.shape[1] * 3, QImage.Format_RGB888)
        # 将图片转换为QPixmap方便显示
        pixmap_img_src = QPixmap.fromImage(temp_img_src).scaled(label_width, label_height)
        show_after_conv.setPixmap(pixmap_img_src)
        # 显示图片
        show_after_conv.setScaledContents(True)
        # 自适应显示
        return

    def run(self):  # 正常情况下死循环
        while True:
            time.sleep(0.5)
