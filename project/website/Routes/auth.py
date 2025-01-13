from flask import Blueprint, render_template, jsonify, request, redirect, url_for
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt, current_user
from website.Models.User import User
from website.Models.Auth import RegisterForm, LoginForm

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == 'POST':
        data = request.get_json()
        user = User.get_user(username=data['username'])
        if user is not None:
            return jsonify({
                "message": "User already exists!",
            })
        new_user = User(
            username=data['username'], 
            password=data['password'])

        new_user.save()
        # view created user
        return jsonify({
            "message": "User created!",
            "id": new_user.id,
            "username": new_user.username,
            "password": new_user.password
            })
    return render_template('signup.html', form=form)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            if not username or not password:
                return jsonify({"error": "Username and password are required"}), 400
            user = User.get_user(username=username)
            if user is None:
                return jsonify({
                    "error": "Invalid username or password!"
                }), 400
            if user.check_password(password=password):
                access_token = create_access_token(identity=user.username)
                refresh_token = create_refresh_token(identity=user.username)
                return jsonify({
                    "message": "User logged in!",
                    "id": user.id,
                    "username": user.username,
                    "tokens": {
                        "access":access_token,
                        "refresh": refresh_token
                    },
                    "redirect_url": "/home"
                    }), 200
            else:
                return jsonify({
                    "error": "Invalid username or password!"
                }), 400
        except Exception as e:
            print(f"Login error: {str(e)}")  # Add server-side logging
            return jsonify({"error": "Server error occurred"}), 500
            
    return render_template('login.html', form=form)

@auth.route('/whoami', methods=['GET'])
@jwt_required()
def whoami():
    return jsonify({
        "message": "message",
        "user_details": {
            "username": current_user.username,
        }
    }), 200

@auth.route('/logout')
def logout():
  return render_template('login.html', user=None)