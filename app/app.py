import json
import os
import pathlib
import re
import sys
import werkzeug
from werkzeug.utils import secure_filename

from flask import Flask, request, make_response, jsonify, render_template

currentdir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(currentdir)+"/../models/")
from datastore import DataStoreOperate

sys.path.append(str(currentdir)+"/../controllers/")
from viewrender import HtmlRender

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024
UPLOAD_DIR = os.getcwd()
ds = DataStoreOperate()
vr = HtmlRender()

@app.route("/")
def started():
    return render_template('index.html')

@app.route("/select", methods=['GET', 'POST'])
def select():
    #Get Tablelist
    tl = ds.get_kinds_list()
    default_val = tl[0]
    cond = ''
    # Get Request View Render
    if request.method == 'GET':
       slbox = vr.make_selectbox(tl,default_val)
       results = ds.select_records(cond,default_val)
       mode = 'condition'
       conditions = vr.conditionrender(results,mode)
       mode = 'update'
       update = vr.conditionrender(results,mode)
       return render_template('select.html',selectbox=slbox,conditions=conditions,update=update)
    # Post Request Param Send
    if request.method == 'POST':
       tn = request.form.get('table_name')
       ck = request.form.get('condition_key_name')
       cv = request.form.get('condition_value')
       if len(cv) !=0:
          conditions = {ck:cv}
       else:
          conditions = ''
       #Search Records
       if request.form.get('search') == '検索':
          results = ds.select_records(conditions,tn)
       #Delete Records
       elif request.form.get('delete') == '削除':
          ds.delete_records(conditions,tn)
          results = ds.select_records(cond,tn)
       body = vr.tablerender(results)
       slbox = vr.make_selectbox(tl,tn)
       mode = 'condition'
       conditions = vr.conditionrender(results,mode)
       mode = 'update'
       update = vr.conditionrender(results,mode)
       return render_template('select.html',content=body,selectbox=slbox,conditions=conditions,update=update)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
       return render_template('upload.html',content='')
    if request.method == 'POST':
       file = request.files['uploadFile']
       if file:
          filename = secure_filename(file.filename)
          # Get Insert KindName
          kn = os.path.splitext(filename)[0]
          filepath = os.path.join(UPLOAD_DIR, filename) 
          file.save(filepath)
          # Call Data Insert 
          ds = DataStoreOperate()
          ds.insert_data(filepath,kn)
          os.remove(filepath)
          return render_template('upload.html',content='アップロード完了しました')

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    title = str(error.code) + 'エラー' 
    content = str(error.name)
    description = str(error.description)
    return render_template('error.html',title=title,content=content,description=description)

@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    title = 'ファイルエラー'
    content = "werkzeug.exceptions.RequestEntityTooLarge"
    description = 'result : file size is overed.'
    return render_template('error.html',title=title,content=content,description=description)

if __name__ == '__main__':
#    app.run(debug=True)
    app.run(host='0.0.0.0', port=5000)
