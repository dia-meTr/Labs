import pandas as pd
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt


def read_dataset(path):
    data = pd.read_csv(path, sep=',')
    return data


def liner_(data):
    liner_regression = stats.linregress(x=data.Date, y=data.Temperature)
    return liner_regression


def prediction(line_inf, x):
    m = line_inf.slope
    b = line_inf.intercept
    t = m * x + b
    return t


def graph(data):
    sns.set_style('whitegrid')
    axes = sns.regplot(x=data.Date, y=data.Temperature)
    axes.set_ylim(10, 70)
    plt.show()


if __name__ == '__main__':
    nyc = read_dataset('USH00305801-tavg-1-1-1895-2018.csv')
    nyc.columns = ['Date', 'Temperature', 'Anomaly']
    nyc.Date = nyc.Date.floordiv(100)
    print(nyc, end='\n\n')

    print(nyc.Temperature.describe(), end='\n\n')

    line = liner_(nyc)

    print('Temperature forecast for the coming years:')
    print('2019: ', prediction(line, 2019))
    print('2020', prediction(line, 2020))
    print('2021', prediction(line, 2021), end='\n\n')

    print('Estimation of temperature in previous years:')
    print('1892', prediction(line, 1892))
    print('1885', prediction(line, 1885))
    print('1880', prediction(line, 1880))

    graph(nyc)
