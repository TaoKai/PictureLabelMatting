import cv2
import numpy as np
import os, sys
import random

base_dir = "D:/workspace/data/douyinvideo/"
save_dir = "D:/workspace/data/douyin_extract/"

def frame_random_extract():
    extract_num_single = 100
    paths = [base_dir+p for p in os.listdir(base_dir)]
    for vid, vp in enumerate(paths):
        cap = cv2.VideoCapture(vp)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        indices = list(np.arange(frame_count))
        random.shuffle(indices)
        indices = indices[:extract_num_single]
        indices.sort()
        i = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                if i in indices:
                    # cv2.imshow("", frame)
                    # cv2.waitKey(1)
                    indices.remove(i)
                    sp = save_dir+str(vid)+"_"+str(i)+".jpg"
                    cv2.imwrite(sp, frame)
                    print("extract to", sp)
            else:
                break
            i += 1
        cap.release()

frame_random_extract()