import json
import requests as req
from bs4 import BeautifulSoup, Tag
import tqdm

url = "https://kazan.hh.ru/search/vacancy?search_field=name&search_field=company_name&search_field=description&text=python+%D1%80%D0%B0%D0%B7%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%87%D0%B8%D0%BA&from=suggest_post"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:105.0) Gecko/20100101 Firefox/105.0'
}
resp = req.get(url, headers=headers)
soupe = BeautifulSoup(resp.text, "lxml")
page_tag = soupe.find_all(attrs={"data-qa": "pager-page"})
vacancies = []


def get_tag_text(x: Tag): return x.text if x != None else ""


max_page = 1
for tag in page_tag:
    page = int(tag.text)
    if (max_page < page):
        max_page = page


try:
    for page in tqdm.tqdm(range(0, max_page), desc=" pages", position=0):
        page_url = url + "&page=" + str(page) + "&hhtmFrom=vacancy_search_list"

        resp = req.get(page_url, headers=headers)
        soupe = BeautifulSoup(resp.text, "lxml")
        head_tags = soupe.find_all(attrs={"data-qa": "serp-item__title"})

        for tag in tqdm.tqdm(head_tags, desc=" vacancies", position=1, leave=False):
            vacancy_page = req.get(tag.attrs["href"], headers=headers)
            vacancy_page_soupe = BeautifulSoup(vacancy_page.text, "lxml")
            title = vacancy_page_soupe.find(attrs={"data-qa": "vacancy-title"})
            expeirence = vacancy_page_soupe.find(
                attrs={"data-qa": "vacancy-experience"})
            salary = vacancy_page_soupe.find(
                attrs={"data-qa": "vacancy-salary"})
            region = vacancy_page_soupe.find(
                attrs={"data-qa": "vacancy-view-raw-address"})

            if region == None:
                region = vacancy_page_soupe.find(
                    attrs={"data-qa": "vacancy-view-location"})

            vacancy = {
                "title": get_tag_text(title),
                "work expeirence": get_tag_text(expeirence),
                "salary": get_tag_text(salary),
                "region": get_tag_text(region).split(",")[0] # отбрасывание адреса
            }

            vacancies.append(vacancy)

except Exception as ex:
    print(ex)

result_obj = {
    "data": vacancies
}

with open("vacancies.json", "w", encoding="utf8") as f:
    f.write(json.dumps(result_obj, indent=4, ensure_ascii=False))
