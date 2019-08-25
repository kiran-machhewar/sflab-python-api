from flask import Flask, request, Response
import os.path
import util.kmlib
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! - Kiran Machhewar' 
    
@app.route('/oauth/callback',methods=['GET'])
def handle_oauth_callback():    
    code = request.args.get('code')   
    access_token = util.kmlib.getAccessTokenByCode(code,request.args.get('state'),os.environ['CLIENT_ID'],os.environ['SECRETE_KEY'])
    resp = Response('{ "Passed Name": "Code is '+code+'", "Access Token":"'+access_token+'"}')
    return resp

if __name__ == '__main__':    
    app.run()
    