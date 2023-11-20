#!/usr/bin/python3
"""states.py"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """Retrieve information for all states.

    Returns:
        Response: JSON response containing information for all states.

    """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """Retrieve information for the specified state.

    Args:
        state_id (str): The ID of the state.

    Returns:
        Response: JSON response containing information for the specified state.

    Raises:
        404: If the state with the given ID is not found.

    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state based on its state_id.

    Args:
        state_id (str): The ID of the state to be deleted.

    Returns:
        Response: Empty JSON response.

    Raises:
        404: If the state with the given ID is not found.

    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})
