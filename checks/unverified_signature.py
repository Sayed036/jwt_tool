import requests


def tamper_signature(token):
    parts = token.split(".")

    if len(parts) != 3:
        raise ValueError("Invalid JWT format")

    header = parts[0]
    payload = parts[1]
    signature = parts[2]

    if not signature:
        raise ValueError("JWT does not contain a signature")

    if signature[0] == "A":
        tampered_signature = "B" + signature[1:]
    else:
        tampered_signature = "A" + signature[1:]

    return header + "." + payload + "." + tampered_signature


def send_token(url, token, location="header", cookie_name=None):

    if location == "header":
        headers = {
            "Authorization": f"Bearer {token}"
        }

        return requests.get(
            url,
            headers=headers,
            allow_redirects=False
        )

    elif location == "cookie":
        if not cookie_name:
            raise ValueError("Cookie name is required")

        cookies = {
            cookie_name: token
        }

        return requests.get(
            url,
            cookies=cookies,
            allow_redirects=False
        )

    else:
        raise ValueError("Invalid JWT location")


def get_baseline_response(url, original_token, location="header",
                          cookie_name=None):

    return send_token(
        url,
        original_token,
        location,
        cookie_name
    )


def analyze_response(baseline_response, tampered_response):

    baseline_status = baseline_response.status_code
    tampered_status = tampered_response.status_code

    baseline_size = len(baseline_response.content)
    tampered_size = len(tampered_response.content)

    print(f"\n[+] Original JWT   : {baseline_status} / {baseline_size} bytes")
    print(f"[+] Tampered JWT   : {tampered_status} / {tampered_size} bytes")

    if (
        baseline_status == tampered_status
        and baseline_size == tampered_size
    ):
        print("\n[!] Potentially unverified signature")
    else:
        print("\n[-] Signature appears to be verified")
        print("[-] Tampered JWT produced a different response")



# for testing the cookie flow.
def run_unverified_signature_scan(
    token,
    url,
    location="header",
    cookie_name=None
):
    print("\n[*] Testing original JWT...")

    baseline_response = get_baseline_response(
        url,
        token,
        location,
        cookie_name
    )

    print(
        f"[+] Original JWT : "
        f"{baseline_response.status_code} / "
        f"{len(baseline_response.content)} bytes"
    )

    print("\n[*] Tampering JWT signature...")

    tampered_token = tamper_signature(token)

    print("[+] Tampered JWT:")
    print(tampered_token)

    print("\n[*] Testing tampered JWT...")

    tampered_response = send_token(
        url,
        tampered_token,
        location,
        cookie_name
    )

    analyze_response(
        baseline_response,
        tampered_response
    )