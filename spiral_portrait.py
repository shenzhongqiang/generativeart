import numpy as np
import cv2

B = 3
RATIO = 6

def get_spiral_points(center, i):
    base_theta = np.pi/180 * i
    num = np.ceil(i * 10e-4).astype('uint8')
    result = []
    for j in range(num):
        theta = base_theta + j*np.pi/180/num
        r = theta * B
        x = int(center[0] + r*np.cos(theta))
        y = int(center[1] + r*np.sin(theta))
        result.append((x, y))
    return result

def draw_with_color():
    im = cv2.imread("images/yuanyuan.jpg")
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    shape = imgray.shape
    mask = np.ones(shape) * 255
    width = shape[1]
    height = shape[0]
    center = (int(width/2), int(height/2))
    max_r = np.min(center)

    points = []
    num = int(max_r/np.pi*180/B)
    sizes = np.random.normal(2, 1, size=num).astype('uint8')
    sizes[sizes>3]=3
    sizes[sizes<2]=2
    sizes = np.random.randint(2, 4, size=num)

    for i in range(num):
        points = get_spiral_points(center, i)
        for point in points:
            cv2.circle(mask, point, radius=sizes[i], color=0, thickness=-1)

    mask = mask.astype(imgray.dtype)
    res = cv2.bitwise_or(imgray,mask)
    cv2.imshow("output", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def draw_with_thickness():
    im = cv2.imread("images/yuanyuan.jpg")
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    shape = imgray.shape
    newshape = np.multiply(shape, RATIO)
    res = np.ones(newshape) * 255
    width = newshape[1]
    height = newshape[0]
    center = (int(width/2), int(height/2))
    max_r = np.min(center)

    spiral_points = []
    num = int(max_r/np.pi*180/B)
    sizes = np.random.normal(2, 1, size=num).astype('uint8')
    sizes[sizes>3]=3
    sizes[sizes<2]=2
    sizes = np.random.randint(2, 4, size=num)

    for i in range(num):
        points = get_spiral_points(center, i)
        spiral_points.extend(points)

    min_color = np.min(imgray)
    max_color = np.max(imgray)
    samples = np.linspace(min_color, max_color, 4)

    for point in spiral_points:
        cord = (int(point[1]/RATIO), int(point[0]/RATIO))
        color = imgray[cord]
        size = 8-2*np.argmax(samples>=color)
        cv2.circle(res, point, radius=size, color=0, thickness=-1, lineType=cv2.LINE_AA)

#    kernel = np.ones((2,2),np.float32)/4
#    res = cv2.filter2D(res,-1,kernel)
    cv2.imwrite("output.jpg", res)
    cv2.imshow("output", res)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == "__main__":
    draw_with_thickness()
