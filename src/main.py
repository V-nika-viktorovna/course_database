from DB_Manager import DBManager
from utils import (creat_database, filling_employers, filling_vacancies,
                   get_data_employers)


def main():

    print("Приветствую! В рамках проекта вы можете получить данные о \
компаниях и вакансиях с сайта hh.ru,")

    name_database = input('Введите имя базы данных для работы с вакансиями:\n')
    print('Получаем данные с hh.ru ...')

    employers_list = ['1035394', '3177', '23427', '4352', '3776', '907345', '3529', '4181', '84585', '196621']
    result_employers_list = get_data_employers(employers_list)
    creat_database(name_database)
    filling_employers(result_employers_list, name_database)
    filling_vacancies(result_employers_list, name_database)

    database_user = DBManager(name_database)

    flag_get_companies_and_vacancies_count = int(input('Выберете одно из действий:\n\
1.Получить список всех компаний и количество вакансий у каждой компании\n\
2.Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию\n\
3.Получить среднюю зарплату по всем вакансиям\n\
4.Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n\
5.Получить список всех вакансий, в названии которых содержатся ключевое слово\n'))

    if flag_get_companies_and_vacancies_count == 1:
        database_user.get_companies_and_vacancies_count()

    elif flag_get_companies_and_vacancies_count == 2:
        database_user.get_all_vacancies()

    elif flag_get_companies_and_vacancies_count == 3:
        database_user.get_avg_salary()

    elif flag_get_companies_and_vacancies_count == 4:
        database_user.get_vacancies_with_higher_salary()

    elif flag_get_companies_and_vacancies_count == 5:
        sotr_word = input('Введите ключевое слово:\n')
        database_user.get_vacancies_with_keyword(sotr_word)


if __name__ == '__main__':
    main()
