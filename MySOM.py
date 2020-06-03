import sys


class Examples:
    def __init__(self, file_name):
        f = open(file_name, "r")
        all_file = f.read()
        f.close()
        all_file = all_file.replace(" ", "")
        all_file = all_file.replace("\t", "")
        digits = all_file.split("\n\n")
        for i, digit in enumerate(digits):
            digits[i] = digit.replace("\n", "")
        self.digits = digits

    def get_digits(self):
        return self.digits


def main():
    if len(sys.argv) < 2:
        print('error')
    examples = Examples(sys.argv[1])
    print(examples.get_digits())


if __name__ == "__main__":
    main()
