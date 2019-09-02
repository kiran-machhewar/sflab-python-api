from flask import Flask, request, Response, redirect, abort
from flask_cors import CORS, cross_origin
from flask import render_template
import json
import os.path
import util.kmlib
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/')
def hello_world():
    return render_template('index.html', message='SF Python API by Kiran Machhewar') 
    
@app.route('/oauth/callback',methods=['GET'])
def handle_oauth_callback():    
    code = request.args.get('code')   
    access_token = util.kmlib.getAccessTokenByCode(code,request.args.get('state'),os.environ['CLIENT_ID'],os.environ['SECRETE_KEY'])        
    return redirect('https://enigmatic-river-52223.herokuapp.com?testVsLogin='+request.args.get('state')+'&access_token='+access_token)

@app.route('/api/getSObjectIds',methods=['POST'])
def get_sobject_ids():
    try:
        if not request.json or not 'sessionId' in request.json or not 'instanceURL' in request.json or not 'batchSize' in request.json or not 'query' in request.json :
            raise Exception('Paramters are missing.')
        result = util.kmlib.getSObjectIds(request.json['query'],request.json['sessionId'],request.json['instanceURL'],request.json['batchSize'])        
        resp = Response(json.dumps(result))       
    except Exception as error:
        print('Error in getSObjectIds-->'+str(error))
        resp = Response(str(error), status=400)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp        

@app.route('/api/runApexCode',methods=['POST'])
def runApexCode():
    try:
        if not request.json or not 'sessionId' in request.json or not 'instanceURL' in request.json or not 'apexCode' in request.json or not 'orgId' in request.json :
            raise Exception('Paramters are missing.')
        apexCode = request.json['apexCode']    
        sessionId = request.json['sessionId']    
        instanceURL = request.json['instanceURL']    
        orgId = request.json['orgId']    
        
        result = util.kmlib.runApexCode( apexCode, sessionId, instanceURL, orgId)
        resp = Response(result)
    except Exception as error:
        resp = Response(str(error), status=400)
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

@app.route('/api/makeToolingAPIQuery',methods=['GET'])
    try:
        if not request.json or not 'sessionId' in request.json or not 'instanceURL' in request.json or not 'query' in request.json:
            raise Exception('Paramters are missing.')
        query = request.json['query']    
        sessionId = request.json['sessionId']    
        instanceURL = request.json['instanceURL']            
        
        result = util.kmlib.makeToolingAPIQuery( query, sessionId, instanceURL)
        resp = Response(result)
    except Exception as error:
        resp = Response(str(error), status=400)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Content-Type'] = 'application/json'
    return resp
        
if __name__ == '__main__':    
    app.run()
    