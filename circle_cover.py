import numpy as np
import cv2 as cv

class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

    def set_color(self, color):
        self.color = color

    def dist(self, c):
        point1 = np.array((self.x, self.y))
        point2 = np.array((c.x, c.y))
        dist = np.linalg.norm(point1 - point2)
        return dist

    def overlap(self, c):
        d = self.dist(c)
        if d <= self.r + c.r + 1:
            return True
        return False


n = 2000
sizes = [2,3,4,5,6]
min_p = 1/sum(sizes)
p = [i*min_p for i in reversed(sizes)]

img = cv.imread("/Users/shenzhongqiang/Desktop/test.png")
(h, w, _) = img.shape
mask = np.zeros((h, w))

circles = []
while True:
    indices = np.argwhere(mask==0)
    i = np.random.randint(len(indices))
    y = indices[i][0]
    x = indices[i][1]
    r = np.random.choice(sizes, p=p)
    cn = Circle(x, y, r)
    overlap = False
    for c in circles:
        overlap = cn.overlap(c)
        if overlap:
            break

    if not overlap:
        color = img[y, x].tolist()
        cv.circle(mask, (x, y), r, 1, -1, cv.LINE_AA)
        cn.set_color(color)
        circles.append(cn)
    if len(circles) >= n:
        break

cv.imshow("pic", mask)
#cv.waitKey(0)

