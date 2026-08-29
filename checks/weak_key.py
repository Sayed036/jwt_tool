from utils.crypto import calculate_hs256_signature


def check_weak_key(signing_input, original_signature, wordlist_path=None):

    if wordlist_path is None:
        wordlist_path = "wordlists/jwt_secrets.txt"

    with open(wordlist_path, "r", encoding="latin-1") as file:
        wordlist = file.readlines()

    for secret in wordlist:

        secret = secret.strip()

        if not secret:
            continue

        generated_signature = calculate_hs256_signature(
            signing_input,
            secret
        )

        if generated_signature == original_signature:

            print(f"\n[+] Weak signing key found: {secret}")

            return

    print("\n[-] Weak signing key not found")