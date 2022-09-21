from flask import Flask, Blueprint
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow # new

import os
import logging


load_dotenv(find_dotenv())
logging.basicConfig(level=logging.DEBUG)
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref

app = Flask(__name__)
CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@mariadb/meteor' #save in secret
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://67m5mprml48gste4jrs9:pscale_pw_y2VYmDfNDhWW3aOS2eRorSucsB6YSvshebmZB43yvHn@us-east.connect.psdb.cloud/meteor?ssl_ca=/etc/ssl/cert.pem' #save in secret
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) # new
ma = Marshmallow(app) # new

from meteor.household.route import household_blueprint

app.register_blueprint(household_blueprint, url_prefix='/household/api/v1')

db.create_all()