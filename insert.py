# загрузка данных и создание таблицы
import pandas as pd
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# для вставки данных
from sqlalchemy import create_engine



# загружаем наш csv, получая Датафрейм
bike = pd.read_csv(r'bikes_info.csv')

# хранение названий атрибутов
data_head = bike.columns.values.tolist()

# хранение типов
data_types = bike.dtypes.tolist()

# хранение данных (индексы колонки данных совпадают с индексом атрибута)
data = bike.values.tolist()


sql_create_table = ''

for i in range(len(data_head)):
    if (i == 0):
        sql_create_table += 'CREATE TABLE graphs (id integer PRIMARY KEY NOT NULL, '
    else:
        sql_create_table += str(data_head[i])
        match data_types[i]:
            case 'int64':
                sql_create_table += ' integer'
            case 'float64':
                sql_create_table += ' double precision'
            case 'object':
                sql_create_table += ' text'
        sql_create_table += ' NOT NULL'
        if (i == len(data_head) - 1):
            sql_create_table += ');'
        else:
            sql_create_table += ', '

# print(tuple(data[0]))


sql_insert = 'INSERT INTO graphs VALUES '

for i in range(len(data)):
    sql_insert += str(tuple(data[i]))
    if (i == len(data) - 1):
        sql_insert += ';'
    else:
        sql_insert += ', '









try:
    # Подключение к базе данных
    connection = psycopg2.connect(user="postgres", password="Onitsuka98",
                                  host="localhost", port="5432",
                                  database="SciviDatabase")

    # !!!!!!!!!!!!!!!!! (без нее не создать)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()

    cursor.execute(sql_create_table)
    cursor.execute(sql_insert)

    print("Таблица успешно создана в PostgreSQL")



    # bike.to_sql('graphs', con=connection, if_exists='replace', index=False)


    # Распечатать сведения о PostgreSQL
    #print("Информация о сервере PostgreSQL")
    #print(connection.get_dsn_parameters(), "\n")
    # Выполнение SQL-запроса
    #cursor.execute("SELECT version();")
    # Получить результат
    #record = cursor.fetchone()
    #print("Вы подключены к - ", record, "\n")

except (Exception, Error) as error:
    print("Ошибка при работе с PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("Соединение с PostgreSQL закрыто")
















# bike.drop(['season', 'yr', 'mnth', 'registered', 'cnt'], axis=1, inplace=True)

# bike.to_csv('bikes_info.csv')

# просмотр первыйх 5 строк
# print(data)

# !!!!!!!!!!!!!
# Cведения о датафрейме, выходит общая информация о нём вроде заголовка, количества значений, типов данных столбцов.