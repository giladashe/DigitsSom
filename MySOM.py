import sys
from random import randint, choice, choices
import math

cols = rows = 6
vector_size = 100


class Table:
    def __init__(self, size):
        self.vector_size = size
        # vectors = np.empty((4, 0), int)

        vectors = [[0.0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                vectors[i] = self.create_random_vector()

        self._vectors = vectors

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

    def get_best_matching_unit(self, example):
        vectors = self._vectors
        best = [0.0, 0]
        for i in range(len(vectors)):
            sum = 0
            for j in range(len(example)):
                sum += math.pow(example[j] - vectors[i][j], 2)
            distance = math.sqrt(sum)
            if best[0] < distance:
                best[0] = distance
                best[1] = i
        return best[1]


class Examples:
    def __init__(self, file_name):
        f = open(file_name, "r")
        all_file = f.read()
        f.close()
        examples = [[0.0] * vector_size for _ in range(vector_size)]
        all_file = all_file.replace(" ", "")
        all_file = all_file.replace("\t", "")
        digits = all_file.split("\n\n")
        for i, digit in enumerate(digits):
            digits[i] = digit.replace("\n", "")
            examples[i] = list()
            for new_digit in digits[i]:
                examples[i].append(float(new_digit))

        self.digits = examples

    def get_digits(self):
        return self.digits


def main():
    if len(sys.argv) < 2:
        print('error')
    examples = Examples(sys.argv[1])
    table = Table(vector_size)
    # vectors = table.get_vectors()
    for i in range(len(examples.get_digits())):
        random_example = choice(examples.get_digits())
        index_of_best = table.get_best_matching_unit(random_example)
        # todo update vectors[index_of_best] and 3 neighborhoods
    # print(vectors)
    # todo make function that returns how good is this map (a number)
    # todo draw map


if __name__ == "__main__":
    main()
