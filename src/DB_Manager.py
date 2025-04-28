import os.path

import psycopg2
from dotenv import load_dotenv


class DBManager():
    """Класс для работы таблицами employers и vacancies
    из баз данных postgresSQL"""

    load_dotenv()

    def __init__(self, name_database: str, pass_pgadmin=os.getenv('PASS_PGADMIN')):
        self.conn = psycopg2.connect(host='localhost',
                                     database=name_database,
                                     user='postgres',
                                     password=pass_pgadmin)

    def get_companies_and_vacancies_count(self):
        """Метод получает список всех компаний и количество вакансий у каждой компании."""

        cur = self.conn.cursor()

        cur.execute("select employer_name, open_vacancies from employers")
        result_list = cur.fetchall()
        for data in result_list:
            print(f'Компания работодатель: {data[0]}. Количество открытых вакансий: {data[1]}')

        cur.close()

        return result_list

    def get_all_vacancies(self):

        cur = self.conn.cursor()

        cur.execute('SELECT url, vacancies_name, salary, currency, employers.employer_name\
                    FROM vacancies JOIN employers USING (employer_id)')
        result_list = cur.fetchall()
        for data in result_list:
            if data[2] == 0 or data[2] is None:
                salary = 'Зарплата не указана'
                print(f'Компания работодатель: {data[-1]}. Должность: {data[1]}\n\
Зарплата: {salary}, Ссылка: {data[0]}\n{"_"*100}')
            else:
                print(f'Компания работодатель: {data[-1]}. Должность: {data[1]}\n\
Зарплата: {data[2]} {data[3]}, Ссылка: {data[0]}\n{"_"*100}')

        cur.close()

        return result_list

    def get_avg_salary(self):

        cur = self.conn.cursor()

        cur.execute('SELECT AVG(salary) FROM vacancies')
        result = cur.fetchall()
        for data in result:
            print(f"Средняя заработная плата: {round(float(data[0]), 2)} RUB")
        cur.close()

        return result

    def get_vacancies_with_higher_salary(self):

        cur = self.conn.cursor()

        cur.execute('SELECT url, vacancies_name, salary, currency, employers.employer_name\
                    FROM vacancies JOIN employers USING (employer_id)\
                    WHERE salary > (SELECT AVG(salary) FROM vacancies)')
        result_list = cur.fetchall()
        for data in result_list:
            if data[2] == 0 or data[2] is None:
                salary = 'Зарплата не указана'
                print(f'Компания работодатель: {data[-1]}. Должность: {data[1]}\n\
Зарплата: {salary}, Ссылка: {data[0]}\n{"_" * 100}')
            else:
                print(f'Компания работодатель: {data[-1]}. Должность: {data[1]}\n\
Зарплата: {data[2]} {data[3]}, Ссылка: {data[0]}\n{"_" * 100}')

        cur.close()

        return result_list

    def get_vacancies_with_keyword(self, data_search: str):

        cur = self.conn.cursor()

        cur.execute("SELECT url, vacancies_name, salary, currency, employers.employer_name\
                    FROM vacancies JOIN employers USING (employer_id)\
                    WHERE vacancies_name ILIKE '%" + data_search + "%'")
        result_list = cur.fetchall()
        for data in result_list:
            if data[2] == 0 or data[2] is None:
                salary = 'Зарплата не указана'
                print(f'Компания работодатель: {data[-1]}. Должность: {data[1]}\n\
Зарплата: {salary}, Ссылка: {data[0]}\n{"_" * 100}')
            else:
                print(f'Компания работодатель: {data[-1]}. Должность: {data[1]}\n\
Зарплата: {data[2]} {data[3]}, Ссылка: {data[0]}\n{"_" * 100}')

        cur.close()

        return result_list


if __name__ == '__main__':
    a = DBManager('vacancies_top10_employers')
    a.get_companies_and_vacancies_count()
    a.get_all_vacancies()
    a.get_avg_salary()
    a.get_vacancies_with_higher_salary()
    a.get_vacancies_with_keyword('водитель')
