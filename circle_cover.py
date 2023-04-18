import sys
import time
import numpy as np
import cv2 as cv

class Counter(object):
    def __init__(self):
        self.loop_nums = []
        self.circle_nums = []

    def add(self, loop_num, circle_num):
        print(loop_num, circle_num)
        self.loop_nums.append(loop_num)
        self.circle_nums.append(circle_num)

    def is_end(self):
        num = len(self.circle_nums)
        circle_num = self.circle_nums[num-1]
        for i in range(num-1, -1, -1):
            if self.circle_nums[i] <= circle_num - 10:
                break
        if self.loop_nums[num-1] - self.loop_nums[i] > 1e4:
            return True

        return False


def main(filename):
    n = 6000
    sizes = np.array([2,3,4,5,6])
    p = np.flip(sizes)**2 * 1/np.sum(sizes**2)


    img = cv.imread(filename)
    (h, w, _) = img.shape
    if w > 640:
        factor = 640/w
        img = cv.resize(img, (0,0), fx=factor, fy=factor)
    (h, w, _) = img.shape
    new_img = np.ones(img.shape) * 255
    new_img = new_img.astype(np.uint8)

    x_array = np.array([])
    y_array = np.array([])
    r_array = np.array([])

    start = time.time()
    i = 0
    c = Counter()
    while True:
        x = np.random.randint(w)
        y = np.random.randint(h)
        r = np.random.choice(sizes, p=p)
        dist = ((x-x_array)**2 + (y-y_array)**2)**0.5
        overlap = np.any(dist-r-r_array<1)

        if not overlap:
            color = img[y, x].tolist()
            cv.circle(new_img, (x, y), r, color, -1, cv.LINE_AA)
            x_array = np.append(x_array, x)
            y_array = np.append(y_array, y)
            r_array = np.append(r_array, r)

        if len(x_array) >= n:
            break

        c.add(i, len(x_array))
        if c.is_end():
            break
        i += 1

    end = time.time()
    print("elapsed ", end-start)
    cv.imwrite("output2.png", new_img)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <filename>" % sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]
    main(filename)
