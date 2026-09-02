import argparse
from checks.alg_none import (
    generate_alg_none_tokens,
    send_token,
    get_baseline_response,
    validate_baseline,
    analyze_response
)

from parser import parse_jwt
from checks.weak_key import check_weak_key
from checks.unverified_signature import run_unverified_signature_scan


def show_menu():

    print("\n========== JWT Security Scanner by f1r350ul ==========\n")

    print("[1] Scan Weak Secret Key")
    print("[2] Scan Algorithm None")
    print("[3] Scan Unverified Signature")

    print()


def main():
    parser = argparse.ArgumentParser(
        description="JWT Security Scanner",
        usage="python3 jwt_tool.py <JWT_TOKEN>"
    )

    parser.add_argument(
        "token",
        help="JWT token to scan"
    )

    parser.add_argument(
        "-w",
        "--wordlist",
        help="Path to custom wordlist"
    )

    args = parser.parse_args()

    try:
        result = parse_jwt(args.token)

        print("\n[+] JWT parsed successfully")

        show_menu()

        choice = input("Enter your choice: ")

        if choice == "1":

            print("\n[*] Scanning for weak secret key...")

            if args.wordlist:

                wordlist_path = args.wordlist

                print(f"\n[*] Using custom wordlist: {wordlist_path}")

            else:

                print("\n[*] Wordlist selection:")
                print("[1] Use default wordlist")
                print("[2] Use custom wordlist")

                wordlist_choice = input("Enter your choice: ")

                if wordlist_choice == "1":

                    wordlist_path = "wordlists/jwt_secrets.txt"

                elif wordlist_choice == "2":

                    wordlist_path = input(
                        "Enter path to wordlist: "
                    )

                else:

                    print("\n[-] Invalid wordlist choice")
                    return

            check_weak_key(
                result["signing_input"],
                result["signature"],
                wordlist_path
            )

        elif choice == "2":

            print("\n[*] Algorithm None scan selected")

            target_url = input("Target URL: ")

            print("\nJWT Location:")
            print("[1] Authorization Header")
            print("[2] Cookie")

            location_choice = input("Enter your choice: ")

            if location_choice == "1":

                location = "header"
                cookie_name = None

            elif location_choice == "2":

                location = "cookie"
                cookie_name = input("Cookie name: ")

            else:

                print("\n[-] Invalid JWT location")
                return

            print("\n[*] Testing original JWT...")

            baseline_response = get_baseline_response(
                target_url,
                args.token,
                location,
                cookie_name
            )

            print(
                f"[+] Baseline Status Code: "
                f"{baseline_response.status_code}"
            )

            if not validate_baseline(baseline_response):
                return

            print("\n[*] Testing Algorithm None variants...")

            alg_none_tokens = generate_alg_none_tokens(args.token)

            for algorithm, token in alg_none_tokens:

                print(f"\n[*] Testing alg: {algorithm}")

                response = send_token(
                    target_url,
                    token,
                    location,
                    cookie_name
                )

                print(f"    Status Code: {response.status_code}")
                print(f"    Response Size: {len(response.content)} bytes")

                if analyze_response(
                    baseline_response,
                    response
                ):

                    print("\n[!] Potentially accepted!")
                    print(f"    Algorithm: {algorithm}")
                    print(f"\n    Token: {token}")

                else:

                    print("\n[-] Rejected")

        elif choice == "3":
            print("\n=== Unverified Signature Scan ===")

            url = input("Enter target URL: ").strip()

            print("\nWhere is the JWT located?")
            print("[1] Authorization Header")
            print("[2] Cookie")

            location_choice = input("Select option: ").strip()

            if location_choice == "1":

                location = "header"
                cookie_name = None

            elif location_choice == "2":

                location = "cookie"
                cookie_name = input("Enter cookie name: ").strip()

            else:

                print("[-] Invalid option")
                return

            run_unverified_signature_scan(
                args.token,
                url,
                location,
                cookie_name
            )

        else:

            print("\n[-] Invalid choice")

    except ValueError as error:
        print(f"\n[-] Error: {error}")


if __name__ == "__main__":
    main()