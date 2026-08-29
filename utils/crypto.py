
# generating signature for weak key, then we will compare with Original signature.  
import hmac
import hashlib
import base64


def calculate_hs256_signature(signing_input, secret):
    signature = hmac.new(
        secret.encode(),
        signing_input.encode(),
        hashlib.sha256
    ).digest()

    return base64.urlsafe_b64encode(signature).decode().rstrip("=")