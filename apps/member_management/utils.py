import bcrypt

def encrypt_password(password):
    """
    Encrypts the provided password using bcrypt.
    """
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')


def check_password(provided_password, stored_hashed_password):
    """
    Checks if the provided password matches the stored hashed password.
    """
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hashed_password.encode('utf-8'))