from Work_with_db import *
import pandas as pd
import sqlite3


def genres():
    data1 = select_column('Genre', 'Netflix', conn)
    data2 = select_column('listed_in', 'Disney', conn)
    data2 = data2.rename(columns={'listed_in': 'Genre'})

    data = pd.concat([data1, data2], ignore_index=True, axis=0)
    data = to_split(data['Genre'], 'Genre', ', |/').drop_duplicates()
    # data.index.name = "Id"

    # print(data)
    insert_to_db('Genres', data, conn)


def directors():
    data = select_column('director', 'Disney', conn)
    data = to_split(data['director'], 'Director', ', ').drop_duplicates()

    insert_to_db('Directors', data, conn)


def cast():
    data = select_column('cast', 'Disney', conn)
    data = to_split(data['cast'], 'Actor', ', ').drop_duplicates()

    insert_to_db('Actors', data, conn)


def countries():
    data = select_column('country', 'Disney', conn)
    data = to_split(data['country'], 'Country', ', ').drop_duplicates()

    insert_to_db('Countries', data, conn)


def types():
    data = select_column('type', 'Disney', conn)

    # print(data)
    insert_to_db('Types', data.type, conn)


def premieres():
    data1 = select_column('release_year', 'Disney', conn)
    data1.columns = ['Premiere']
    data2 = select_column('Premiere', 'Netflix', conn)

    data = pd.concat([data1, data2], ignore_index=True, axis=0)

    # print(data)
    insert_to_db('Release_date', data, conn)


def company():
    data = pd.DataFrame({'Company': ['Disney', 'Netflix']})

    # print(data)
    insert_to_db('Companies', data, conn)


def languages():
    query = """SELECT WikipediaLanguageCode AS Lang_code, 
                LanguagenameEnglish AS Lang_name, 
                Languagenamenative AS Lang_native_name
                FROM Languages_set """
    data1 = select_(query, conn)

    query = """SELECT Netflix.Language AS Lang_name FROM Netflix
                GROUP BY Netflix.Language"""
    data2 = select_(query, conn)
    data2 = to_split(data2.Lang_name, 'Lang_name', '/')

    data = pd.concat([data1, data2], ignore_index=True, axis=0).drop_duplicates(subset=['Lang_name'])
    # data = data.reset_index()
    # print(data)

    insert_to_db("Languages", data, conn)


def rewrite():
    # SELECT Disney
    query = """SELECT title AS Title, 
                duration AS Duration, 
                Types.Id AS Type, 
                Release_date.Id As Premiere,
                listed_in AS Genre, 
                director, 
                Disney.cast, 
                country
                FROM Disney
                INNER JOIN Types
                ON Types.Type = Disney.type
                INNER JOIN Release_date
                ON Disney.release_year = Release_date.Premiere"""
    disney = select_(query, conn)
    disney.insert(3, 'Company', 0, True)

    # SELECT Netflix
    query = """SELECT Title, 
                        Runtime AS Duration,
                        Release_date.Id As Premiere,
                        Genre,
                        IMDBScore,
    					Netflix.Language AS Lang_name
                        FROM Netflix
                        INNER JOIN Release_date
                        ON Netflix.Premiere = Release_date.Premiere"""
    netflix = select_(query, conn)
    netflix.insert(2, 'Type', 1, True)
    netflix.insert(3, 'Company', 1, True)

    # Data manipulation
    data = pd.concat([netflix, disney], ignore_index=True, axis=0)

    # INSERT DATA
    print(data)
    print(data.columns)
    data_db = data[['Title', 'Duration', 'IMDBScore', 'Type', 'Company', 'Premiere']]
    insert_to_db('Films', data_db, conn)
    print(data_db.columns)
    print(data_db)
    print(data_db.Duration)

    create_additional_tb(data['cast'], 'Cast', 'Actors', 'Actor', ', ')
    data = data.drop(['cast'], axis=1)
    create_additional_tb(data['director'], 'Directors_to_films', 'Directors', 'Director', ', ')
    data = data.drop(['director'], axis=1)
    create_additional_tb(data['Genre'], 'Genres_to_films', 'Genres', 'Genre', ', |/')
    data = data.drop(['Genre'], axis=1)
    create_additional_tb(data['country'], 'Countries_to_films', 'Countries', 'Country', ', ')
    data = data.drop(['country'], axis=1)
    create_additional_tb(data['Lang_name'], 'Languages_to_films', 'Languages', 'Lang_name', '/')
    data = data.drop(['Lang_name'], axis=1)


def create_additional_tb(data, new_table, table, fild, separator):
    new_data = pd.DataFrame()
    # print(data)
    data2 = select_(f"SELECT * FROM {table}", conn)
    # print(data2)
    data2 = data2.set_index(fild)
    # print(data2)

    for el in data:
        try:
            lst = [e.strip(' \t\n\r').capitalize() for e in re.split(separator, el)]
            for e in lst:
                # print(e)
                # print(data[data == el].index[0])
                # print(data2.loc[e].index)
                df = pd.DataFrame({'Film': [data[data == el].index[0]], fild: [data2.loc[e].Id]})
                new_data = pd.concat([new_data, df], ignore_index=True, axis=0)
                # print(df)
        except TypeError:
            pass

    # print(new_data)
    insert_to_db(new_table, new_data.drop_duplicates(), conn)


if __name__ == '__main__':
    user = 'root'
    password = '1212'
    host = 'localhost'
    port = 3306
    database = 'Stage2'

    try:
        conn = get_connection(user, password, host, port, database)
        print(
            f"Connection to the {host} for user {user} created successfully.")
    except Exception as ex:
        print("Connection could not be made due to the following error: \n", ex)

    genres()
    directors()
    cast()
    countries()
    types()
    premieres()
    company()
    languages()

    rewrite()
