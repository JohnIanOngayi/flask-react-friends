#!/usr/bin/env python3

"""
Defines api routes
"""

from typing import Tuple
from app import app, db
from flask import Response, request, jsonify
from models import Friend
from uuid import uuid4


@app.route("/api", methods=["GET"], strict_slashes=False)
def index() -> Response:
    """
    GET /api/
    returns success payload if api is up
    """
    return jsonify({"status": "OK"})


@app.route("/api/friends", methods=["GET"], strict_slashes=False)
def get_friends() -> Response:
    """
    GET /api/friends
    returns all friends from db
    """
    friends = Friend.query.all()
    friends_json = [f.to_json() for f in friends]
    return jsonify(friends_json)


@app.route("/api/friends", methods=["POST"], strict_slashes=False)
def create_friend() -> Tuple[Response, int]:
    """
    POST /friends
    creates a new friend and returns success message
    """
    try:
        friend_dict = request.form.to_dict()
        name = friend_dict.get("name")
        role = friend_dict.get("role")
        description = friend_dict.get("description")
        gender = friend_dict.get("gender")

        required = ["name", "role", "gender", "description"]
        for field in required:
            if field not in friend_dict.keys():
                return jsonify({"error": f"missing required field {field}"}), 400
        # fetch avatar image based on gender
        if gender == "male":
            img_url = f"https://avatar.iran.liara.run/public/boy?username={name}"
        elif gender == "female":
            img_url = f"https://avatar.iran.liara.run/public/girl?username={name}"
        else:
            img_url = None

        new_friend = Friend(
            name=name,
            role=role,
            description=description,
            gender=gender,
            img_url=img_url,
        )
        db.session.add(new_friend)
        db.session.commit()
        return jsonify({"message": "friend successfully created"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/friends/<id: int>", methods=["DELETE"], strict_slashes=False)
def delete_friend():
    """Deletes friend matching id"""
    if id is None or not isinstance(id, int):
        return jsonify({ 'error': f'id must be a positive integer' })
    try:
        except:
            db.session.rollback()
            return jsonify()

