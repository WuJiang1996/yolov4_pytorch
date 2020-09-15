#-*- coding = utf-8 -*-
import time
import cv2
from yolo import YOLO
from PIL import Image
import numpy as np
yolo = YOLO()


RTSP_URL = 'rtsp://admin:fcwl123456@192.168.1.108:554/cam/realmonitor?channel=1&subtype=0'   # your camera's rtsp url
DURATION = 30   # how many time in seconds you want to capture
OUTPUT_FILE = 'capture_video.mp4'

cap = cv2.VideoCapture(RTSP_URL)
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#fourcc = 0x21
FPS = cap.get(cv2.CAP_PROP_FPS)
#fps = 25
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
saver = cv2.VideoWriter(OUTPUT_FILE, fourcc, FPS, size)

print("rtsp_url = %s, fps = %d, size = %s"%(RTSP_URL, FPS, size))

got_first_frame = False
frame_count = 0
fps = 0.0
while True:
    t1 = time.time()
    ret, frame = cap.read()
    if not(ret):
        continue

    frame_count += 1
    print("%s: frame %d received" % (time.time(), frame_count))

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # 转变成Image
    frame = Image.fromarray(np.uint8(frame))

    # 进行检测
    frame = np.array(yolo.detect_image(frame))

    # RGBtoBGR满足opencv显示格式
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    fps = (fps + (1./(time.time()-t1))) / 2
    print("fps= %.2f" % (fps))
    frame = cv2.putText(frame, "fps= %.2f" % (fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    
    saver.write(frame)

    if got_first_frame == False:
        start_time = time.time()
        got_first_frame = True

    now = time.time()
    if int(now - start_time) > DURATION:
        break


