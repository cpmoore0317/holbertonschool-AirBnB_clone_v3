#!/usr/bin/python3
"""users.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Get information for all users."""
    # Retrieve all users from storage and convert them to dictionaries.
    users = [user.to_dict() for user in storage.all("User").values()]
    return jsonify(users)

@app_views.route('/users/<string:user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Get information for the specified user."""
    # Retrieve a user based on user_id from storage.
    user = storage.get("User", user_id)
    if user is None:
        # If the user is not found, return a 404 error.
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<string:user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a user based on user_id."""
    # Retrieve a user based on user_id from storage.
    user = storage.get("User", user_id)
    if user is None:
        # If the user is not found, return a 404 error.
        abort(404)
    # Delete the user and save the changes to storage.
    user.delete()
    storage.save()
    return jsonify({})

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Create a new user."""
    # Check if the request contains JSON data.
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    # Check if 'email' and 'password' are present in the JSON data.
    if 'email' not in request.get_json() or 'password' not in request.get_json():
        return make_response(jsonify({'error': 'Missing email or password'}), 400)
    # Create a new User object and save it.
    user = User(**request.get_json())
    user.save()
    return make_response(jsonify(user.to_dict()), 201)

@app_views.route('/users/<string:user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Update a user."""
    # Retrieve a user based on user_id from storage.
    user = storage.get("User", user_id)
    if user is None:
        # If the user is not found, return a 404 error.
        abort(404)
    # Check if the request contains JSON data.
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    # Update user attributes based on the JSON data.
    for attr, val in request.get_json().items():
        if attr not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, attr, val)
    # Save the changes to the user.
    user.save()
    return jsonify(user.to_dict())
