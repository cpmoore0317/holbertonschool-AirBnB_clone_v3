#!/usr/bin/python3
"""places_reviews.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """Get information for all reviews of a place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in storage.all(Review).values() if review.place_id == place_id]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get information for the specified review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review based on its review_id."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Create a new review for a place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    user = storage.get(User, request.get_json()['user_id'])
    if user is None:
        abort(404)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    review = Review(place_id=place_id, **request.get_json())
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Update a review."""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, attr, val)
    review.save()
    return jsonify(review.to_dict())
