import numpy as np
import cv2

RATIO = 1.5

def get_spiral_points(center, i):
    base_theta = np.pi/180 * i
    num = np.ceil(i * 10e-4).astype('uint8')
    result = []
    for j in range(num):
        theta = base_theta + j*np.pi/180/num
        r = theta * RATIO
        x = int(center[0] + r*np.cos(theta))
        y = int(center[1] + r*np.sin(theta))
        result.append((x, y))
    return result

def draw_spiral(img, center, max_r):
    points = []
    num = int(max_r/np.pi*180/RATIO)
    sizes = np.random.normal(2, 1, size=num).astype('uint8')
    sizes[sizes>3]=3
    sizes[sizes<2]=2
    sizes = np.random.randint(2, 4, size=num)
    print(np.min(sizes))
    for i in range(num):
        points = get_spiral_points(center, i)
        for point in points:
            cv2.circle(img, point, 1, 0, sizes[i])

im = cv2.imread("yuanyuan.jpg")
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
shape = imgray.shape
mask = np.ones(shape) * 255
width = shape[1]
height = shape[0]
center = (int(width/2), int(height/2))
max_r = np.max(center)
draw_spiral(mask, center, max_r)
mask = mask.astype(imgray.dtype)
res = cv2.bitwise_or(imgray,mask)
cv2.imshow("output", res)
cv2.waitKey(0)
cv2.destroyAllWindows()

