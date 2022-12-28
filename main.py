import sys
from MyWin import MyWin
from PyQt5.Qt import QApplication


if __name__ == "__main__":
    app = QApplication(sys.argv)
    my_show = MyWin()
    my_show.show()
    sys.exit(app.exec())
