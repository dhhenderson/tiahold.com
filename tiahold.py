from flask import Flask, render_template
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
@app.route('/index.html')
@app.route('/index.htm')
def index():
    return render_template('index.html')

# We only need this for local development.
if __name__ == '__main__':
    app.run()

