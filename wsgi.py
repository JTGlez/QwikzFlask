from app import create_app
import firebase_admin
from firebase_admin import credentials
import os

# Build the absolute path to the credentials file
cred_path = os.path.join('/opt', 'credentials.json')

# Load the credentials from the specified path
try:
    cred = credentials.Certificate(cred_path)
except Exception as e:
    cred = credentials.Certificate('credentials.json')

# Firebase configuration
default_app = firebase_admin.initialize_app(cred)

# Create the app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
