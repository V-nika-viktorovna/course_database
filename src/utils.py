import os.path
from typing import Any

import psycopg2
import requests
from dotenv import load_dotenv

load_dotenv()
pass_pgadmin = os.getenv('PASS_PGADMIN')


def get_data_employers(employers_list: list) -> Any:
    """Получает лист с работодателями, подключается по api к ресурсу hh.ru
    и возвращает словарь с данными о работодателях"""

    result_list = []
    for employer in employers_list:

        try:
            response = requests.get('https://api.hh.ru/employers/' + employer)
        except Exception as e:
            return f'Ошибка при подключении к hh: {e}'
        else:

            try:
                result_response = response.json()

                result_dict = {
                    'employer_id': result_response['id'],
                    'employer_name': result_response['name'],
                    'open_vacancies': result_response['open_vacancies']
                }

            except Exception as e:

                if response.status_code != 200:
                    print(f'Код ответа: {response.status_code}')
                    return result_list
                else:
                    return f'Ошибка при формировании данных о работодателе: {e}'

            else:
                result_list.append(result_dict)

    return result_list


def creat_database(name_database: str) -> None:
    """Функция принимает строку и создает БД в postgresSQL с переданным в строке именем.
    Также создает таблицы 'employers' и 'vacancies' в этой базе данных"""

    load_dotenv()
    pass_pgadmin = os.getenv('PASS_PGADMIN')

    conn = psycopg2.connect(host='localhost',
                            user='postgres',
                            password=pass_pgadmin)
    cur = conn.cursor()

    conn.autocommit = True
    cur.execute("DROP DATABASE IF EXISTS " + name_database)
    cur.execute("CREATE DATABASE " + name_database)

    cur.close()
    conn.close()

    conn = psycopg2.connect(host='localhost',
                            database=name_database,
                            user='postgres',
                            password=pass_pgadmin)
    cur = conn.cursor()

    conn.autocommit = True
    cur.execute("DROP TABLE IF EXISTS employers;")
    cur.execute("CREATE TABLE employers \
                (employer_id int PRIMARY KEY, \
                employer_name varchar(100) NOT NULL, \
                open_vacancies int);")

    cur.execute("DROP TABLE IF EXISTS vacancies;")
    cur.execute("CREATE TABLE vacancies \
                    (url varchar(255) PRIMARY KEY, \
                    vacancies_name varchar(100) NOT NULL, \
                    salary int, \
                    currency char(5), \
                    employer_id int REFERENCES employers(employer_id) NOT NULL)")

    cur.close()
    conn.close()


def filling_employers(employers_data: list[dict], name_database: str) -> None:
    """Фугкция принимает список словарей с данными о работодателях и имя БД.
     Заполняет таблицу employers"""

    load_dotenv()
    pass_pgadmin = os.getenv('PASS_PGADMIN')

    conn = psycopg2.connect(host='localhost',
                            database=name_database,
                            user='postgres',
                            password=pass_pgadmin)

    with conn.cursor() as cur:
        conn.autocommit = True
        for employer in employers_data:
            cur.execute("""INSERT INTO employers (employer_id, employer_name, open_vacancies) \
                        VALUES (%s, %s, %s);""", (
                        employer['employer_id'],
                        employer['employer_name'],
                        employer['open_vacancies'])
                        )
        conn.close()


def filling_vacancies(result_employers_list: list[dict], name_database: str) -> None:
    """Функция принимает список словарей с данными о работодателях и имя БД.
     Подключается по api к ресурсу hh.ru и заполняет таблицу vacancies"""

    vacancies_list = []
    for employer in result_employers_list:

        params = {
            'employer_id': employer['employer_id'],
            'per_page': 100
        }

        try:
            response = requests.get("https://api.hh.ru/vacancies/", params=params)
        except Exception as e:
            if response.status_code != 200:
                print(f'Код ответа: {response.status_code}')
                break
            else:
                print(f'Ошибка подключения: {e}')
        else:
            result_response = response.json()

            for data in result_response['items']:
                url = data['alternate_url']
                vacancies_name = data['name']
                if data['salary'] is None:
                    salary = 0
                    currency = None
                else:
                    salary = data['salary'].get("from")
                    currency = data['salary'].get("currency")

                vacancie_dict = {
                                'url': url,
                                'vacancies_name': vacancies_name,
                                'salary': salary,
                                'currency': currency,
                                'employer_id': employer['employer_id']
                                }
                vacancies_list.append(vacancie_dict)

    conn = psycopg2.connect(host='localhost',
                            database=name_database,
                            user='postgres',
                            password=pass_pgadmin)

    with conn.cursor() as cur:

        for vacanci in vacancies_list:
            cur.execute("""INSERT INTO vacancies (url, vacancies_name, salary, currency, employer_id) \
                        VALUES (%s, %s, %s, %s, %s);""", (
                        vacanci['url'],
                        vacanci['vacancies_name'],
                        vacanci['salary'],
                        vacanci['currency'],
                        vacanci['employer_id'])
                        )
            conn.commit()
        conn.close()


if __name__ == '__main__':
    employers_list = ['1035394', '3177', '23427', '4352', '3776', '907345', '3529', '4181', '84585', '196621']

    creat_database('vacancies_top10_employers')
    result_employers_list = get_data_employers(employers_list)
    #print(result_employers_list)
    filling_employers(result_employers_list, 'vacancies_top10_employers')
    filling_vacancies(result_employers_list, 'vacancies_top10_employers')
