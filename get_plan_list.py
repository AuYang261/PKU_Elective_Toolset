import utils
import requests
import json
import time
import re
from bs4 import BeautifulSoup
from itertools import zip_longest
import os

url1 = "https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/getCurriculmByForm.do"
url2 = "https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/queryCurriculum.jsp?netui_pagesize=syllabusListGrid%3B100&wlw-checkbox_key%3A%7BactionForm.queryDateFlag%7DOldValue=false&wlw-select_key%3A%7BactionForm.courseTime%7D=&wlw-select_key%3A%7BactionForm.courseTime%7DOldValue=true&netui_row=syllabusListGrid%3B{}00&wlw-select_key%3A%7BactionForm.courseDay%7DOldValue=true&deptIdHide=ALL&wlw-select_key%3A%7BactionForm.courseDay%7D=&%7BactionForm.courseName%7D=&wlw-select_key%3A%7BactionForm.deptID%7D=ALL&wlw-select_key%3A%7BactionForm.deptID%7DOldValue=true&%7BactionForm.courseID%7D="
referer = "https://elective.pku.edu.cn/elective2008/edu/pku/stu/elective/controller/courseQuery/CourseQueryController.jpf"


def main():
    if not os.path.exists(utils.out_dir):
        os.mkdir(utils.out_dir)
    headers = utils.headers.copy()
    headers["Referer"] = referer
    headers["Cookie"] = utils.get_cookie()
    response = requests.post(url1, headers=headers)
    match = re.search("Page [0-9] of ([0-9]+)", response.text)
    if match:
        total_page = int(match.group(1))
        print("total_page:", total_page)
    else:
        raise ValueError("Page number not found")
    bs = BeautifulSoup(response.text, "html.parser")
    with open(os.path.join(utils.out_dir, "plan_list.csv"), "w", encoding="gbk") as f:
        f.write(",".join(get_header(bs)) + "\n")
        for row in get_data(bs):
            f.write(",".join(row) + "\n")
        print("Page 1 done")
        for i in range(1, total_page):
            response = requests.get(url2.format(i), headers=headers)
            rows = get_data(BeautifulSoup(response.text, "html.parser"))
            for row in rows:
                f.write(",".join(row) + "\n")
            print(f"Page {i + 1} done")
            time.sleep(1)


def get_header(html: BeautifulSoup) -> list:
    header = html.find_all("tr", class_="datagrid-header")
    if len(header) == 0:
        raise ValueError("Header not found")
    return [th.text for th in header[0].find_all("th")]


def get_data(html: BeautifulSoup) -> list:
    data_even = html.find_all("tr", class_="datagrid-even")
    data_odd = html.find_all("tr", class_="datagrid-odd")
    if len(data_even) == 0 and len(data_odd) == 0:
        raise ValueError("Data not found")
    rows = [
        item
        for pair in zip_longest(data_even, data_odd)
        for item in pair
        if item is not None
    ]
    return [['"' + td.text + '"' for td in row.find_all("td")] for row in rows]


if __name__ == "__main__":
    main()
