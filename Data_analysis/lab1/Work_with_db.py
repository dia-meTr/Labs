import re
import sqlite3
import pandas as pd
from sqlalchemy.engine import create_engine


def get_connection(user, password, host, port, database):
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


def get_connection_sqlite(db):
    conn = sqlite3.connect(db)
    return conn


def select_column(fild, table, conn):
    query = f"""SELECT {table}.{fild} FROM {table} 
                WHERE {table}.{fild} IS NOT NULL 
                GROUP BY {table}.{fild}"""
    genres = pd.read_sql(query, conn)

    return genres


def select_(query, conn):
    try:
        table = pd.read_sql(query, conn)
    except:
        print(f'ERROR {query}')

    return table


def insert_to_db(table, inf, conn):
    try:
        inf = inf.reset_index()
        inf = inf.drop(['index'], axis=1)
        inf.to_sql(table, conn, if_exists='append', index_label='Id')
        print(f'Information added to table {table}')
    except Exception as ex:
        print(f'ERROR:{ex}')
        print(inf)


def to_split(data, column, separator):
    new_data = pd.DataFrame()

    for el in data:
        lst = [e.strip(' \t\n\r').capitalize() for e in re.split(separator, el)]
        new_data = pd.concat([new_data, pd.DataFrame(lst)], ignore_index=True, axis=0)

    # new_data.index.name = "Id"
    new_data = new_data.rename(columns={'index': 'Id', 0: column})
    new_data = new_data

    return new_data.drop_duplicates()

