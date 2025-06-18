"""Cryptography module.

This module generates an RSA key pair (private and public keys)
for encryption and decryption processes used within the application.
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

# Generate an RSA private key.
# public_exponent=65537 is a common choice for RSA.
# key_size=2048 is secure for most general purposes.
private_key: rsa.RSAPrivateKey = rsa.generate_private_key(public_exponent=65537, key_size=2048)

# Derive the public key from the private key.
public_key: rsa.RSAPublicKey = private_key.public_key()

# Serialize the public key to PEM format (Base64-encoded ASN.1 structure).
# This allows sharing the public key externally for encryption purposes.
public_pem: str = public_key.public_bytes(
    encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo
).decode()
