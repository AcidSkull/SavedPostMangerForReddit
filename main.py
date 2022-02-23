from flask import Flask, render_template, request
from requests.auth import HTTPBasicAuth
import os, random, requests

app = Flask(__name__)

REDDIT_TOKEN = os.environ.get("REDDIT_TOKEN")
CLIENT_ID = os.environ.get("CLIENT_ID")
RANDOM_STRING = str(random.randint(16, 90))
URI = 'https://savescraperforreddit.herokuapp.com'

url = f"https://www.reddit.com/api/v1/authorize?client_id={CLIENT_ID}&response_type=code&state={RANDOM_STRING}&redirect_uri={URI}&duration=temporary&scope=history"

@app.route('/')
def index():
    if request.args.get('code'):
        access_token = requests.post('https://reddit.com/api/v1/access_token', 
        auth=HTTPBasicAuth(CLIENT_ID, REDDIT_TOKEN),
        headers={'User-agent' : 'Save Scraper 0.0.1', 'Content-Type': 'application/x-www-form-urlencoded'},
        data={"grant_type":'authorization_code', "code":f"{request.args.get('code')}", "redirect_uri":f"{URI}"})
        print(access_token)
        return 'access_token'
    return render_template('index.html', auth=url)

if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)