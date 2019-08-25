from flask import Flask, request, Response
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World! - Kiran Machhewar' 
    
@app.route('/json-post', methods=['POST'])
def json_post():
    req_data = request.get_json()
    name = req_data['name']
    email = req_data['email']
    resp = Response('''
           { "Passed Name": "Kiran",
           "Passed Email": "smachhewar@gmail.com" }''')
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/oauth/callback',methods=['GET'])
def handle_oauth_callback():    
    code = request.args.get('code')    
    resp = Response('{ "Passed Name": "Code is '+code+'"}')
    return resp

if __name__ == '__main__':
    app.run()
    