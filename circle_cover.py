import time
import numpy as np
import cv2 as cv

class Circle(object):
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

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


n = 5000
sizes = [2,3,4,5,6]
min_p = 1/sum(sizes)
p = [i*min_p for i in reversed(sizes)]

img = cv.imread("/Users/shenzhongqiang/Desktop/test.png")
(h, w, _) = img.shape
new_img = np.ones(img.shape) * 255
new_img = new_img.astype(np.uint8)

circles = []
start = time.time()
while True:
    x = np.random.randint(w)
    y = np.random.randint(h)
    r = np.random.choice(sizes, p=p)
    cn = Circle(x, y, r)
    overlap = False
    for c in circles:
        overlap = cn.overlap(c)
        if overlap:
            break

    if not overlap:
        color = img[y, x].tolist()
        cv.circle(new_img, (x, y), r, color, -1, cv.LINE_AA)
        circles.append(cn)
    if len(circles) >= n:
        break

end = time.time()
print("elapsed ", end-start)
cv.imwrite("output.png", new_img)

