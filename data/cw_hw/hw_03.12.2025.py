import ultralytics
import numpy as np
import cv2

model = ultralytics.YOLO(r'C:\ITSTEP\ITStep-AI\data\lesson_seg\brain-tumor-seg.pt')

img = cv2.imread(r'C:\ITSTEP\ITStep-AI\data\lesson_seg\tumor1.jpg')

results = model.predict(img, verbose=False)
result = results[0]

masks = result.masks.data
mask = masks[0]

mask = mask.cpu().numpy().astype(np.uint8)
mask *= 255

pixels_area = mask.astype(bool).sum()

cm2_area = pixels_area * 0.0025

if cm2_area < 10:
    tumor_type = "small"
elif cm2_area <= 25:
    tumor_type = "middle"
else:
    tumor_type = "large"

mask_bool = mask.astype(bool)
tumor_img = img.copy()
tumor_img[~mask_bool] = 0

cv2.imshow(tumor_type, tumor_img)

print("Pixels:", pixels_area)
print("Area cm2:", cm2_area)
print("Type:", tumor_type)

cv2.waitKey(0)
