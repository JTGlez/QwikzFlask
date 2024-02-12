from decorators.decorators import verify_token, verify_student_claim, verify_teacher_claim
from flask_cors import cross_origin
from flask import (
    Blueprint, request, jsonify, g
)
from firebase_admin import auth

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

    # Get the user's information from the request
    uid = g.uid
    accountType = request.json.get('accountType')

    # Set the user with the custom claims
    auth.set_custom_user_claims(uid, {'accountType': accountType})

    # Force token refresh
    auth.revoke_refresh_tokens(uid)

    # Generate a new access token with the custom claim attached
    custom_token = auth.create_custom_token(uid)

    # Decode the custom token to a string
    custom_token_str = custom_token.decode('utf-8')

    print(custom_token_str)

    response_body = {
        "uid": uid,
        "accountType": accountType,
        "customToken": custom_token_str
    }

    return jsonify(response_body)