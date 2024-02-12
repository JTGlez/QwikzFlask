
from functools import wraps
from flask import (
    request, jsonify, g
)
from firebase_admin import credentials, auth
cred = credentials.Certificate('./credentials.json')

# Decorator to verify the token
def verify_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the token from the request header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}),  403

        # Extract the token by removing the 'Bearer ' prefix
        token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else None
        if not token:
            return jsonify({'message': 'Invalid token format'}),  403

        # Verify the token and get the user's UID storing it in the request context
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
            # Almacena el uid del usuario en el contexto de la petición
            g.uid = uid
        except ValueError:
            return jsonify({'message': 'Token is invalid'}),  403

        return f(*args, **kwargs)

    return decorated_function

def verify_student_claim(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtén el encabezado de autorización
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}),   403

        # Extrae el token quitando el prefijo 'Bearer '
        token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else None
        if not token:
            return jsonify({'message': 'Invalid token format'}),   403

        # Verifica el token y obtén el UID del usuario
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
        except ValueError:
            return jsonify({'message': 'Token is invalid'}),   403

        # Obtiene los custom claims del usuario
        custom_claims = auth.get_custom_user_claims(uid)

        # Verifica si el usuario tiene el custom claim de "student"
        if 'student' not in custom_claims or not custom_claims['student']:
            return jsonify({'message': 'User is not a student'}),   403

        return f(*args, **kwargs)

    return decorated_function


def verify_teacher_claim(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Obtén el encabezado de autorización
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'message': 'Token is missing'}),   403

        # Extrae el token quitando el prefijo 'Bearer '
        token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else None
        if not token:
            return jsonify({'message': 'Invalid token format'}),   403

        # Verifica el token y obtén el UID del usuario
        try:
            decoded_token = auth.verify_id_token(token)
            uid = decoded_token['uid']
        except ValueError:
            return jsonify({'message': 'Token is invalid'}),   403

        # Obtiene los custom claims del usuario
        custom_claims = auth.get_custom_user_claims(uid)

        # Verifica si el usuario tiene el custom claim de "teacher"
        if 'teacher' not in custom_claims or not custom_claims['teacher']:
            return jsonify({'message': 'User is not a teacher'}),   403

        return f(*args, **kwargs)

    return decorated_function