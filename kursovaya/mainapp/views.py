import pandas as pd
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

from django.http import HttpResponse


# from .models import Post


def index(request):
    sql = ''
    sql += 'SELECT holiday, weekday, workingday ' \
           'FROM graphs ' \
           'ORDER BY id ' \
           'OFFSET 0 ROWS FETCH NEXT 1 ROWS ONLY'
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

        print(records)


        print("Таблица успешно создана в PostgreSQL")

    except (Exception, Error) as error:
        print("Ошибка при работе с PostgreSQL", error)

    finally:
        if connection:
            # cursor.close()
            connection.close()
            print("Соединение с PostgreSQL закрыто")

    output = ['1', '1', '1', '1', '1']

    return HttpResponse('\n'.join(str(records)))
