import logging

import boto3

from flask import Flask, render_template, json
from flask_bootstrap import Bootstrap

import requests

app = Flask(__name__)
app.config.from_object('default_settings')
app.config.from_envvar('TIAHOLD_SETTINGS', silent=True)
#print(app.config['DEBUG'])

# with this logger, messages flow from lambda to cloudwatch
logger = logging.getLogger()

Bootstrap(app)

# initialize db
if app.config['DYNAMO_LOCAL']:
    dynamodb = boto3.resource('dynamodb', endpoint_url=app.config['DYNAMO_LOCAL_URL'])
else:
    dynamodb = boto3.resource('dynamodb')
#print "DYNAMO_LOCAL = %s" % (app.config['DYNAMO_LOCAL'])

# timestamp ajax callback
@app.route('/_get_timestamp')
def get_timestamp():
    try:
        r = requests.get(app.config['TIMESTAMP_URL'], timeout=20)
        data = json.loads(r.text)
        logger.info('logger.info ' + r.text) # this shows up in cloudwatch
        app.logger.info('app.logger.info ' + r.text) # this shows up locally
        print('print ' + r.text) # this shows up in both but w/o decoration
        return data['timestamp']
    except requests.exceptions.RequestException as e:
        app.logger.error(e)
        return 'Timestamp unavailable'

# timestamp does not show up on staging unless end of url has slash. Should '/'
# redirect to '/index.html'?
@app.route('/')
@app.route('/index.html')
@app.route('/index.htm')
def index():
    return render_template('index.html')

@app.route('/favs')
def favs():
    table = dynamodb.Table('favs')
    response = table.scan()
    favs = response['Items']
    return render_template('favs.html', favs=favs)


@app.cli.command('initdb')
def initdb_command():
    print("DYNAMO_LOCAL = %s" % (app.config['DYNAMO_LOCAL']))
    table = dynamodb.create_table(
        TableName = 'favs',
        KeySchema = [
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions = [
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput = {
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='favs')

    table.put_item(
        Item = {
            'name': 'bloom',
            'url': 'https://www.bloomberg.com',
        }
    )

    print(table.item_count)

    response = table.scan()
    favs = response['Items']
    print(favs)

# We only need this for local development.
#if __name__ == '__main__':
#    app.run()
