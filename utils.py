import os


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "Cookie": "",
    "Host": "elective.pku.edu.cn",
    "Origin": "https://elective.pku.edu.cn",
    "Referer": "",
    "Content-Type": "application/x-www-form-urlencoded",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}
out_dir = "out/"

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
