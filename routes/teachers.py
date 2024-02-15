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


@bp.route('/groups', methods=['POST'])
@cross_origin()
@verify_teacher_claim
def get_groups():
    """Get all the groups of a teacher

    Returns:
        JSON: A JSON object containing the groups of the teacher
    """
    # Get the teacher's uid from the request context stored by the verify_teacher_claim decorator
    teacher_uid = g.uid
    print(teacher_uid)
    try:
        groups = GroupModel.get_groups(teacher_uid)
        return jsonify(groups), 200
    except Exception as e:
        # If an error occurs, return a 500 server side error
        return jsonify({"error": str(e)}), 500
    
@bp.route('/creategroup', methods=['POST'])
@cross_origin()
@verify_teacher_claim
def create_group():
    """Creates a group for a teacher and returns the group confirmation

    Returns:
        JSON: A JSON object containing the confirmation of the group creation
    """
    try:

        # Get the teacher's uid from the request context stored by the verify_teacher_claim decorator
        teacher_uid = g.uid
        group_name = request.json.get('groupName')
        group_code = request.json.get('key')

        group_created = GroupModel.create_group(teacher_uid, group_name, group_code)
        return jsonify(group_created), 200
    
    except Exception as e:
        # If an error occurs, return a 500 server side error
        print(e)
        return jsonify({"error": str(e)}), 500