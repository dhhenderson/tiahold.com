import boto3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    app.cli.add_command(init_db_command)


def get_db():
    if 'db' not in g:
        if current_app.config['IS_DYNAMO_LOCAL']:
            g.db = boto3.resource('dynamodb',
                                  endpoint_url=current_app.config[
                                      'DYNAMO_LOCAL_URL'])
        else:
            g.db = boto3.resource('dynamodb')

    return g.db


@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_db():
    """Initialize the DB.

    # Exception thrown if table already exists.
    # Bouncing dynamodb-local container will drop database.
    """
    db = get_db()

    table = db.create_table(
        TableName='favs',
        KeySchema=[
            {
                'AttributeName': 'name',
                'KeyType': 'HASH'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'name',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait until the table exists.
    table.meta.client.get_waiter('table_exists').wait(TableName='favs')

    table.put_item(
        Item={
            'name': 'bloom',
            'url': 'https://www.bloomberg.com',
        }
    )

    print(table.item_count)
    response = table.scan()
    favs = response['Items']
    print(favs)
