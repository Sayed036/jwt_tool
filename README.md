# jwt_tool

JWT Vulnerability Scanner tool.

## Features

- JWT Parsing
- Weak Secret Key Detection
- Algorithm None Detection
- Unverified Signature Detection
- Authorization Header support
- Cookie support
- Custom wordlist support

## Requirements

- Python 3
- `requests`

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd jwt_tool
```

Install the required dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

Run the tool by providing a JWT token:

```bash
python3 jwt_tool.py "<JWT_TOKEN>"
```

Example:

```bash
python3 jwt_tool.py "eyJhbGciOiJIUzI1NiJ9..."
```

## Available Scans

After providing the JWT, the tool provides the following options:

```text
[1] Scan Weak Secret Key
[2] Scan Algorithm None
[3] Scan Unverified Signature
```

### 1. Weak Secret Key

Attempts to identify weak JWT signing secrets using a wordlist.

The tool provides an option to use the default JWT secret wordlist or a custom wordlist.

### 2. Algorithm None

Tests whether the application incorrectly accepts JWTs using the `none` algorithm.

The tool supports testing JWTs supplied through:

- Authorization Header
- Cookie

### 3. Unverified Signature

Tests whether the application accepts a JWT with a tampered/invalid signature.

The original JWT is compared with the tampered JWT to identify potentially unverified signatures.

## Custom Wordlist

A custom wordlist can be provided using `-w` or `--wordlist`:

```bash
python3 jwt_tool.py "<JWT_TOKEN>" -w /path/to/wordlist.txt
```

Example:

```bash
python3 jwt_tool.py "<JWT_TOKEN>" -w /usr/share/wordlists/rockyou.txt
```

## Help

To view the available options:

```bash
python3 jwt_tool.py --help
```

### Options

**JWT Token**

The JWT token that you want to scan.

```bash
python3 jwt_tool.py "<JWT_TOKEN>"
```

**`-w, --wordlist`**

Use a custom wordlist for the Weak Secret Key scan.

```bash
python3 jwt_tool.py "<JWT_TOKEN>" -w /path/to/wordlist.txt
```

Example:

```bash
python3 jwt_tool.py "<JWT_TOKEN>" -w /usr/share/wordlists/rockyou.txt
```

### Example

```text
$ python3 jwt_tool.py "<JWT_TOKEN>"

========== JWT Security Scanner by f1r350ul ==========

[1] Scan Weak Secret Key
[2] Scan Algorithm None
[3] Scan Unverified Signature

Enter your choice:
```

Select the required scan from the menu and follow the instructions shown by the tool.


## Disclaimer

This tool is intended for security testing, learning, and authorized penetration testing only.

Do not use it against systems without proper authorization.