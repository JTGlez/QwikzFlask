from app import create_app
import firebase_admin
from firebase_admin import credentials
cred = credentials.Certificate('./credentials.json')

# Firebase configuration
default_app = firebase_admin.initialize_app(cred)

# Create the app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)