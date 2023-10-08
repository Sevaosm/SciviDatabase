from itertools import chain
from psycopg2 import Error
from jinja2 import Environment, select_autoescape
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from psycopg2.extensions import adapt, register_adapter

# Преобразование изображения в бинарные данные
image_file = open("D:/Dev/Kursovaya/kursovaya/mainapp/static/images/gifka.gif", "rb")
image_data = image_file.read()

# Регистрация адаптера для типа данных bytea
def adapt_bytea(data):
    return psycopg2.extensions.Binary(data)


try:
    # Подключение к базе данных
    connection = psycopg2.connect(user="postgres", password="Onitsuka98",
                                  host="localhost", port="5432",
                                  database="SciviDatabase")

    # !!!!!!!!!!!!!!!!! (без нее не создать)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    register_adapter(bytes, adapt_bytea)

    # Вставка изображения в таблицу
    cursor = connection.cursor()

    cursor.execute("UPDATE graphs SET linkimg = %s WHERE id = 1;", (image_data,))
    connection.commit()

    # Закрытие соединения
    cursor.close()
    connection.close()

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")












