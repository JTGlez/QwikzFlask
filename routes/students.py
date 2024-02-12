from decorators.decorators import verify_student_claim, verify_teacher_claim
from flask_cors import cross_origin
from flask import (
    Blueprint, request, jsonify, g
)

# Create a Blueprint for the auth routes
bp = Blueprint('students', __name__, url_prefix='/students')

# ------------------- Auth Routes -------------------#

@bp.route('/register', methods=["POST"])
@cross_origin()
def register():
    """_summary_

    Returns:
        _type_: _description_
    """

    # Calls the JSON web token from the request
    result = check_token(request)

    return "Me llamaron"