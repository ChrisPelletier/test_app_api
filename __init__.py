from flask import Flask, jsonify, abort, make_response, request, url_for
from mongokit import Connection
from sample_app.models.user import User
import sample_app.config as config
from flask_cors import CORS, cross_origin
from flask_admin import Admin


app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = config.DEBUG
app.config['MONGODB_HOST'] = config.MONGODB_HOST
# app.config['MONGOALCHEMY_DATABASE'] = 'sample_app'

connection = Connection(app.config['MONGODB_HOST'])
connection.register([User])

admin = Admin(app, name='Sample App', template_mode='bootstrap3')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


import api
_ = api

