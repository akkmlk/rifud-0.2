from werkzeug.security import generate_password_hash

hashed = generate_password_hash("budi123")
print(hashed)