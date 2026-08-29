# to check the jwt tokens valid or not....

import base64 
import json

def decode_base64url(data):
    padding = '=' * (-len(data) % 4)
    data += padding

    decoded = base64.urlsafe_b64decode(data)
    return decoded.decode("utf-8")

def parse_jwt(token):
    parts = token.split(".")

    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    header = json.loads(decode_base64url(parts[0]))
    payload = json.loads(decode_base64url(parts[1]))
    signature = parts[2]

    signing_input = parts[0] + "." + parts[1]

    return {
        "header": header,
        "payload" : payload,
        "signature" : signature,
        "signing_input" : signing_input
    }
