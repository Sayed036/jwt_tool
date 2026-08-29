import argparse

from parser import parse_jwt
from checks.weak_key import check_weak_key


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

        check_weak_key(
            result["signing_input"],
            result["signature"],
            args.wordlist
        )

    except ValueError as error:

        print(f"\n[-] Error: {error}")


if __name__ == "__main__":
    main()