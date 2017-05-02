# -*- coding: utf-8 -*-
import cv2
import numpy as np
import Queue
import matplotlib.pyplot as plt
# 获得视频的格式
videoCapture = cv2.VideoCapture('A四次录像.avi')

# 获得码率及尺寸
fps = videoCapture.get(cv2.cv.CV_CAP_PROP_FPS)
size = (int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)),
        int(videoCapture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT)))
# 读帧
success, frame = videoCapture.read()
print size

fourcc = cv2.cv.FOURCC(*'XVID')
out = cv2.VideoWriter('A四次录像300_90.avi', cv2.cv.CV_FOURCC('M', 'J', 'P', 'G'), fps, size)

q = Queue.Queue()

def dfs(i, j):
    q.put((i, j))
    while q.empty() == False:
        nowi, nowj = q.get()
        for x in xrange(max(nowi - 1, 0), min(nowi + 2, 720)):
            for y in xrange(max(nowj - 1, 0), min(nowj + 2, 1280)):
                if frame[x][y] < 90 and res[x][y] == 0:
                    res[x][y] = 254
                    q.put((x, y))

i = 1
while success:
    print i
    i += 1
    #cv2.imshow("test", frame)  # 显示
    #cv2.waitKey(1000 / int(fps))  # 延迟
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    frame = cv2.GaussianBlur(frame, (3, 3), 500)
    #frame = cv2.GaussianBlur(frame, (3, 3), 500)
    res = cv2.Canny(frame, 10, 300, apertureSize = 3)
    height, width = np.shape(res)

    for x in xrange(height):
        for y in xrange(width):
            if res[x][y] == 255:
                dfs(x, y)

    cv2.imwrite("tmp.png", res)
    aaa = cv2.imread("tmp.png")
    out.write(aaa)
    #print np.shape(aaa)
    success, frame = videoCapture.read()  # 获取下一帧
    # if i > 5:
    #     break
out.release()