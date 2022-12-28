import cv2


def conv(list_of_conv):
    img = list_of_conv[0]  # 图片信息
    kernel = list_of_conv[1]  # 卷积核
    if img is None or kernel is None:
        return None
    dst = cv2.filter2D(img, -1, kernel)  # 卷积操作
    return dst
