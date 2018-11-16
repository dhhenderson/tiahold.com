import logging
import requests

from flask import current_app, Blueprint, render_template, json

from app.db import get_db

views = Blueprint('views', __name__)

# TODO: _get_timestamp does not work on staging unless '/staging' url has a
# slash on the end of it.
#
# Previously, these routes were included:
# @views.route('/index.html')
# @views.route('/index.htm')
# However, can impact web indexing/reporting/SEO tools. Clunky.
# So, just have the '/' route and add a 404 page w/ a link back to it.
# Others have set up 'catch all' routing: http://flask.pocoo.org/snippets/57/
# but this will override any 404 behavior that is desired.
@views.route('/')
def index():
    # print(current_app.url_map)
    return render_template('views/index.html')


@views.route('/favs')
def favs():
    table = get_db().Table('favs')
    response = table.scan()
    favs = response['Items']
    return render_template('views/favs.html', favs=favs)


@views.route('/_get_timestamp')
def get_timestamp():
    """Return timestamp for ajax callback"""
    # With this logger, messages flow from lambda to cloudwatch.
    logger = logging.getLogger()
    try:
        r = requests.get(current_app.config['TIMESTAMP_URL'], timeout=20)
        data = json.loads(r.text)
        # This shows up in cloudwatch
        logger.info('logger.info ' + r.text)
        # This shows up locally
        current_app.logger.info('app.logger.info ' + r.text)
        # This shows up in both but w/o decoration
        print('print ' + r.text)
        return data['timestamp']
    except requests.exceptions.RequestException as e:
        logger.error(e)
        current_app.logger.error(e)
        return 'Timestamp unavailable'

# Ongoing debate over error handler behavior:
# https://github.com/pallets/flask/issues/2841
# https://github.com/pallets/flask/issues/2778
# but a catch all Exception handler doesn't appear to step on 404 handler.
# It does, however, override the DEBUG mode browser stack dump behavior.
# This dumps the list of handlers and the Execption classes they are mapped to:
#    print(current_app.error_handler_spec)
# TODO: Should/can this be enabled only for production?
# @views.app_errorhandler(Exception)
# def unexpected_error(error):
#     return 'Internal Server Error', 500


@views.app_errorhandler(404)
def page_not_found(error):
    return render_template('views/404.html'), 404


@views.app_errorhandler(500)
def internal_server_error(error):
    return 'Internal Server Error', 500
