from flask import Flask, render_template, json
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
Bootstrap(app)

# TODO: make url a config setting; does it change? if so, how to update? dynamoDB? tests

@app.route('/_get_timestamp')
def get_timestamp():
    try:
        r = requests.get('https://d7xrbctt1l.execute-api.us-east-1.amazonaws.com/Prod/', timeout=2)
        data = json.loads(r.text)
        app.logger.info(r.text)
        return data['timestamp']
    except requests.exceptions.RequestException as e:
        app.logger.error(e)
        return 'Timestamp unavailable'

@app.route('/')
@app.route('/index.html')
@app.route('/index.htm')
def index():
    return render_template('index.html')

# We only need this for local development.
if __name__ == '__main__':
    app.run()
