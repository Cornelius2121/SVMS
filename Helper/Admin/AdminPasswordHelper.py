import hashlib
from Services.Admin.AdminService import select_password_from_admin_username


# This method checks the password from the student id
def check_admin_password(admin_username: str, given_password: str):
    hashed_given_password = hash_password(given_password)
    actual_hashed_password = select_password_from_admin_username(admin_username)
    if hashed_given_password == actual_hashed_password:
        return True, "Success"
    else:
        return False, "Password is not correct"


# Hashes a string password with MD5 and returns a hex string
def hash_password(password: str) -> str:
    hash_pw = hashlib.md5(password.encode())
    return str(hash_pw.hexdigest())
