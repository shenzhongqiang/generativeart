import matplotlib.pyplot as plt
import numpy as np
import cv2

im_flag = cv2.imread("images/flagcrop.png", cv2.IMREAD_UNCHANGED)
im_flag[im_flag[:,:,3]==0]=[0, 0, 0, 0]
im_profile = cv2.imread("images/bg.jpg", cv2.IMREAD_UNCHANGED)
im_profile = cv2.cvtColor(im_profile, cv2.COLOR_RGB2RGBA)

profile_h, profile_w, _= im_profile.shape
img = np.zeros((profile_h, profile_w, 4), np.uint8)
flag_h, flag_w, _ = im_flag.shape
flag_bg = np.zeros((flag_h+23, flag_w+27, 4), np.uint8)
flag_bg[13:13+flag_h, 17:17+flag_w] = im_flag
white_bg = np.ones((profile_h, profile_w, 4), np.uint8) * 255

flag_bg_h, flag_bg_w, _ = flag_bg.shape
x_left = profile_w - flag_bg_w - 5
y_top = profile_h - flag_bg_h - 5


imgray = cv2.cvtColor(flag_bg, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 100, 255, cv2.THRESH_BINARY)


# draw contour around flag
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = np.array(contours)
contours[:,:,:,0] = contours[:,:,:,0]*1.12
contours[:,:,:,1] = contours[:,:,:,1]*1.08
contours = contours.astype(np.int)

flag_contr = cv2.drawContours(flag_bg, contours, -1, (255, 255, 255, 255), 15, offset=(-11, -7))

flag_contr[flag_contr[:,:,3]==0] = [255, 255, 255, 0]

# anti-aliasing
kernel = np.ones((3, 3), np.float32)/9
flag_blur = cv2.filter2D(flag_contr, -1, kernel)

# draw white background
border = 30
top_left = (border*2, border)
bottom_right = (profile_w-border*2, profile_h-border)
cv2.rectangle(white_bg, top_left, bottom_right, (0,0,0,0), -1)
top_left = (border, border*2)
bottom_right = (profile_w-border, profile_h-border*2)
cv2.rectangle(white_bg, top_left, bottom_right, (0,0,0,0), -1)
cv2.circle(white_bg, (border*2, border*2), border, (0,0,0,0), -1)
cv2.circle(white_bg, (profile_w-border*2, border*2), border, (0,0,0,0), -1)
cv2.circle(white_bg, (profile_w-border*2, profile_h-border*2), border, (0,0,0,0), -1)
cv2.circle(white_bg, (border*2, profile_h-border*2), border, (0,0,0,0), -1)


for i in range(profile_h):
    for j in range(profile_w):
        if white_bg[i,j,3] == 0:
            white_bg[i,j] = im_profile[i,j]

for i in range(flag_bg_h):
    for j in range(flag_bg_w):
        if flag_blur[i, j, 3] > 0:
            if y_top+i >= profile_h or x_left+j >= profile_w:
                continue
            white_bg[y_top+i, x_left+j] = flag_blur[i,j]

cv2.imshow('image', white_bg)
cv2.waitKey(0)
cv2.destroyAllWindows()
