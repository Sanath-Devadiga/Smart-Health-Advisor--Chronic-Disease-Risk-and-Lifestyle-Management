# AES 256 Encryption Module for storing prediction history securely
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.backends import default_backend
import os
import base64
import json

class AES256Encryption:
    # AES 256 GCM encryption class for encrypting and decrypting prediction data
    
    def __init__(self, username):
        # Initialize encryption with username-based key derivation
        self.username = username

        self.key = self._derive_key(username)
        self.backend = default_backend()
    
    def _derive_key(self, username):
        
        import hashlib
        
        key_material = username.encode('utf-8')
        
        key = hashlib.sha256(key_material).digest()
        return key
    
    def encrypt(self, data):
        # Encrypt data using AES-256-GCM (data: dict or string, returns: base64 encoded encrypted data with nonce)
        # Convert data to JSON string if it's a dict
        if isinstance(data, dict):
            data_str = json.dumps(data)
        else:
            data_str = str(data)
        
        # Generate a random nonce (12 bytes for GCM)
        nonce = os.urandom(12)
        
        # Create AESGCM cipher
        aesgcm = AESGCM(self.key)
        
        # Encrypt the data
        ciphertext = aesgcm.encrypt(nonce, data_str.encode('utf-8'), None)
        
        # Combine nonce and ciphertext, then base64 encode
        encrypted_data = nonce + ciphertext
        encoded_data = base64.b64encode(encrypted_data).decode('utf-8')
        
        return encoded_data
    
    def decrypt(self, encrypted_data):
        # Decrypt data using AES-256-GCM (encrypted_data: base64 encoded data, returns: dict or string)
        try:
            # Decode from base64
            encrypted_bytes = base64.b64decode(encrypted_data.encode('utf-8'))
            
            # Extract nonce (first 12 bytes) and ciphertext
            nonce = encrypted_bytes[:12]
            ciphertext = encrypted_bytes[12:]
            
            # Create AESGCM cipher
            aesgcm = AESGCM(self.key)
            
            # Decrypt the data
            decrypted_bytes = aesgcm.decrypt(nonce, ciphertext, None)
            decrypted_str = decrypted_bytes.decode('utf-8')
            
            # Try to parse as JSON, return as string if it fails
            try:
                return json.loads(decrypted_str)
            except json.JSONDecodeError:
                return decrypted_str
                
        except Exception as e:
            raise ValueError(f"Decryption failed: {str(e)}")


def encrypt_prediction_data(username, inputs_dict, prediction_result):

    encryption = AES256Encryption(username)
    data = {
        'inputs': inputs_dict,
        'prediction': prediction_result
    }
    return encryption.encrypt(data)


def decrypt_prediction_data(username, encrypted_data):
   
    encryption = AES256Encryption(username)
    return encryption.decrypt(encrypted_data)

