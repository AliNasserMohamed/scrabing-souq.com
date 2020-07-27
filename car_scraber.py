import requests
import csv
import json
from bs4 import BeautifulSoup

json_file = open("car.json", "w", encoding="utf-8")
csv_file = open("car.csv", "w", encoding="utf-8")
data = {}
url = (
    "https://jo.opensooq.com/ar/%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D9%88%D9%85%D8%B1%D9%83%D8%A8%D8%A7%D8%AA/%D8%B3%D9%8A%D8%A7%D8%B1%D8%A7%D8%AA-%D9%84%D9%84%D8%A8%D9%8A%D8%B9?page=2&per-page=")
for page in range(10):
    print('---', page, '---')
    r = requests.get(url + str(page))
    print(url + str(page))
    soup = BeautifulSoup(r.content, "lxml")
    unit = soup.find_all("li", {"class": "rectLi ie relative mb15"})
    field = ["title", "type", "year", "distance"]
    csv_writer = csv.DictWriter(csv_file, fieldnames=field)
    csv_writer.writeheader()

    json_file.write("[\n")
    print("1")
    for x in unit:
        title = x.find("span", {"class": "inline vMiddle postSpanTitle"})
        price=x.find("div",{"class":""})
        li = x.find_all("li", {"class": "ml8"})
        if len(li) >= 4:
            type = li[1]
            year = li[2]
            distance = li[3]
            print(li[1].text)
            print(li[2].text)
            print(li[3].text)
        if title:
            csv_writer.writerow(
                {'title': title.text.replace('', '').strip('\r\n'), 'type': type.text
                    , 'year': year.text, "distance": distance.text})
            data["title"] = title.text.replace('                    ', '').strip('\r\n')
            data['type'] = type.text
            data["year"] = year.text
            data["distance"] = distance.text
            file_js = json.dumps(data, ensure_ascii=False, indent=2)
            json_file.write(file_js)
json_file.write("\n ]")
json_file.close()
csv_file.close()
