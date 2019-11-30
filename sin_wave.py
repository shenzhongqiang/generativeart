import cv2
import numpy as np
import matplotlib.pyplot as plt

shape = (600, 600, 3)
img = np.ones(shape, np.uint8) * 255
xs = np.arange(0, 600, 5)
ys_upper = np.array(20*np.sin(-xs/60) + 0.2*xs + 300)
ys_lower = np.array(20*np.sin(-xs/60) - 0.2*xs + 300)
ys_upper = ys_upper.astype(int)
ys_lower = ys_lower.astype(int)
color = (228, 207, 85)
color = (223, 114, 238) #ee72df
points = []
for i in range(len(xs)):
    x = xs[i]
    ys = range(ys_lower[i], ys_upper[i], 3)
    for y in ys:
        points.append((x, y))

points = np.array(points)
size = int(0.6*len(points))
points_ids = np.random.choice(len(points), size=size)
for point in points[points_ids]:
    center = tuple(point)
    overlay = img.copy()
    #cv2.circle(overlay, center, radius=3, color=color, thickness=1, lineType=cv2.LINE_AA)
    cv2.circle(overlay, center, radius=3, color=color, thickness=-1, lineType=cv2.LINE_AA)
    img = cv2.addWeighted(overlay, 0.3, img, 0.7, 0)

cv2.imwrite("output.jpg", img)
cv2.imshow("output", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
