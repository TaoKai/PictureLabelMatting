import cv2
import numpy as np
from codecs import open
import json
import os, sys

from numpy.lib.polynomial import poly

def test():
    data_str = open("label_logs/LABEL2021-08-23.log", "r", "utf-8").read().strip().split("\n")
    for line in data_str:
        props = line.split("|")
        mid = props[0].strip()
        path = props[1].strip()
        if os.path.exists(path):
            data_point = json.loads(props[2].strip())
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            info = read_heats(data_point)
            alpha = draw_heats(info, img.shape)
            img_alpha = alpha/255*img
            img_alpha = img_alpha.astype(np.uint8)
            img = np.concatenate([img, alpha, img_alpha], axis=1)
            cv2.imshow(mid, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

def draw_heats(poly_info, shp):
    alpha = np.zeros((1000,800,3), dtype=np.uint8)
    for pi in poly_info:
        if pi[1]==0:
            points = np.array(pi[0], dtype=np.int32)
            pen = (1-pi[1])*255
            cv2.fillPoly(alpha, [points], (pen,pen,pen))
    for pi in poly_info:
        if pi[1]==1:
            points = np.array(pi[0], dtype=np.int32)
            pen = (1-pi[1])*255
            cv2.fillPoly(alpha, [points], (pen,pen,pen))
    alpha = cv2.resize(alpha, (shp[1], shp[0]))
    return alpha

def read_heats(json_dic):
    poly_info = []
    for heat in json_dic:
        points_dic = heat["points"]
        pen_type = int(heat["pen_type"])
        points = []
        for p in points_dic:
            x = int(p["x"])
            y = int(p["y"])
            points.append((x, y))
        poly_info.append((points, pen_type))
    return poly_info

test()