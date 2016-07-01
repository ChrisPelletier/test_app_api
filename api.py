from flask import jsonify, request, abort
from sample_app import app, connection
import sample_app.resources.token as token
import datetime


@app.route('/user', methods=['POST',"GET"])
def new_user():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        if connection.User.find_one({"username":username}):
            return jsonify({"error": "Username already exists."}), 400
        next_user_id = connection.User.find_one({"username":"next_user_id", "password_hash":"thisisapassword"})
        new_user_doc = connection.User()
        new_user_doc['id'] = next_user_id.id + 1
        new_user_doc['username'] = username
        new_user_doc['password_hash'] = new_user_doc.hash_password(password)
        new_user_doc.validate()
        if len(new_user_doc.validation_errors) > 0:
            errors = []
            for key, value in new_user_doc.validation_errors.iteritems():
                for error in value:
                    errors.append(error[0])
            if len(errors) > 1:
                return jsonify({"errors": errors}), 400
            else:
                return jsonify({"error": errors[0]}), 400
        else:
            new_user_doc.save()
        if new_user_doc:
            next_user_id['id'] += next_user_id.id + 1
            next_user_id.save()
            return jsonify({"id":new_user_doc["id"], "username":new_user_doc["username"]}), 201
        else:
            return jsonify({"error": "Could not create user"}), 400
    elif request.method == 'GET':
        if 'Authorization' not in request.headers:
            return jsonify({"error": "Request is missing Authorization header."})
        decoded_token = token.decode_token(request.headers['Authorization'])
        if 'error' in decoded_token:
            return jsonify({"error": "invalid_token"}), 401
        user = connection.User.find_one({"username": decoded_token['username'], "id": decoded_token['user_id']})
        return jsonify({
            "username": user.username,
            "id": user.id,
            "created": user.created,
            "updated": user.updated,
            "last_login": user.last_login
        }), 200
    else:
        return jsonify({"error": request.method + 'is not allowed.'}), 400


@app.route('/login', methods=['POST'])
def new_jwt():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')
        user = connection.User.find_one({"username":username})
        if user.verify_password(password):
            new_token = token.create_jwt(user)
            user['last_login'] = datetime.datetime.utcnow()
            user.save()
            return jsonify({"token": new_token}), 201
        else:
            return jsonify({"error": "The username and password provided do not match"}), 401
    else:
        return jsonify({"error": request.method + 'is not allowed.'}), 400

