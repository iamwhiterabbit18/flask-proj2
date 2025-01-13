from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from website.Models.User import User
from website.schemas import UserSchema

users = Blueprint('users', __name__)

@users.route('/users', methods=['GET'])
@jwt_required()
def get_users():
  claims = get_jwt()
  if not claims['is_admin']:
    return jsonify({
      "message": "Unauthorized.",
      "error": "unauthorized"
    }), 401
  page = request.args.get('page', default=1, type=int)
  per_page = request.args.get('per_page', default=3, type=int)
  users = User.query.paginate(
    page = page,
    per_page = per_page
  )

  result = UserSchema().dump(users, many=True)

  return jsonify({
    "message": "All users.",
    "users": result
  }), 200