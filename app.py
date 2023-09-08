from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv

from audioop import add
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    post = list(db.diary.find({},{'_id':False}))
    return jsonify({'post': post})

@app.route('/diary', methods=['POST'])
def save_diary():
    #sample_receive = request.form['sample_give']
    #print(sample_receive)
    title_receive= request.form.get('title_give')
    content_receive = request.form.get('content_give')
    
    today = datetime.now()
     
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'file-{mytime}.{extension}'
    save_to = f'static/{filename}'
    file.save(save_to)
    
    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')
    profilename = f'file-{mytime}.{extension}'
    save_profile = f'static/{profilename}'
    profile.save(save_profile)
   
    doc = {
        'file': filename,
        'profile' : profilename,
        'title' : title_receive,
        'content': content_receive 
        
    }
    db.diary.insert_one(doc)
    return jsonify({'msg': 'save sudah di clik!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)