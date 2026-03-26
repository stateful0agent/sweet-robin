import sys
import os


def set_secret(key, value):
    secrets = {}
    if os.path.exists(".env"):
        with open(".env", "r") as f:
            for line in f:
                if "=" in line:
                    k, v = line.strip().split("=", 1)
                    secrets[k] = v

    secrets[key] = value

    with open(".env", "w") as f:
        for k, v in secrets.items():
            f.write(f"{k}={v}\n")


if __name__ == "__main__":
    if len(sys.argv) == 3:
        set_secret(sys.argv[1], sys.argv[2])
