from decorators.decorators import verify_student_claim
from models.GroupModel import GroupModel
from flask_cors import cross_origin
from flask import (
    Blueprint, request, jsonify, g
)

# Create a Blueprint for the auth routes
bp = Blueprint('students', __name__, url_prefix='/students')

# ------------------- Student Routes -------------------#


@bp.route('/groups', methods=['POST'])
@cross_origin()
@verify_student_claim
def get_student_groups():
    """Get all the groups where the student is a member of

    Returns:
        json: A JSON object containing the groups of the student
    """

    try:
        student_uid = g.uid
        groups = GroupModel.get_student_groups(student_uid)
        return jsonify(groups), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@bp.route('/joingroup', methods=['POST'])
@cross_origin()
@verify_student_claim
def join_group():
    """Join a group for a student and returns the group confirmation

    Returns:
        JSON: A JSON object containing the confirmation of the group joined
    """
    try:

        # Get the teacher's uid from the request context stored by the verify_teacher_claim decorator
        student_uid = g.uid
        access_token = request.json.get('accessToken')
        group_joined = GroupModel.join_group(access_token, student_uid)
        return jsonify(group_joined), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
