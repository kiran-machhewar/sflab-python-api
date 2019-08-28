from flask import Flask, request, Response, redirect
from flask import render_template
import json
import os.path
import util.kmlib
app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html', message='SF Python API by Kiran Machhewar') 
    
@app.route('/oauth/callback',methods=['GET'])
def handle_oauth_callback():    
    code = request.args.get('code')   
    access_token = util.kmlib.getAccessTokenByCode(code,request.args.get('state'),os.environ['CLIENT_ID'],os.environ['SECRETE_KEY'])        
    return redirect('https://enigmatic-river-52223.herokuapp.com?testVsLogin='+request.args.get('state')+'&access_token='+access_token)

@app.route('/api/getSObjectIds',methods=['POST'])
def getSObjectIds():
    if not request.json or not 'sessionId' in request.json or not 'instanceURL' in request.json or not 'batchSize' in request.json or not 'query' in request.json :
        abort(400)
    print('request.json')
    print(request.json)
    result = util.kmlib.getSObjectIds(request.json['query'],request.json['sessionId'],request.json['instanceURL'],request.json['batchSize'])    
    print('jsonDump-->')
    print(json.dumps(result))
    resp = Response(json.dumps(result))
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp
    
@app.route('/api/getUserInfo',methods=['GET'])
def getUserInfo():
    access_token = request.args.get('access_token')
    testVsLogin  = request.args.get('testVsLogin')
    jsonResponse = util.kmlib.getUserInfo(access_token,testVsLogin)
    print('JSONResponse')
    print(jsonResponse)
    resp = Response(jsonResponse)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp 
    
if __name__ == '__main__':    
    app.run()
    