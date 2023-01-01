from datetime import timedelta
import random
import numpy as np
import copy
import time


class GeneticEngine:
    def __init__(self, population_size, layers, mutation_rate, crossover_rate, retain_rate, X, y):
        self.population_size = population_size
        self.layers = layers
        self.nets = [NeuralNetwork(self.layers) for i in range(self.population_size)]
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.retain_rate = retain_rate
        self.X = X[:]
        self.y = y[:]

    def generate_random_points(self, type):
        net = self.nets[0]
        layer_index, point_index = random.randint(0, net.num_layers - 2), 0
        if type == 'weight':
            row = random.randint(0, net.weights[layer_index].shape[0] - 1)
            col = random.randint(0, net.weights[layer_index].shape[1] - 1)
            point_index = (row, col)
        elif type == 'bias':
            point_index = random.randint(0, net.biases[layer_index].size - 1)

        return (layer_index, point_index)

    def all_scores(self):
        return [net.score(self.X, self.y) for net in self.nets]

    def min_score(self):
        scores = self.all_scores()
        return min(scores)

    def avg_score(self):
        scores = self.all_scores()
        return sum(scores) / len(scores)

    def crossover(self, father, mother):
        # Алгоритм створює нову популяцію шляхом кроссоверу між двома випадковими представниками та мутацією.
        # Кроссовер відбувається випадковим перемішуванням зміщень та вагів нейромереж.

        nn = copy.deepcopy(father)

        for _ in range(self.nets[0].bias_nitem):
            layer, point = self.generate_random_points('bias')
            if random.uniform(0, 1) < self.crossover_rate:
                nn.biases[layer][point] = mother.biases[layer][point]

        for _ in range(self.nets[0].weight_nitem):
            layer, point = self.generate_random_points('weight')
            if random.uniform(0, 1) < self.crossover_rate:
                nn.weights[layer][point] = mother.weights[layer][point]

        return nn

    def mutation(self, child):
        # Мутація відбувається шляхом додавання випадкових змінних до зміщень та вагів нейромереж.
        nn = copy.deepcopy(child)

        for _ in range(self.nets[0].bias_nitem):
            layer, point = self.generate_random_points('bias')
            if random.uniform(0, 1) < self.mutation_rate:
                nn.biases[layer][point] += random.uniform(-0.5, 0.5)

            for _ in range(self.nets[0].weight_nitem):
                layer, point = self.generate_random_points('weight')
                if random.uniform(0, 1) < self.mutation_rate:
                    nn.weights[layer][point[0], point[1]] += random.uniform(-0.5, 0.5)
        return nn

    def run(self):
        # На кожній ітерації циклу:
        score_list = list(zip(self.nets, self.all_scores()))
        score_list.sort(key=lambda x: x[1])
        score_list = [obj[0] for obj in score_list]
        retain_num = int(self.population_size * self.retain_rate)
        score_list_top = score_list[:retain_num]
        retain_non_best = int((self.population_size - retain_num) * self.retain_rate)

        for _ in range(random.randint(0, retain_non_best)):
            score_list_top.append(random.choice(score_list[retain_num:]))


        # Також обираємо кілька представників з поганою точністю для уникнення локальних максимумів
        while len(score_list_top) < self.population_size:
            father = random.choice(score_list_top)
            mother = random.choice(score_list_top)
            if father != mother:
                new_child = self.crossover(father, mother)
                new_child = self.mutation(new_child)
                score_list_top.append(new_child)

        self.nets = score_list_top


class NeuralNetwork(object):
    def __init__(self, sizes):
        self.num_layers = len(sizes)
        self.sizes = sizes
        self.biases = [np.random.randn(y, 1) for y in sizes[1:]]
        self.weights = [np.random.randn(y, x) for x, y in zip(sizes[:-1], sizes[1:])]
        self.bias_nitem = sum(sizes[1:])
        self.weight_nitem = sum([self.weights[i].size for i in range(self.num_layers - 2)])

    def feedforward(self, a):
        for b, w in zip(self.biases, self.weights):
            a = self.sigmoid(np.dot(w, a) + b)
        return a

    def sigmoid(self, z):
        return 1.0 / (1.0 + np.exp(-z))

    def score(self, X, y):
        total_score = 0
        for i in range(X.shape[0]):
            predicted = self.feedforward(X[i].reshape(-1, 1))
            actual = y[i].reshape(-1, 1)
            total_score += np.sum(np.power(predicted - actual, 2) / 2)
        return total_score


def main():
    # Generate our data 2-6-7-8-7-6-1
    # Function is z = x * cos(x + y)

    X = np.random.rand(1000, 2)
    y = X[:, 0] * np.sin(X[:, 0] + X[:, 1])

    POPULATION = 30
    LAYERS = [2, 6, 7, 8, 7, 6, 1]
    MUTATION_RATE = 0.2
    CROSSOVER_RATE = 0.5
    RETAIN_RATE = 0.40

    engine = GeneticEngine(POPULATION, LAYERS, MUTATION_RATE, CROSSOVER_RATE, RETAIN_RATE, X, y)

    for i in range(1000):
        min = engine.min_score()
        print(f"Iteration {i:<3} {min:.5f} ")

        engine.run()


if __name__ == "__main__":
    main()
