import openpyxl
import pandas as pd

wb = openpyxl.load_workbook('zag_der_reg_2000-2021_ue.xlsx')
ws = wb['Shit1']


def get_line(num):
    line = list(ws[f'B{num}':f'W{num}'][0])
    line = [x.value if isinstance(x.value, (int, float)) else None for x in line]
    return line


class WoodSeries:
    def __init__(self, years):
        self.line = get_line(42)
        self.data = self.create_series()
        self.years = years
        self.data_with_indexes = None
        self.describe = None
        self.std = None
        self.max = None
        self.min = None
        self.count = None
        self.add_indexes()

    def create_series(self):  # Створення Series з індексами за замовчуванням
        return pd.Series(self.line)

    def count_statistic(self):  # Обчислення описових статистик для Series
        self.count = self.data.count()
        self.min = self.data.min()
        self.max = self.data.max()
        self.std = self.data.std()

        s = f"Count: {self.count} \n" \
            f"Min = {self.min} \n" \
            f"Max = {self.max} \n" \
            f"Std = {self.std}"
        print(s)

    def count_describe(self):
        self.describe = self.data.describe()

    def add_indexes(self):  # Створення колекції Series з нестандартними індексами
        self.data_with_indexes = pd.Series(self.line, index=self.years)


class WoodDataFrame:
    def __init__(self, years, regions):
        self.data = None
        self.years = years
        self.regions = regions

    def create_dict(self):

        datas = []
        dict = {}
        for i in range(40,67):
            datas.append(get_line(i))

        for i in range(0, 27):
            dict[self.regions[i]] = datas[i]

        return dict

    def create_dataframe(self):  # Створення DataFrame на базі словника
        self.data = pd.DataFrame(self.create_dict())

    def add_index(self):
        self.data.index = self.years


if __name__ == '__main__':
    pass
