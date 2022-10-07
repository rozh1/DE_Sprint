import operator
import re
from concurrent.futures import ThreadPoolExecutor
from types import NoneType
from typing import Dict, Optional
from urllib.parse import urlencode
from numpy import void
from tabulate import tabulate
import requests
from tqdm import tqdm

class DataCollector:
    r"""Researcher parameters

    Parameters
    ----------
    exchange_rates : dict
        Dict of exchange rates: RUR, USD, EUR.

    """
    __API_BASE_URL = "https://api.hh.ru/vacancies/"

    def __init__(self, exchange_rates: Optional[Dict]):
        self._rates = exchange_rates

    @staticmethod
    def clean_tags(html_text: str) -> str:
        """Remove HTML tags from the string

        Parameters
        ----------
        html_text: str
            Input string with tags

        Returns
        -------
        result: string
            Clean text without HTML tags

        """
        pattern = re.compile("<.*?>")
        return re.sub(pattern, "", html_text)

    @staticmethod
    def __convert_gross(is_gross: bool) -> float:
        return 0.87 if is_gross else 1

    def get_vacancy(self, vacancy_id: str):
        # Get data from URL
        url = f"{self.__API_BASE_URL}{vacancy_id}"
        vacancy = requests.api.get(url).json()

        # Extract salary
        salary = vacancy.get("salary")

        # Calculate salary:
        # Get salary into {RUB, USD, EUR} with {Gross} parameter and
        # return a new salary in RUB.
        from_to = {"from": None, "to": None}
        if salary:
            is_gross = vacancy["salary"].get("gross")
            for k, v in from_to.items():
                if vacancy["salary"][k] is not None:
                    _value = self.__convert_gross(is_gross)
                    from_to[k] = int(_value * salary[k] / self._rates[salary["currency"]])

        # Create pages tuple
        return (
            vacancy_id,
            vacancy["employer"]["name"],
            vacancy["name"],
            salary is not None,
            from_to["from"],
            from_to["to"],
            vacancy["experience"]["name"],
            vacancy["schedule"]["name"],
            [el["name"] for el in vacancy["key_skills"]],
            self.clean_tags(vacancy["description"]),
        )

    def collect_vacancies(self, query: Optional[Dict], refresh: bool = False, max_workers: int = 1) -> list:
        """Parse vacancy JSON: get vacancy name, salary, experience etc.

        Parameters
        ----------
        query : dict
            Search query params for GET requests.
        refresh :  bool
            Refresh cached data
        max_workers :  int
            Number of workers for threading.

        Returns
        -------
        dict
            Dict of useful arguments from vacancies

        """

        # Check number of pages...
        target_url = self.__API_BASE_URL + "?" + urlencode(query)
        num_pages = requests.get(target_url).json()["pages"]

        # Collect vacancy IDs...
        ids = []
        for idx in range(num_pages + 1):
            response = requests.get(target_url, {"page": idx})
            data = response.json()
            if "items" not in data:
                break
            ids.extend(x["id"] for x in data["items"])

        # Collect vacancies...
        jobs_list = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            for vacancy in tqdm(
                executor.map(self.get_vacancy, ids),
                desc="Get data via HH API",
                ncols=100,
                total=len(ids),
            ):
                jobs_list.append(vacancy)

        return jobs_list

class DataAnalyzer:
    def __init__(self, vacancies):
        self._vacancies = vacancies
    
    def TopSkills(self) -> void:
        result = {}
        for vac in vacancies:
            for skill in vac[8]:
                if skill in result:
                    result[skill] += 1
                else:
                    result[skill] = 1

        sorted_d = sorted(result.items(), key=operator.itemgetter(1),reverse=True)
        print(tabulate(sorted_d, headers=['Skill', 'Count'], tablefmt='orgtbl'))
        print()

    def TopExperience(self) -> void:
        result = {}
        for vac in vacancies:
            experience = vac[6]
            if experience in result:
                result[experience] += 1
            else:
                result[experience] = 1

        sorted_d = sorted(result.items(), key=operator.itemgetter(1),reverse=True)
        print(tabulate(sorted_d, headers=['Experience', 'Count'], tablefmt='orgtbl'))
        print()

    def TopCompanies(self) -> void:
        result = {}
        for vac in vacancies:
            company = vac[1]
            if company in result:
                result[company] += 1
            else:
                result[company] = 1

        sorted_d = sorted(result.items(), key=operator.itemgetter(1),reverse=True)
        print(tabulate(sorted_d, headers=['Company', 'Count'], tablefmt='orgtbl'))
        print()

    def TopSalary(self) -> void:
        s_from =['from', -1, -1, -1]
        s_to=['to', -1, -1, -1]
        s_from_count = 0
        s_to_count = 0
        s_from_sum = 0
        s_to_sum = 0
        for vac in vacancies:
            if (vac[4] is not None):
                s_from_count += 1
                s_from_sum += vac[4]
                if (vac[4]<s_from[1] or s_from[1] == -1):
                    s_from[1] = vac[4]
                if (vac[4]>s_from[2] or s_from[2] == -1):
                    s_from[2] = vac[4]

            if (vac[5] is not None):
                s_to_count += 1
                s_to_sum += vac[5]
                if (vac[5]<s_to[1] or s_to[1] == -1):
                    s_to[1] = vac[5]
                if (vac[5]>s_to[2] or s_to[2] == -1):
                    s_to[2] = vac[5]

        if (s_from_count > 0):
            s_from[3] = s_from_sum/s_from_count

        if (s_to_count > 0):
            s_to[3] = s_to_sum/s_to_count

        print(tabulate([s_from, s_to], headers=['From/To', 'Min', 'Max', 'Avg'], tablefmt='orgtbl'))
        print()

if __name__ == "__main__":
    dc = DataCollector(exchange_rates={"USD": 0.017, "EUR": 0.02, "RUR": 1.0})

    vacancies = dc.collect_vacancies(
        query={"text": "Data Engineering", "area": 1, "per_page": 50, "search_field": "name"},
    )

    an = DataAnalyzer(vacancies)
    an.TopCompanies()
    an.TopSkills()
    an.TopExperience()
    an.TopSalary()

    with open("hh_msk.csv", "w", encoding="utf8") as f:
        for x in vacancies:
            f.write(",".join(f'"{str(y)}"' for y in x))
            f.write("\n")
