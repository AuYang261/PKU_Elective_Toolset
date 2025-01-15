import os


def get_cookie():
    if os.path.exists("cookie.txt"):
        with open("cookie.txt") as f:
            return f.read().strip()
    else:
        raise FileNotFoundError("cookie.txt not found")


def get_xh():
    if os.path.exists("xh.txt"):
        with open("xh.txt") as f:
            return f.read().strip()
    else:
        raise FileNotFoundError("xh.txt not found")
    