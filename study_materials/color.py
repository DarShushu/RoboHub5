import cv2 as cv

from hsv_color_picker import SliderHSV


color_slider = SliderHSV("HSV slider", normalized_display=True)
while True:
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break