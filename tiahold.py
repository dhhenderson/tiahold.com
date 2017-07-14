from flask import Flask, render_template, json
from flask_bootstrap import Bootstrap
import requests

app = Flask(__name__)
app.config.from_object('default_settings')
app.config.from_envvar('TIAHOLD_SETTINGS', silent=True)

#print(app.config['DEBUG'])

Bootstrap(app)

@app.route('/_get_timestamp')
def get_timestamp():
    try:
        r = requests.get(app.config['TIMESTAMP_URL'], timeout=2)
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
