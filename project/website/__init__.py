from flask import Flask, jsonify

from .extensions import db, jwt

from dotenv import load_dotenv
from os import path, getenv

from .Routes.views import views
from .Routes.auth import auth
from .Routes.users import users

from website.Models.User import User


def create_app():

    load_dotenv()

    app = Flask(__name__)
    app.config['DEBUG'] = True
    app.config['SECRET_KEY'] = getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('SQLALCHEMY_DATABASE_URI')
    DB_NAME = getenv('DB_NAME')

    #init/register extentions 
    db.init_app(app)
    jwt.init_app(app)

    # register blueprints
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')

    #get user from jwt token
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jtw_data):
      identity = jtw_data['sub']
      return User.query.filter_by(username=identity).one_or_none()
    
    #additional claims
    @jwt.additional_claims_loader
    def make_additional_claims(identity):
      if identity == 'Gene':
        return {
          "is_admin": True
        }
      return {
        "is_admin": False
      }
    
    #jtw error handler
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
      return jsonify({
        "message": "Token has expired.",
        "error": "token_expired"
      }), 401
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
      return jsonify({
        "message": "Signature verification failed.",
        "error": "invalid_token"
      }), 401
    @jwt.unauthorized_loader
    def missing_token_callback(error):
      return jsonify({
        "message": "Request does not contain an access token.",
        "error": "authorization_required"
      }), 401

    #create database and tables
    from .Models.User import User
    create_database(app, DB_NAME)

    return app

def create_database(app, db_name):
  with app.app_context():
    if not path.exists('website/' + db_name):
      db.create_all()
      print('Created Database!')