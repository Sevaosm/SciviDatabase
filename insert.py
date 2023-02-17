import pandas as pd
import psycopg2
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# загружаем наш csv
bike = pd.read_csv(r'bike.csv')

del bike['id']

# хранение названий атрибутов
data_head = bike.columns.values.tolist()

# хранение типов
data_types = bike.dtypes.tolist()

# хранение данных (индексы колонки данных совпадают с индексом атрибута)
data = bike.values.tolist()


sql = ''

for i in range(len(data_head)):
    if (i == 0):
        sql += 'CREATE TABLE graphs (id integer PRIMARY KEY NOT NULL, '
    else:
        sql += str(data_head[i])
        match data_types[i]:
            case 'int64':
                sql += ' integer'
            case 'float64':
                sql += ' double precision'
            case '0':
                sql += ' <ДАТА>'
            case '<bool>':
                sql += ' boolean'
        sql += ' NOT NULL'
        if (i == len(data_head) - 1):
            sql += ');'
        else:
            sql += ', '



print(sql)



try:
    # Подключение к базе данных
    connection = psycopg2.connect(user="postgres", password="Onitsuka98",
                                  host="localhost", port="5432",
                                  database="SciviDatabase")

    # !!!!!!!!!!!!!!!!! (без нее не создать)
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # Курсор для выполнения операций с базой данных
    cursor = connection.cursor()

    create_table_query = sql

    cursor.execute(create_table_query)

    print("Таблица успешно создана в PostgreSQL")

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
# print(bike.info())