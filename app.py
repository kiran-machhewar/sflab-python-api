from flask import Flask, request, Response, redirect
from flask import render_template
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
def handle_api_get_sobject_ids():
    return ''
    
@app.route('/api/getUserInfo',methods=['GET'])
def getUserInfo():
    access_token = request.args.get('access_token')
    testVsLogin  = request.args.get('testVsLogin')
    return util.kmlib.getUserInfo(access_token,testVsLogin)
    


if __name__ == '__main__':    
    app.run()
    