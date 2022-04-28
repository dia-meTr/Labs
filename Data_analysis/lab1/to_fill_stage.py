from sqlalchemy.engine import create_engine
import sqlite3
import pandas as pd


def create_dataframe(file_name):
    data = pd.read_csv(file_name, encoding="ISO-8859-1")
    return data


def fill_db(data, table):
    data.to_sql(table, con=conn, if_exists='replace', index_label='Id')


def get_connection():
    return create_engine(
        url="mysql+pymysql://{0}:{1}@{2}:{3}/{4}".format(
            user, password, host, port, database
        )
    )


def get_connection_sqlite(db):
        conn = sqlite3.connect(db)
        return conn


if __name__ == '__main__':
    user = 'root'
    password = '1212'
    host = 'localhost'
    port = 3306
    database = 'Stage2'

    try:
        conn = get_connection()
        print(
            f"Connection to the {host} for user {user} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

    # --Netflix
    data_netflix = create_dataframe('Netflix.csv')
    fill_db(data_netflix, 'Netflix')
    del data_netflix

    # --Disney
    data_disney = create_dataframe('Disney.csv')
    fill_db(data_disney, 'Disney')
    del data_disney

    # --Languages
    data_languages = create_dataframe('languages.csv')
    data_languages = data_languages.drop(['index'], axis=1)
    fill_db(data_languages, 'Languages_set')
    del data_languages


