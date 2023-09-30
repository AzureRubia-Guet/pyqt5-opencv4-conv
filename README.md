# pyqt5-opencv4
## 功能
  用pyqt5和opencv写出来的一个小东西，选择图片和输入卷积核之后输出卷积之后的图片
## 编写过程中的一些事情
    1. 使用的是python 3.9.13
    2. 那个ui.py是把a_test.ui转成py之后，修改一点显示信息得到的
    3. 用pyinstaller打包得到exe，过程中碰上了一些问题，把版本退回4.10得以解决
    4. 本工程使用的环境是anaconda环境，据说使用upx可以减小一点体积（未知，待求证）

## 大致结构
    1. 使用了两个自己写的类，myWin和myConvThread
        1.1 myWin继承了两个类，分别是QWidget和Ui_Form；Ui_Form类是把.ui文件转成.py文件之后得到的
            1.1.1 myWin的各个函数基本上分为两类：对各个控件的初始化以及槽函数的绑定、槽函数实现
        1.2 myConvThread类继承自QThread
            1.2.1 其中run函数是一个死循环，正常情况下会在这个死循环中，啥也不干，单纯活着
            1.2.2 logic_of_request函数则是在接收到主函数的click_of_conv函数发来的消息之后，把发来的图像和卷积核传给位于myOpencv.py的conv函数，然后接收返回的图像，并显示
    2. 主函数很简单，就是创建-显示-循环直到关闭窗口
