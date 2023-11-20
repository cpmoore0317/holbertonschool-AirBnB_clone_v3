#!/usr/bin/python3
"""index.py to connect to API"""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
from models import storage


# Dictionary to map endpoint names to corresponding model classes
hbnbText = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', strict_slashes=False)
def hbnbStatus():
    """Route to get the status of the API.

    Returns:
        Response: JSON response with the status 'OK'.

    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def hbnbStats():
    """Route to get statistics about the number of objects in storage.

    Returns:
        Response: JSON response with a dictionary containing counts
        for each model type.

    Notes:
        The dictionary includes counts for 'amenities', 'cities', 'places',
        'reviews', 'states', and 'users'.

    """
    return_dict = {}
    for key, value in hbnbText.items():
        return_dict[key] = storage.count(value)
    return jsonify(return_dict)

if __name__ == "__main__":
    pass
