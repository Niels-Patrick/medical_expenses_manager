from cryptography.fernet import Fernet

fernet = Fernet('QZag_vDmlUwshopblUOkEONqD6d5UMDBA0syEPKAnWE=')

# Encrypt and decrypt an email manually for testing
test_email = "test@example.com"
encrypted_email = fernet.encrypt(test_email.encode())  # Encrypt the test email
decrypted_email = fernet.decrypt(encrypted_email).decode()  # Decrypt and get the original email

print(f"Original Email: {test_email}")
print(f"Encrypted Email: {encrypted_email}")
print(f"Decrypted Email: {decrypted_email}")