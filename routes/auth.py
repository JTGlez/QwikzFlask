from flask import (Blueprint, request, jsonify, g)
from flask_cors import cross_origin
from firebase_admin import auth
from decorators.decorators import verify_token
from models.TeacherModel import TeacherModel
from models.StudentModel import StudentModel

# Create a Blueprint for the auth routes
bp = Blueprint('auth', __name__, url_prefix='/auth')

# ------------------- Auth Routes -------------------#


@bp.route('/register', methods=["POST"])
@cross_origin()
@verify_token
def register():
    """ 
    Retrieves the user's information and sets the custom claims for the user.

    :return: The user's information and the custom claims set.
    """

    # Get the user's information from the request context stored by the verify_token decorator
    uid = g.uid
    accountType = request.json.get('accountType')

    # Set the user with the custom claims
    auth.set_custom_user_claims(uid, {'accountType': accountType})

    # Register the user uid in the database with the accountType
    if accountType == 'teacher':
        TeacherModel.register_teacher(uid)
    else:
        StudentModel.register_student(uid)

    # Generate a new access token with the custom claim attached
    custom_token = auth.create_custom_token(uid)

    # Decode the custom token to a string
    custom_token_str = custom_token.decode('utf-8')

    response_body = {
        "customToken": custom_token_str
    }

    return jsonify(response_body)


@bp.route('/verify', methods=["POST"])
@cross_origin()
@verify_token
def verify_custom_claim():
    """Using Firebase SDK verifies the custom claims of the user declared in the token.

    return: A boolean value indicating if the user has the custom claim or not.
    """

    # Get the user's information from the request context stored by the verify_token decorator
    token = g.token
    accountType = request.json.get('accountType')

    # Get the user's custom claims
    custom_claims = auth.verify_id_token(token)

    # Check if the server and client custom claims match
    claims_match = custom_claims.get('accountType') == accountType

    print(custom_claims.get('accountType'), accountType)
    print('¿Hacen match?', claims_match)

    response_body = {
        "ok": claims_match
    }

    return jsonify(response_body)
