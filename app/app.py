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
    #default_val = ds.get_default_table(tl)
    default_val = tl[0]
    # Get Request View Render
    if request.method == 'GET':
       slbox = vr.make_selectbox(tl,default_val)
       return render_template('select.html',selectbox=slbox)
    # Post Request Param Send
    if request.method == 'POST':
       tn = request.form.get('table_name')
       pkey = request.form.get('partitionkey')
       rkey = request.form.get('rowkey')
       if len(pkey) !=0 and len(rkey) !=0:
          conditions = [pkey,rkey]
       elif len(pkey):
          conditions = "PartitionKey eq '" + pkey +"'"
       else:
          conditions = ""
       # Call Select Records
       if request.form.get('search') == '検索':
          results = ds.select_records(conditions,tn)
          body = vr.tablerender(results)
          slbox = vr.make_selectbox(tl,tn)
          return render_template('select.html',content=body,selectbox=slbox)
       # Call Delete Records
       elif request.form.get('delete') == '削除':
          ds.delete_records(conditions,tn)
          ac = ""
          results = ds.select_records(ac,tn)
          body = vr.tablerender(results)
          slbox = vr.make_selectbox(tl,tn)
          return render_template('select.html',content=body,selectbox=slbox)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
       return render_template('upload.html',content='')
    if request.method == 'POST':
       file = request.files['uploadFile']
       if file:
          filename = secure_filename(file.filename)
          # Get Upsert KindName
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
