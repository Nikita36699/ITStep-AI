# Завдання 1
# Відкрийте зображення data/lesson3/sonet.png. Проведіть
# бінарізацію.
# Обов’язково використайте:
#  розмиття або наведення різкості
#  адаптивну бінарізацію
#  очищеня шумів
# import cv2
#
#
# img = cv2.imread(r'C:\ITSTEP\ITStep-AI\data\lesson3\sonet.png', cv2.IMREAD_GRAYSCALE)
#
# cv2.imshow('original', img)
#
# # 1. Розмиття
# blur = cv2.GaussianBlur(img, (3,3), 2)
# cv2.imshow('blur', blur)
#
# # 2. Адаптивна бінарізація
# bin_adapt = cv2.adaptiveThreshold(
#     blur,
#     255,
#     cv2.ADAPTIVE_THRESH_MEAN_C,
#     cv2.THRESH_BINARY,
#     7,
#     3
# )
# cv2.imshow('binary_adaptive', bin_adapt)
#
# # 3. Очищення шумів — bilateral
# clean = cv2.bilateralFilter(bin_adapt, d=5, sigmaColor=75, sigmaSpace=75)
# cv2.imshow('cleaned', clean)





# Завдання 2
# Відкрийте зображення data/lesson3/sonnet_noised.png.
# Проведіть бінарізацію. Застосуйте код з завдання 1 та
# спробуйте покращити результат

import cv2


img = cv2.imread(r'C:\ITSTEP\ITStep-AI\data\lesson3\sonet_noised.png', cv2.IMREAD_GRAYSCALE)

cv2.imshow('original', img)


denoise = cv2.bilateralFilter(img, d=5, sigmaColor=75, sigmaSpace=75)
cv2.imshow('denoise', denoise)


blur = cv2.GaussianBlur(denoise, (5,5), 2)
cv2.imshow('blur', blur)


bin_adapt = cv2.adaptiveThreshold(
    blur,
    255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY,
    13,
    3
)
cv2.imshow('binary_adaptive', bin_adapt)

cv2.waitKey(0)
