from cryptography.fernet import Fernet
from tensorflow import keras

def encrypt_parameters(model):
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)

    # Encrypting the model
    model_bytes = model.to_json().encode('utf-8')
    encrypted_model_bytes = cipher_suite.encrypt(model_bytes)
    # Save the encrypted model and key
    with open('encrypted_model.json', 'wb') as f:
        f.write(encrypted_model_bytes)
    with open('cipher_suite.json', 'wb') as k:
        k.write(key)

def decrypt():
    with open('encrypted_model.json', 'rb') as f:
        encrypted_model_bytes = f.read()
        key = open('cipher_suite.json')
        cipher_suite = Fernet(key.read())
        decrypted_model_bytes = cipher_suite .decrypt(encrypted_model_bytes)
        decrypted_model_json = decrypted_model_bytes.decode('utf-8')
        model = keras.models.model_from_json(decrypted_model_json)
    return model