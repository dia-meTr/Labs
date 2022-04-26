from Wood_data import *


def series_work():
    print("Створення Series з індексами за замовчуванням")
    print("Виведення колекції Series")
    print(riv.data, end='\n\n')  # Виведення колекції Series

    print("Звернення до елемента 2 Series")
    print(riv.data[2], end='\n\n')  # Звернення до елементів Series

    print("Обчислення описових статистик для Series")
    riv.count_statistic()
    print("----------------------")
    riv.count_describe()
    print(riv.describe, end='\n\n')

    print("Створення колекції Series з нестандартними індексами")
    print(riv.data_with_indexes, end='\n\n')

    print("Звернення до елементів Series з нестандартним індексом '2010'")
    print(riv.data_with_indexes[2010], end='\n\n')

    print("Створення колекції Series із строковими елементами")


def dataframe_work():
    print("Створення DataFrame на базі словника")
    riv.create_dataframe()
    print(riv.data, end='\n\n')

    print("Налаштування індексів DataFrame з використанням атрибута index")
    riv.add_index()
    print(riv.data, end='\n\n')

    print("Звернення до стовпця DataFrame Vinnytsya")
    print(riv.data.Vinnytsya, end='\n\n')

    print("Звернення до стовпця DataFrame Lviv")
    print(riv.data['Lviv'], end='\n\n')

    print("Вибір рядків з використанням атрибутів loc(2010) і iloc(9)")
    print(riv.data.loc[2010], end='\n\n')
    print(riv.data.iloc[9], end='\n\n')

    print("Вибір рядків з використанням атрибутів loc і iloc")
    print(riv.data.loc[2010:2013], end='\n\n')
    print(riv.data.iloc[9:13], end='\n\n')

    print("Вибір підмножин рядків і стовпців")
    print(riv.data.loc[2010:2013, ['Volyn', 'Zhytomyr']], end='\n\n')
    print(riv.data.iloc[9:13, 3:6], end='\n\n')

    print("Логічне індексування (> 100)")
    print(riv.data[riv.data > 100], end='\n\n')

    print("Звернення до конкретного осередку DataFrame по рядку і стовпцю [2002, 'Vinnytsya']")
    print(riv.data.at[2002, 'Vinnytsya'], end='\n\n')

    print("Описова статистика")
    print(riv.data.describe(), end='\n\n')

    print("Транспонування DataFrame з використанням атрибута T")
    print(riv.data.T, end='\n\n')

    print("Сортування рядків за індексами")
    print(riv.data.sort_index(ascending=False), end='\n\n')

    print("Сортування за індексами стовпців")
    print(riv.data.sort_index(axis=1), end='\n\n')

    print("Сортування за значеннями стовпців")
    print(riv.data.sort_values(by=2021, axis=1), end='\n\n')


if __name__ == '__main__':

    years = list(range(2000, 2022))

    print("--Task1(Series)------------------------------------")
    riv = WoodSeries(years)
    series_work()
    del riv

    print("--Task1(DataFrame)")
    regions = ws['X'][6:33]
    regions = [x.value for x in regions]
    riv = WoodDataFrame(years, regions)
    dataframe_work()


