from utils.crypto import calculate_hs256_signature


def check_weak_key(
    signing_input,
    original_signature,
    wordlist_path
):

    try:

        with open(wordlist_path, "r", encoding="latin-1", errors="ignore") as file:
            wordlist = file.readlines()

    except FileNotFoundError:

        print(f"\n[-] Wordlist not found: {wordlist_path}")
        return

    print(f"\n[*] Using wordlist: {wordlist_path}")

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