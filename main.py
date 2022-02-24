from flask import Flask, render_template, request, session
from uuid import uuid4
import os, requests

app = Flask(__name__)
app.secret_key = str(uuid4)

CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")
URI = 'https://savescraperforreddit.herokuapp.com'

def get_access_token(code):
    auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    
    data = {'grant_type' : 'authorization_code',
            'code' : code,
            'redirect_uri' : URI}

    headers = {'User-agent' : 'SaveScraperForReddit/0.2.1 by u/AciidSkull'}

    access_token = requests.post('https://ssl.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    token = access_token.json()

    return token['access_token']

@app.route('/')
def index():
    random_string = str(uuid4())
    url = f"https://www.reddit.com/api/v1/authorize?client_id={CLIENT_ID}&response_type=code&state={random_string}&redirect_uri={URI}&duration=temporary&scope=identity,read,history"

    if (request.args.get('code')):
        Token = get_access_token(request.args.get('code'))
        response = requests.get("https://oauth.reddit.com/api/v1/me", headers={"Authorization" : "bearer " + Token, 'User-agent' : 'SaveScraperForReddit/0.2.1 by u/AciidSkull'})
        if response.status_code == 200:
            json = response.json()
            session['name'] = json['name']
            
            response = requests.get(f"https://oauth.reddit.com/api/user/{session['name']}/saved", headers={"Authorization" : "bearer " + Token, 'User-agent' : 'SaveScraperForReddit/0.2.1 by u/AciidSkull'})
            print(response)
            if response.status_code == 200:
                json = response.json()
                session['saved'] = json
        
    return render_template('index.html', auth_url=url)

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)