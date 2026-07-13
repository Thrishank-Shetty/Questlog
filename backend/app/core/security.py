import bcrypt
def hashpassword(password):
    byte_password=password.encode('utf-8')
    salt=bcrypt.gensalt()
    hashpassword=bcrypt.hashpw(byte_password,salt)
    hash_password=hashpassword.decode('utf=8')
    return hash_password

def verifypassword(plainpassword,hashpassword):
    plainbyte=plainpassword.encode('utf-8')
    hashbyte=hashpassword.encode('utf-8')
    return bcrypt.checkpw(plainbyte,hashbyte)
    