import numpy as np
import cv2 as cv

grid_size = 8
img = cv.imread("/Users/shenzhongqiang/Desktop/test.png")
#img = cv.blur(img, (grid_size//2, grid_size//2))

(h, w, _) = img.shape
h = int(h/grid_size) * grid_size
w = int(w/grid_size) * grid_size
roi = img[:h, :w]

new_img = np.ones((h, w, 3)) * 255
new_img = new_img.astype(np.uint8)

for j in range(0, h, grid_size):
    for i in range(0, w, grid_size):
        grid = roi[j:j+grid_size, i:i+grid_size]
        color = np.mean(grid, axis=(0,1)).astype(int).tolist()
        g = np.mean(color)
        max_r = grid_size//2 - 1
        if g >= 200:
            r = int(max_r/-55 * (g-255))
        else:
            r = max_r

        if r > 0:
            cv.circle(new_img, (i+grid_size//2, j+grid_size//2), r, color, -1, cv.LINE_AA)

cv.imshow("pic", new_img)
cv.waitKey(0)

