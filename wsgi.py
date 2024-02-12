from app import create_app
import firebase_admin
from firebase_admin import credentials
import os
import stat

# Build the absolute path to the credentials file
cred_path = os.path.join('/opt', 'credentials.json')
print("Attempting to load credentials from:", cred_path)

if os.path.exists(cred_path):
    print("Credentials file exists.")
else:
    print("Credentials file does not exist.")

print("Checking if credentials file exists at:", cred_path)
if os.path.exists(cred_path):
    print("Credentials file found.")
    try:
        cred = credentials.Certificate(cred_path)
        print("Credentials loaded successfully.")
    except Exception as e:
        print("Failed to load credentials:", e)
else:
    print("Credentials file not found.")

permissions = stat.filemode(os.stat(cred_path).st_mode)
print("File permissions:", permissions)

# Load the credentials from the specified path
try:
    cred = credentials.Certificate(cred_path)
except Exception as e:
    print("Failed to load credentials:", e)

# Firebase configuration
default_app = firebase_admin.initialize_app(cred)

# Create the app
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)