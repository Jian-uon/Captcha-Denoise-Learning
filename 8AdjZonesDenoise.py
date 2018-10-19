#coding:utf-8
from PIL import Image
import numpy as np


def check(x, y, width, height):
    if x > 0 and x < width and y > 0 and y < height:
        return True
    return False

#白色点为255，黑色点为0
def detect(img,T):
    dx = [1, 1, 1, 0, -1, -1, -1, 0]
    dy = [-1, 1, 0, 1, -1, 1, 0, -1]
    for x in xrange(img.size[0]):
        for y in xrange(img.size[1]):
            acc = 0
            for _ in xrange(8):
                nx = x + dx[_]
                ny = y + dy[_]
                if check(nx, ny, img.size[0], img.size[1]) == False:
                    continue
                if img.getpixel((nx,ny)) == 255:
                    acc += 1
            #避免无效更新，加入随机函数
            if T%2 == 0 and acc == T:
                if np.random.rand() > 0.5:
                    continue
            if acc >= T:
                img.putpixel((x,y), 255)
    return img

# T为阈值， N为次数
def denoise(img, T, N):
    for _ in xrange(N):
        img = detect(img, T) 
    return img

def get_image(filename):
    img = Image.open(filename)
    #若不是黑白两色图需先二值化，此处用之前处理好的图片
    return img


if __name__ == '__main__':
    filename = 'pic/wb2.jpg'
    img = get_image(filename)
    img = denoise(img, 4, 12)
    img.save('pic/new_wb3.jpg')
    img.show()
    

