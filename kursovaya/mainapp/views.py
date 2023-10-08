from itertools import chain
from jinja2 import Environment, select_autoescape

import pandas as pd
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from django.shortcuts import render

from django.http import HttpResponse


# заполнение шаблона для вывода данных (корректное кол-во полей)
def html_string_for_data_attributes():

    # запрос количества атрибутов таблицы
    sql = 'SELECT COUNT(*) AS attribute_count FROM information_schema.columns WHERE table_name = \'graphs\'';

    try:
        # Подключение к базе данных
        connection = psycopg2.connect(user="postgres", password="Onitsuka98",
                                      host="localhost", port="5432",
                                      database="SciviDatabase")

        # !!!!!!!!!!!!!!!!! (без нее не создать)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        cursor.execute(sql)

        # количество атрибутов
        count_attributes = cursor.fetchall()

        count_attributes = [list(ele) for ele in count_attributes]

        # количество атрибутов - первый элемент списка
        count_attributes = list(chain.from_iterable(count_attributes))

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

    # Создание экземпляра окружения Jinja2
    env = Environment(autoescape=select_autoescape(['html', 'xml']))

    # Передача значения dataAttributes в шаблон
    template = env.from_string("""
    {% for dataStr in data %}
        <div class="table-row">
            {{ dataAttributes|safe }}
        </div>
    {% endfor %}
    """)

    # Массив данных, который будет использоваться в цикле
    data = [1]
    dataAttributes = ""

    for i in range(count_attributes[0]):
        value = "{{ dataStr." + str(i) + " }}"
        dataAttributes += f"\t\t\t<div class =\"table-cell\" > {value} </div>\n"

    # Отображение шаблона с передачей данных
    rendered_template = template.render(data=data, dataAttributes=dataAttributes)

    with open('templates/indexSup.html', 'w') as file:
        file.write(rendered_template)


# перечисление названий атрибутов
def html_string_attributes():

    sql = 'SELECT attname, format_type(atttypid, atttypmod) AS data_type FROM pg_attribute WHERE attrelid = \'graphs\'::regclass AND attnum > 0;'
    sql_result_names_attributes = ""

    try:
        # Подключение к базе данных
        connection = psycopg2.connect(user="postgres", password="Onitsuka98",
                                      host="localhost", port="5432",
                                      database="SciviDatabase")

        # !!!!!!!!!!!!!!!!! (без нее не создать)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        cursor.execute(sql)

        attributes = cursor.fetchall()

        result = [list(ele) for ele in attributes]

        result1, result2 = list(zip(*result))

        print(result1)
        print(result2)

        print("Таблица успешно создана в PostgreSQL")

        for i in range(len(result1)):
            sql_result_names_attributes += "<div class=\"table-cell\">" + str(result1[i]) + "</div>\n"

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)
    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

    return sql_result_names_attributes


# формирование данных, заполнение основного шаблона
def index(request):

    # заполнение шаблона
    html_string_for_data_attributes()


    # html код названий атрибутов
    html_string_names_attributes = html_string_attributes()

    sql = 'SELECT * ' \
           'FROM graphs ' \
           'ORDER BY id ' \
           'OFFSET 0 ROWS FETCH NEXT 5 ROWS ONLY'
    try:
        # Подключение к базе данных
        connection = psycopg2.connect(user="postgres", password="Onitsuka98",
                                      host="localhost", port="5432",
                                      database="SciviDatabase")

        # !!!!!!!!!!!!!!!!! (без нее не создать)
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

        # Курсор для выполнения операций с базой данных
        cursor = connection.cursor()

        cursor.execute(sql)

        records = cursor.fetchall()

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            # cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

    return render(request, "index.html", {"data": records, 'namesAttributes': html_string_names_attributes})




