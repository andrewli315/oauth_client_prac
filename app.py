import sys
from io import BytesIO
from flask import Flask,request,render_template,jsonify,redirect, url_for
import json
import requests
from flask_bootstrap import Bootstrap
from flask_cors import CORS


app = Flask(__name__)
bootstrap = Bootstrap(app)
CORS(app)

@app.route('/', methods=['GET'])
def show_root():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def authorize():
    red =  redirect('http://140.118.110.32:50080/oauth/web/login?response_type=code&client_id=m10709311&state=programming_homework_2&redirect_uri=http://192.168.2.46:8080/authorize')  
    #red =  redirect('http://140.118.110.32:50080/oauth/web/login?response_type=code&client_id=m10709311&state=programming_homework_2&redirect_uri=http://140.118.110.164:8877/authorize')  
    return red



@app.route('/authorize', methods=['GET'])
def auth():
    code = request.args.get('code')
    print(code)
    code = code.strip('/')
    print(code)
    return render_template('auth.html',code=code)

@app.route('/token',methods=['GET'])
def get_token():
    code = request.args.get('code')
    code = code.strip('/')
    uri = 'http://140.118.110.32:50080/oauth/web/token'
    po_data = {
            'grant_type':'authorization_code',
            'code':code,
            'client_id':'m10709311',
            'client_secret':'4dfa258235c20dbb04207fc703ccd7fd67514884',
            'redirect_uri':'http://192.168.2.46:8080/authorize'
            #'redirect_uri':'http://140.118.110.164:8877/authorize'
            }
    print(po_data)
    r = requests.post(url=uri, data=po_data)
    print(r.status_code)
    print(r.text)
    ret = json.loads(r.text)
    print(ret['access_token'])
    #r = render_template('access.html',token=ret['access_token'],refresh_token=ret['refresh_token'])
    #return redirect('http://192.168.2.46:8080/access?access_token='+ret['access_token']+'&refresh_token='+ret['refresh_token'])
    return render_template('access.html',token=ret['access_token'],refresh_token=ret['refresh_token'])
    
@app.route('/access',methods=['GET','POST'])
def access():
    token = request.args.get('access_token')
    print(token)
    payload={'access_token':token}
    r = requests.get('http://140.118.110.32:50080/oauth/web/resource',payload)
    print(r.text)
    ret = json.loads(r.text)
    first_name = ret['first_name']
    last_name = ret['last_name']
    return render_template('data.html',first_name=first_name,last_name=last_name)

@app.route('/robots.txt')
def robots():
    robots_file = render_template('robots.txt')
    return robots_file

# listening 0.0.0.0
# in local port 8080

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=False)


