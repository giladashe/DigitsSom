import sys
from random import choice
import matplotlib.pyplot as plt
import math
import numpy as np

cols = rows = 6
vector_size = 100
rangeMax = rows + cols
learnMax = 0.5
stepsMax = 90
shuffle_p = 1


def manhattan_dist(r1, c1, r2, c2):
    return np.abs(r1 - r2) + np.abs(c1 - c2)


def most_common(lst, n):
    # lst is a list of values 0 . . n
    if len(lst) == 0:
        return -1
    counts = np.zeros(shape=n, dtype=np.int)
    for i in range(len(lst)):
        counts[lst[i]] += 1
    return np.argmax(counts)


class Table:
    def __init__(self, size):
        self.vector_size = size
        self._vectors = np.random.uniform(0, 1, size=(rows, cols, vector_size))

    # creates a random binary vector
    def create_random_vector(self):
        binary = [0.0, 1.0]
        vector = []
        # randomly pick binary digit and concatenate to the vector
        for i in range(self.vector_size):
            vector.append(choice(binary))
        # returns the random binary vector
        return vector

    def get_vectors(self):
        return self._vectors

    # gets the BMU - the best matching unit for given example
    def get_best_matching_unit(self, example):
        vectors = self._vectors
        best = [0, 0]
        best_dist = math.inf
        for i, row in enumerate(vectors):
            for j, vect in enumerate(row):
                dist = np.linalg.norm(vect - example)
                if dist < best_dist:
                    best_dist = dist
                    best = [i, j]
        return best[0], best[1]


class Examples:
    def __init__(self, file_name):
        # gets all examples from file and arrange them in an array
        f = open(file_name, "r")
        all_file = f.read()
        f.close()
        examples = np.zeros((vector_size, vector_size))
        all_file = all_file.replace(" ", "")
        all_file = all_file.replace("\t", "")
        digits = all_file.split("\n\n")
        for i, digit in enumerate(digits):
            digits[i] = digit.replace("\n", "")
            for j, new_digit in enumerate(digits[i]):
                examples[i][j] = float(new_digit)

        self.digits = examples

    def get_digits(self):
        return self.digits


def main():
    # Gets examples from the file
    examples = Examples("Digits_Ex3.txt")
    table = Table(vector_size)
    examples_copy = np.asarray(examples.get_digits())
    loss = []
    # go over all the examples and train the SOM
    for r in range(stepsMax):
        if np.random.uniform(0, 1) < shuffle_p:
            np.random.shuffle(examples_copy)
        los = 0
        for v in examples_copy:
            pct_left = 1.0 - ((r * 1.0) / stepsMax)
            curr_rate = pct_left * learnMax
            i_bmu, j_bmu = table.get_best_matching_unit(v)
            vector = table.get_vectors()[i_bmu][j_bmu]
            los += np.linalg.norm(vector - v)
            for i in range(rows):
                for j in range(cols):
                    vector = table.get_vectors()[i][j]
                    manhattan = manhattan_dist(i_bmu, j_bmu, i, j)
                    table.get_vectors()[i][j] = vector + curr_rate * (v - vector) * np.power(0.5, manhattan) * 2
        loss.append(los / 100)
    mapping = np.empty(shape=(rows, cols), dtype=object)
    for i in range(rows):
        for j in range(cols):
            mapping[i][j] = []
    for i, v in enumerate(examples.get_digits()):
        i_bmu, j_bmu = table.get_best_matching_unit(v)
        mapping[i_bmu][j_bmu].append(i // 10)

    digit = 0
    counter = 0

    # print the cells that represents each digit example
    for example in examples.get_digits():
        i_bmu, j_bmu = table.get_best_matching_unit(example)
        print("digit: " + str(digit) + " example number: " + str(counter + 1) + " - represented by cell " + "[" + str(
            i_bmu)
              + "," + str(j_bmu) + "]")
        counter = counter + 1
        if counter == 10:
            digit = digit + 1
            counter = 0
    label_map = np.zeros(shape=(rows, cols), dtype=np.int)
    for i in range(rows):
        for j in range(cols):
            label_map[i][j] = most_common(mapping[i][j], 10)

    plt.imshow(label_map, cmap=plt.cm.get_cmap('terrain_r', 11))
    plt.colorbar()
    plt.show()


if __name__ == "__main__":
    main()
