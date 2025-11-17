import cv2
import numpy as np


img = cv2.imread('C:\ITSTEP\ITStep-AI\data\lesson1\Lenna.png')
if img is None:
    raise ValueError("Lenna.png не знайдено. Перевір шлях.")


mask1 = cv2.imread('C:\ITSTEP\ITStep-AI\data\lesson1\mask1.png', cv2.IMREAD_GRAYSCALE)
mask2 = cv2.imread('C:\ITSTEP\ITStep-AI\data\lesson1\mask2.png', cv2.IMREAD_GRAYSCALE)

if mask1 is None or mask2 is None:
    raise ValueError("mask1.png або mask2.png не знайдено.")

mask1 = mask1 > 0
mask2 = mask2 > 0


mask_or = mask1 | mask2
mask_and = mask1 & mask2


result1 = img.copy()
result1[:] = 0
result1[mask1] = img[mask1]


result2 = img.copy()
result2[:] = 0
result2[mask2] = img[mask2]


result_and = img.copy()
result_and[:] = 0
result_and[mask_and] = img[mask_and]


result_or = img.copy()
result_or[:] = 0
result_or[mask_or] = img[mask_or]


cv2.imshow("mask1", mask1.astype(np.uint8) * 255)
cv2.imshow("mask2", mask2.astype(np.uint8) * 255)
cv2.imshow("mask_or", mask_or.astype(np.uint8) * 255)


cv2.imshow("result1", result1)
cv2.imshow("result2", result2)
cv2.imshow("result_and", result_and)
cv2.imshow("result_or", result_or)








img = cv2.imread("C:\\ITSTEP\\ITStep-AI\\data\\lesson1\\baboo.jpg", cv2.IMREAD_GRAYSCALE)


if img is None:
    raise ValueError("Не удалось загрузить изображение.")


cv2.imshow("Original", img)



crop = img[20:80, 60:200]


cv2.imshow("Crop", crop)

cv2.waitKey(0)
cv2.destroyAllWindows()
