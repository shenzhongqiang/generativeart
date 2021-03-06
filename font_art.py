import random
import numpy as np
import cv2
import matplotlib.pyplot as plt
from PIL import ImageFont, ImageDraw, Image

plt.rcParams['figure.figsize'] = [16, 24]

def point_in_contours(point, contours, hierarchy):
    res = False
    outer_ids = []
    inner_ids = []
    for i in range(len(hierarchy[0])):
        if hierarchy[0][i][3] == -1:
            outer_ids.append(i)
        else:
            inner_ids.append(i)
    outer_contours = list(map(lambda x: contours[x], outer_ids))
    inner_contours = list(map(lambda x: contours[x], inner_ids))
    for contour in outer_contours:
        dist = cv2.pointPolygonTest(contour, point, True)
        res = res or dist > 0
    for contour in inner_contours:
        dist = cv2.pointPolygonTest(contour, point, True)
        res = res and dist < 0

    return res

width = 2000
height = 1200
sizes = [1, 2, 2, 2, 3, 3, 3, 5]
thicks = range(2, 6, 1)
colors = [(255, 78, 78), (102,160,104), (102, 180, 104), (255, 78, 57), (255, 78, 19)]#, (255, 255, 255)]
img = np.zeros((height, width, 3), np.uint8)

# write English
cv2.putText(img, 'Merry', (380,450), cv2.FONT_HERSHEY_SIMPLEX, 15, (255,255,255), 40, cv2.LINE_AA)
cv2.putText(img, 'Christmas', (80,850), cv2.FONT_HERSHEY_SIMPLEX, 12, (255,255,255), 40, cv2.LINE_AA)

# write Chinese
#fontpath = "/usr/share/fonts/truetype/microsoft/SIMSUN.TTC"
#font = ImageFont.truetype(fontpath, 240)
#img_pil = Image.fromarray(img)
#draw = ImageDraw.Draw(img_pil)
#draw.text((50, 100), "你好", font=font, fill=(255,255,255))
#img = np.array(img_pil)

imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(imgray, 127, 255, 0)
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#print(hierarchy)
cv2.drawContours(img, contours, -1, (0, 255,0), 1)

img_res = np.ones((height, width, 3), np.uint8) * 255

for y in range(0, height, 6):
    for x in range(0, width, 8):
        offset_x = random.choice(range(-10, 11, 1))
        offset_y = random.choice(range(-8, 9, 1))
        point = (x+offset_x, y+offset_y)
        if not point_in_contours(point, contours, hierarchy):
            continue
        overlay = img_res.copy()
        size = random.choice(sizes)
        color = random.choice(colors)
        thick = random.choice(thicks)
        alpha = random.uniform(0.6, 1)
        cv2.circle(overlay, point, size, color, thick)
        img_res = cv2.addWeighted(overlay, alpha, img_res, 1-alpha, 0)

img_res = cv2.cvtColor(img_res, cv2.COLOR_BGR2RGB)
cv2.imwrite("text.jpg", img_res)
cv2.imshow("text", img_res)
cv2.waitKey(0)
cv2.destroyAllWindows()
