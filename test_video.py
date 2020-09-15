from yolo import YOLO
from PIL import Image
import numpy as np
import cv2
import time
yolo = YOLO()


# 调用摄像头
vid=cv2.VideoCapture("/home/ubuntu/Bubbliiiing-yolov4-pytorch-master/videos/test06.mp4")
video_frame_cnt = int(vid.get(7))
video_width = int(vid.get(3))
video_height = int(vid.get(4))
video_fps = int(vid.get(5))

fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
videoWriter = cv2.VideoWriter('test_result_06.mp4', fourcc, video_fps, (video_width, video_height))

print(vid.isOpened())

fps = 0.0
while(True):
    t1 = time.time()
    # 读取某一帧
    ref,frame= vid.read()
    #print(ref)
    # 格式转变，BGRtoRGB
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    # 转变成Image
    frame = Image.fromarray(np.uint8(frame))

    # 进行检测
    frame = np.array(yolo.detect_image(frame))

    # RGBtoBGR满足opencv显示格式
    frame = cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)

    fps  = (fps + (1./(time.time()-t1))) / 2
    print("fps= %.2f"%(fps))
    frame = cv2.putText(frame, "fps= %.2f"%(fps), (0, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    videoWriter.write(frame)


    c= cv2.waitKey(30) & 0xff
    if c==27:
        vid.release()
        break
