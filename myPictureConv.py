from cv2 import filter2D
from numpy import ndarray

def conv(list_of_conv:ndarray)->ndarray:
    img = list_of_conv[0]  # 图片信息
    kernel = list_of_conv[1]  # 卷积核
    if img is None or kernel is None:
        return None
    dst = filter2D(img, -1, kernel)  # 卷积操作
    return dst