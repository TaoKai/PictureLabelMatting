from flask import Flask,render_template,request,redirect,url_for
from werkzeug.utils import secure_filename
import os
import cv2
import random
import sys
import json
import shutil

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
    files = list_pictures("http://localhost:9092/")
    dic = {
        'image': files[0]
    }
    if request.method == 'POST':
        pass
    return render_template('index.html', **dic)

@app.route('/get_points', methods=['POST'])
def get_points():
    if request.method=='POST':
        json_str = request.get_data()
        map_data = json.loads(json_str)
        img_src = map_data["src"]
        img_maps = map_data["heat_maps"]
        img_name = img_src.split("/")[-1]
        img_file = "./static/cache/data_pictures/"+img_name
        print(img_file, img_maps)
        files = list_pictures("http://localhost:9092/")
        return files[0]
 
if __name__ == '__main__':
    app.run(debug=False, port=9092, host='0.0.0.0')