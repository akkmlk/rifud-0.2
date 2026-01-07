from werkzeug.security import generate_password_hash

hashed = generate_password_hash("siti123")
print(hashed)