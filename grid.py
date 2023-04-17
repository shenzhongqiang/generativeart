import sys
import numpy as np
import cv2 as cv


def circle_grid(filename):
    grid_size = 8
    img = cv.imread(filename)

    (h, w, _) = img.shape
    h = int(h/grid_size) * grid_size
    w = int(w/grid_size) * grid_size
    roi = img[:h, :w]

    new_img = np.ones((h, w, 3)) * 255
    new_img = new_img.astype(np.uint8)

    for j in range(0, h, grid_size):
        for i in range(0, w, grid_size):
            grid = roi[j:j+grid_size, i:i+grid_size]
            color = np.mean(grid, axis=(0,1)).astype(np.uint8).tolist()
            g = np.mean(color)
            max_r = grid_size//2 - 1
            if g >= 200:
                r = int(max_r/-55 * (g-255))
            else:
                r = max_r

            if r > 0:
                cv.circle(new_img, (i+grid_size//2, j+grid_size//2), r, color, -1, cv.LINE_AA)

    cv.imwrite("grid.png", new_img)


def draw_hexagon(img, center, r, color):
    x = center[0]
    y = center[1]
    x1 = x - r
    y1 = y
    x2 = round(x - r/2)
    y2 = round(y - 3**0.5*r/2)
    x3 = round(x + r/2)
    y3 = round(y - 3**0.5*r/2)
    x4 = x + r
    y4 = y
    x5 = round(x + r/2)
    y5 = round(y + 3**0.5*r/2)
    x6 = round(x - r/2)
    y6 = round(y + 3**0.5*r/2)
    pts = np.array([[
        [x1,y1],
        [x2,y2],
        [x3,y3],
        [x4,y4],
        [x5,y5],
        [x6,y6]
    ]])

    cv.fillPoly(img, pts=pts, color=color, lineType=cv.LINE_AA)


def constrain(v, low, high):
    if v < low:
        return low
    if v > high:
        return high
    return v


def nearest_point(w, h, x, y):
    if x < 0 or x >= w:
        x = constrain(x, 0, w-1)
    if y < 0 or y >= h:
        y = constrain(y, 0, h-1)
    return (x, y)


def hexagon_grid(filename):
    grid_size = 12
    img = cv.imread(filename)
    (orig_h, orig_w, _) = img.shape
    ratio = 1
    h = orig_h * ratio
    w = orig_w * ratio
    img = cv.resize(img, (w, h))

    new_img = np.ones((h, w, 3)) * 255
    new_img = new_img.astype(np.uint8)

    centers = []
    y_gap = 2
    x_gap = round(y_gap/(3**0.5/2))
    y_step = round(3**0.5 * grid_size/4)
    x_step = round(1.5 * grid_size)
    row = 0
    while True:
        col = 0
        y = row * y_step + row*y_gap
        if y-y_step >= h:
            break

        while True:
            if row % 2 == 0:
                x = int(grid_size/4 + col*x_step + col*2*x_gap)
            else:
                x = int(grid_size + col*x_step + col*2*x_gap + x_gap)

            if x-grid_size/2 >= w:
                break
            centers.append((x, y))
            col += 1
        row += 1

    for center in centers:
        x = center[0]
        y = center[1]
        top = constrain(y-grid_size//4, 0, h)
        bottom = constrain(y+grid_size//4, 0, h)
        left = constrain(x-grid_size//4, 0, w)
        right = constrain(x+grid_size//4, 0, w)
        grid = img[top:bottom, left:right]
        if grid.size == 0:
            p = nearest_point(w, h, x, y)
            color = img[p[1], p[0]].tolist()
        else:
            color = np.mean(grid, axis=(0,1)).astype(np.uint8).tolist()
        g = np.mean(color)
        max_r = grid_size//2
        r = max_r
        if g >= 200:
            r = int(max_r/-55 * (g-255))

        if r > 0:
            draw_hexagon(new_img, center, r, color)

    new_img = cv.resize(new_img, (w//ratio, h//ratio))
    cv.imwrite("grid.png", new_img)



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: %s <filename>" % sys.argv[0])
        sys.exit(1)
    filename = sys.argv[1]
    hexagon_grid(filename)
