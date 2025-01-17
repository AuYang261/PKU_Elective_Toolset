import requests
import json
from tkinter import messagebox
import time
import utils

url = "https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/supplement/refreshLimit.do"
referer = "https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/electiveWork/showResults.do?xh=%s"
course = {
    # "面向金融的Python": {
    #     "index": "16",
    #     "seq": "yjkc20180700028066",
    # },
    "面向对象技术": {
        "index": "5",
        "seq": "YKC01711200AT0001238",
    },
    # "Python": {
    #     "index": "39",
    #     "seq": "yjkc20200800035751",
    # },
}


def main():
    xh = utils.get_xh()
    headers = utils.headers.copy()
    headers["Referer"] = referer % xh
    headers["Cookie"] = utils.get_cookie()
    while True:
        for course_name, data in course.items():
            data["xh"] = xh
            while True:
                try:
                    response = requests.post(url, headers=headers, data=data)
                    j = json.loads(response.text)
                    if j.get("limitNum") is not None:
                        break
                except:
                    print(response.text)
                time.sleep(1)
            print(course_name, response.text)
            with open("log.txt", "a") as f:
                f.write(f"{course_name}: {response.text}\n")
            if j["electedNum"] != j["limitNum"]:
                messagebox.showinfo("选课提醒", f"{course_name} 有空位了！")
            else:
                time.sleep(1)


if __name__ == "__main__":
    main()
