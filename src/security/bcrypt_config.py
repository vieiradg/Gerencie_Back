from flask_bcrypt import bcrypt
from dotenv import load_dotenv

load_dotenv()
import os

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw((password.encode("utf-8")), salt)
    return hashed.decode("utf-8")

def check_password(hashed_password, user_password):
    return bcrypt.checkpw(hashed_password.encode("utf-8"), user_password.encode("utf-8"))
