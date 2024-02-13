from decorators.decorators import verify_teacher_claim
from flask_cors import cross_origin
from flask import (
    Blueprint, request, jsonify, g
)
from models.GroupModel import GroupModel

# Create a Blueprint for the auth routes
bp = Blueprint('teachers', __name__, url_prefix='/teachers')

# ------------------- Teacher Routes -------------------#

# Route to get all the groups of a teacher


@bp.route('/groups', methods=['GET'])
@cross_origin()
@verify_teacher_claim
def get_groups():
    """Get all the groups of a teacher

    Returns:
        JSON: A JSON object containing the groups of the teacher
    """
    try:
        groups = GroupModel.get_groups()
        return jsonify(groups), 200
    except Exception as e:
        # If an error occurs, return a 500 server side error
        return jsonify({"error": str(e)}), 500