import cv2
import numpy as np


img = cv2.imread('C:\ITSTEP\ITStep-AI\data\lesson2\darken.png')
img = cv2.resize(img, (500, 500))

cv2.imshow('original', img)


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)


value = hsv[:, :, 2]

value_eq = cv2.equalizeHist(value)


hsv1 = hsv.copy()
hsv1[:, :, 2] = value_eq

result_eq = cv2.cvtColor(hsv1, cv2.COLOR_HSV2BGR)
cv2.imshow('equalized', result_eq)


value2 = value.astype(np.float32)
value2 = value2 * 1.4       # +40%

value2 = np.clip(value2, 0, 255)
value2 = value2.astype(np.uint8)


hsv2 = hsv.copy()
hsv2[:, :, 2] = value2

result_bright = cv2.cvtColor(hsv2, cv2.COLOR_HSV2BGR)
cv2.imshow('brightened', result_bright)

cv2.waitKey(0)
