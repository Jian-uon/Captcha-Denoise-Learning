#coding:utf-8
import numpy as np
from PIL import Image
import sys


sys.setrecursionlimit(160*60)
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

def flood_denoise(img):
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
    dx = [-1, -1, 1, 1]
    dy = [-1, 1, -1, 1]
    for i in xrange(4):
        nx = x+dx[i]
        ny = y+dy[i]
        if nx > 0 and nx < w and ny > 0 and ny < h and  visited[nx][ny] == -1:
            if img.getpixel((nx, ny)) < threshold:
                dfs(nx, ny, index)
            else:
                visited[nx][ny] = 0
    return

if __name__ == '__main__':
    print np.array(img)
    new_img = flood_denoise(img)
    new_img.save('f'+filename)
    new_img.show()
