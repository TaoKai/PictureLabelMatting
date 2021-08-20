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

lock = Lock()
ip_address = "http://localhost:9092/"
file_cursor = 0

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

app = Flask(__name__)
@app.route('/', methods=['POST', 'GET'])
def upload():
    basepath = os.path.dirname(__file__) # 当前文件所在路径
    files = list_pictures(ip_address)
    dic = {
        'image': files[0]
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
        img_file = "static/cache/data_pictures/"+img_name
        json_line = member_id+"|"+img_file+"|"+img_maps+"\n"
        lock.acquire()
        f = open(log_file, "a", "utf-8")
        f.write(json_line)
        f.close()
        lock.release()
        files = list_pictures(ip_address)
        return files[0]
 
if __name__ == '__main__':
    app.run(debug=False, port=9092, host='0.0.0.0')