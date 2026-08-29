import base64
import json
import hmac
import hashlib


header = {
    "alg": "HS256",
    "typ": "JWT"
}

payload = {
    "sub": "1234567890",
    "name": "John Doe",
    "admin": True
}

secret = "hello"


def base64url_encode(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


encoded_header = base64url_encode(
    json.dumps(header, separators=(",", ":")).encode()
)

encoded_payload = base64url_encode(
    json.dumps(payload, separators=(",", ":")).encode()
)

signing_input = encoded_header + "." + encoded_payload


signature = hmac.new(
    secret.encode(),
    signing_input.encode(),
    hashlib.sha256
).digest()

encoded_signature = base64url_encode(signature)


token = signing_input + "." + encoded_signature

print("Test JWT:")
print(token)