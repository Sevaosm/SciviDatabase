from itertools import chain
from psycopg2 import Error
from jinja2 import Environment, select_autoescape
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
from psycopg2.extensions import adapt, register_adapter
from io import BytesIO
from PIL import Image
import io

sql = "SELECT linkimg from graphs where id=1"


try:
    # Подключение к базе данных
    connection = psycopg2.connect(user="postgres", password="Onitsuka98",
                                  host="localhost", port="5432",
                                  database="SciviDatabase")

    # !!!!!!!!!!!!!!!!! (без нее не создать)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Вставка изображения в таблицу
    cursor = connection.cursor()

    cursor.execute(sql)
    binary_data = cursor.fetchone()[0]  # Получение бинарных данных из запроса
    decoded_data = BytesIO(binary_data).read() # Раскодирование бинарных данных в Python

    image = Image.open(io.BytesIO(decoded_data))
    image.save("D:/Dev/Kursovaya/kursovaya/mainapp/static/images/graphs1.gif")

    # Закрытие соединения
    cursor.close()
    connection.close()

    print(decoded_data)

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")












