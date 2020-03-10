import numpy as np
import cv2

def generate_sheets(im, sheet_num):
    shape = im.shape
    inteval = 256/sheet_num
    sheet_images = np.ones((sheet_num, shape[0], shape[1]), dtype=np.uint8) * 255
    for row in range(shape[0]):
        for col in range(shape[1]):
            value = im[row][col]
            hole_num = int(value/inteval)
            for i in range(hole_num):
                sheet_images[i][row][col] = 255-inteval
    return sheet_images

def merge_sheets(sheet_images):
    shape = sheet_images[0].shape
    result = np.zeros(shape, dtype=np.float16)
    inteval = 256/len(sheet_images)
    for i in range(len(sheet_images)):
        sheet_image = sheet_images[i]
        sheet_image = 255 - sheet_image
        result += sheet_image
    result = result.astype(np.uint8)
    return result

sheet_num = 5
inteval = int(256/sheet_num)
im = cv2.imread("qiangqiang.jpg", cv2.IMREAD_GRAYSCALE)
shape = im.shape
im_new = im/inteval
im_new = im_new.astype(np.uint8) * inteval

print(im_new)
cv2.imshow("effect", im_new)
cv2.waitKey(0)
cv2.destroyAllWindows()

sheet_images = generate_sheets(im, sheet_num)
for i in range(len(sheet_images)):
    filename = "sheet{:02d}.jpg".format(i)
    cv2.imwrite(filename, sheet_images[i])

result_image = merge_sheets(sheet_images)
cv2.imshow("result", result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
