import json
from flask import Flask, jsonify, make_response, request, Response
from flask_api import status
from google.cloud import datastore
import datetime

app = Flask(__name__)
client = datastore.Client()

@app.route('/api/createdata', methods=['POST'])
def create_data():
  try:
    data = request.data.decode('utf-8')
    data = json.loads(str(data))
    key = client.key("Task2")
    entity = datastore.Entity(key)
    entity.update(data)
    client.put(entity)
    response = jsonify({'status':'200','message': 'success'})
    return response
  except Exception as e:
    result = error_handler(e)
    return result

@app.route('/api/searchdata', methods=['GET'])
def search_data():
  try:
    data = request.data.decode('utf-8')
    data = json.loads(str(data))
    keylist= [i for i in data.keys()]
    valuelist = [ j for j in data.values()]
    query = client.query(kind="Task2")
    for k,v in zip(keylist,valuelist):
        query.add_filter(k, "=", v )
    result = list(query.fetch())
    return jsonify(result)
  except Exception as e:
    return error_handler(e)

@app.errorhandler(400)
@app.errorhandler(404)
@app.errorhandler(500)
def error_handler(error):
    response = jsonify({
                          "error": {
                          "type": error.name,
                          "message": error.description
                          }
                      })
    return response, error.code

if __name__ == '__main__':
  app.debug=True
  app.run(host='0.0.0.0')
