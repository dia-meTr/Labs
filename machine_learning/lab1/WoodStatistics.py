import statistics
import matplotlib.pyplot as plt


class WoodStatistics:
    def __init__(self, data, years):
        self.data = [x.value for x in data]
        self.years = years
        self.mean = self.count_math_exp()
        self.median = self.count_median()
        self.mode = self.count_mode()
        self.variance = self.count_variance()
        self.standard_deviation = self.count_standard_deviation()

    def count_math_exp(self):
        mean = statistics.mean(self.data)
        return mean

    def count_median(self):
        median = statistics.median(self.data)
        return median

    def count_mode(self):
        mode = statistics.mode(self.data)
        return mode

    def count_variance(self):
        variance = statistics.pvariance(self.data)
        return variance

    def count_standard_deviation(self):
        deviation = statistics.pstdev(self.data)
        return deviation

    def graf(self):
        plt.bar(self.years, self.data)
        plt.show()

    def __str__(self):
        s = f"Data: {self.data} \n" \
            f"Mathematical expectation = {self.mean} \n" \
            f"Median = {self.median} \n" \
            f"Mode = {self.mode} \n" \
            f"Variance = {self.variance} \n" \
            f"Standard deviation = {self.standard_deviation} "
        return s
