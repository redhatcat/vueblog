from app import app
from models.user import User, hash_password
from flask import abort, jsonify, request

from webargs import fields, validate
from webargs.flaskparser import use_args

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_optional,
    jwt_required
)

@app.route("/api/users/create", methods=['POST'])
@jwt_optional
@use_args({
    'username': fields.String(required=True, validate=validate.Length(max=32)),
    'password': fields.String(required=True, validate=validate.Length(max=32)),
})
def user_create(args):
    requires_auth = True
    # Check if there are user records and if there is not, let this action bypass auth.
    # This allows the first user to create their account.
    if User.objects()[:1].count() < 1:
        requires_auth = False
    if requires_auth is True:
        current_user = get_jwt_identity()
        if current_user is None:
            abort(403)
        username = current_user.get('username')
        if username is None:
            abort(403)
    username = args.get('username')
    password = args.get('password')
    # TODO check for existing user here
    # TODO check password complexity here
    hashed_password = hash_password(password)
    user = User(username=username, password=hashed_password)
    user.save()
    # TODO If first user created, throw JWT in response
    return jsonify(dict(result='user ({}) created'))

@app.route("/api/users/empty", methods=['POST'])
def user_count():
    if User.objects()[:1].count() < 1:
        return jsonify(dict(result=True))
    return jsonify(dict(result=False))

@app.route('/api/users/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.objects(username=username, password=hash_password(password)).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=dict(username=username))
    return jsonify(access_token=access_token, username=username), 200

@app.route('/api/users/renew', methods=['POST'])
@jwt_required
def renew():
    current_user = get_jwt_identity()
    username = current_user.get('username')
    if username is None:
        abort(403)
    access_token = create_access_token(identity=dict(username=username))
    return jsonify(access_token=access_token, username=username), 200
