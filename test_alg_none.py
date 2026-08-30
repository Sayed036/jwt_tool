from checks.alg_none import generate_alg_none_tokens


token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWV9.eeh23SpHL4YlJ5v1JoF4QsIARiTW5jIhmk--RnxW1Ls"

tokens = generate_alg_none_tokens(token)

for token in tokens:
    print(token)
    print()