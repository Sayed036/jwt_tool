from checks.alg_none import send_token


url = input("Target URL: ")
token = input("JWT token: ")

response = send_token(url, token)

print("\nStatus Code:", response.status_code)
print("Response Length:", len(response.text))