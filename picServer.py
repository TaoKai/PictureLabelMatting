from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
import cv2
import random
import sys
import json
import shutil
import time
from codecs import open
from threading import Lock

def randColor():
    rc = random.randint(20, 150)
    gc = random.randint(20, 150)
    bc = random.randint(20, 150)
    return (bc, gc, rc)

def list_pictures(url):
    base = "static/cache/data_pictures/"
    files = os.listdir(base)
    files = [url+base+p for p in files]
    random.shuffle(files)
    return files

lock = Lock()
ip_address = "http://localhost:9092/"
file_cursor = 0
total_picture_files = list_pictures(ip_address)
labeled_pictures = []
finish_pic = ip_address+"static/cache/util_pictures/finish.png"

def get_image_file_by_cursor():
    global file_cursor, total_picture_files
    if file_cursor==len(total_picture_files):
        file_cursor = 0
        total_picture_files = list(set(total_picture_files)-set(labeled_pictures))
        if len(total_picture_files)==0:
            return None
    img_file = total_picture_files[file_cursor]
    file_cursor += 1
    return img_file

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def upload():
    basepath = os.path.dirname(__file__) # 当前文件所在路径
    lock.acquire()
    img_file = get_image_file_by_cursor()
    if img_file is None:
        img_file = finish_pic
    lock.release()
    dic = {
        'image': img_file,
        'ip':ip_address
    }
    if request.method == 'POST':
        pass
    return render_template('index.html', **dic)

@app.route('/get_points', methods=['POST'])
def get_points():
    log_file = time.strftime("label_logs/LABEL%Y-%m-%d.log")
    if request.method=='POST':
        json_str = request.get_data()
        map_data = json.loads(json_str)
        member_id = map_data["member_id"].strip()
        img_src = map_data["src"]
        img_maps = json.dumps(map_data["heat_maps"])
        img_name = img_src.split("/")[-1]
        img_file_local = "static/cache/data_pictures/"+img_name
        json_line = member_id+"|"+img_file_local+"|"+img_maps+"\n"
        lock.acquire()
        f = open(log_file, "a", "utf-8")
        f.write(json_line)
        f.close()
        labeled_pictures.append(img_src)
        img_file = get_image_file_by_cursor()
        if img_file is None:
            img_file = finish_pic
        lock.release()
        return img_file
 
if __name__ == '__main__':
    app.run(debug=False, port=9092, host='0.0.0.0')