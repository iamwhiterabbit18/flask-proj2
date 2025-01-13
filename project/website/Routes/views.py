from flask import Blueprint, render_template
from flask_jwt_extended import jwt_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
def landing():
  return render_template('landing.html', user=None)

@views.route('/home')
@jwt_required()
def home():
  current_user = get_jwt_identity()
  return render_template('home.html', user=current_user)
