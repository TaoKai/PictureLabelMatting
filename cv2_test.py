import cv2
import numpy as np
from codecs import open
import json
import os, sys

from numpy.lib.polynomial import poly

def test():
    data_str = open("label_logs/LABEL2021-08-26.log", "r", "utf-8").read().strip().split("\n")
    for line in data_str:
        props = line.split("|")
        mid = props[0].strip()
        path = props[1].strip()
        if os.path.exists(path):
            data_point = json.loads(props[2].strip())
            img = cv2.imread(path, cv2.IMREAD_COLOR)
            gray = np.ones(img.shape, dtype=np.uint8)*200
            info = read_heats(data_point)
            alpha = draw_heats(info, img)
            img_alpha = alpha/255*img+(1-alpha/255)*gray
            img_alpha = img_alpha.astype(np.uint8)
            img = np.concatenate([img, alpha, img_alpha], axis=1)
            cv2.imshow(mid, img)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

def draw_heats(poly_info, img):
    shp = img.shape
    alpha0 = np.zeros((1000,800,3), dtype=np.uint8)
    alpha1 = np.zeros((1000,800,3), dtype=np.uint8)
    alpha2 = np.zeros((1000,800,3), dtype=np.uint8)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
    for pi in poly_info:
        if pi[1]==0:
            points = np.array(pi[0], dtype=np.int32)
            pen = 255
            cv2.fillPoly(alpha0, [points], (pen,pen,pen))
        elif pi[1]==1:
            points = np.array(pi[0], dtype=np.int32)
            pen = 255
            cv2.fillPoly(alpha1, [points], (pen,pen,pen))
        elif pi[1]==2:
            points = np.array(pi[0], dtype=np.int32)
            pen = 255
            cv2.fillPoly(alpha2, [points], (pen,pen,pen))
    alpha0 = cv2.resize(alpha0, (shp[1], shp[0]))
    alpha1 = cv2.resize(alpha1, (shp[1], shp[0]))
    alpha2 = cv2.resize(alpha2, (shp[1], shp[0]))
    edge_map = get_scharr_map(img)
    alpha2 = alpha2/255
    alpha1 = alpha1/255
    alpha0 = alpha0/255
    alpha2_e = cv2.erode(alpha2, kernel, iterations=3)
    alpha2_d = cv2.dilate(alpha2, kernel, iterations=3)
    alpha0 = np.clip(alpha0-alpha2_e, 0, 1)
    alpha_edge = edge_map/255*alpha2_d
    alpha = np.clip(alpha0+alpha_edge, 0, 1)
    alpha = np.clip(alpha-alpha1, 0, 1)*255
    alpha = alpha.astype(np.uint8)
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

def show(img, name="", wait=0):
    cv2.imshow(name, img)
    cv2.waitKey(wait)

def get_scharr_map(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    sobelx = cv2.Scharr(gray, -1, 1, 0, scale=1)
    sobely = cv2.Scharr(gray, -1, 0, 1, scale=1)
    sobel = np.where(sobelx>sobely, sobelx, sobely)
    sobel = sobel.reshape(sobel.shape+(1,))
    sobel = np.concatenate([sobel, sobel, sobel], axis=2)
    return sobel

if __name__=="__main__":
    test()