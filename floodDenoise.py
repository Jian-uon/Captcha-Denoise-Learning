#coding:utf-8
#洪水填充法去除大的噪点
import numpy as np
from PIL import Image
import sys


#是我dfs写的有问题吗。。不加最大深度会爆栈，真的是有问题。。
sys.setrecursionlimit(160*60)
#全局定义太多差评。。。
filename = '2.jpg'
img = Image.open(filename)
img = img.convert('L')

visited = np.array(0)
(w, h) = img.size
visited = np.array([-1]*w*h)
visited.shape= (w,h)
threshold = 230
zone_threshold = w*h/100
zone = [0]*w*h

def flood_fill_denoise(img):
    print img.size
    index = 1
    for i in xrange(w):
        for j in xrange(h):
            if visited[i][j] == -1:
                if img.getpixel((i,j)) < threshold:
                    dfs(i, j, index)
                    index += 1
                else:
                    visited[i][j] == 0
    
    remove_list = [0]*w*h
    for id, val in enumerate(zone):
        if val < zone_threshold:
            remove_list[id] = 1

    for i in xrange(w):
        for j in xrange(h):
            if remove_list[visited[i][j]] == 1:
                img.putpixel((i,j), 255)
            
    return img 

def dfs(x, y, index):
    #print x, y, index,w, h
    if visited[x][y] != -1:
        return
    visited[x][y] = index
    zone[index] += 1 
    dx = [-1, 0, 1, 0]
    dy = [0, 1, 0, -1]
    for i in xrange(4):
        nx = x+dx[i]
        ny = y+dy[i]
        if nx > 0 and nx < w and ny > 0 and ny < h and  visited[nx][ny] == -1:
            if img.getpixel((nx, ny)) < threshold:
                dfs(nx, ny, index)
            else:
                visited[nx][ny] = 0
    return

#二值化图片
#img为Image类型 b为阈值
def getBinaryImage(img, b):
    for i in xrange(img.size[0]):
        for j in xrange(img.size[1]):
            if img.getpixel((i,j)) > b:
                img.putpixel((i,j), 255)
            else:
                img.putpixel((i,j), 0)
    return img

if __name__ == '__main__':
    img = getBinaryImage(img, threshold)
    img.save('binary'+filename)
    new_img = flood_fill_denoise(img)
    new_img.save('result'+filename)
    new_img.show()
