from medium import ToStrMixin, ToFileMixin


class Matrix(ToStrMixin, ToFileMixin):
    def __init__(self, data):
        for i in range(0, len(data) - 1):
            if len(data[i]) != len(data[i + 1]):
                raise ValueError("Data should be rectangle matrix")

        self._data = list(map(list, map(lambda x: map(int, x), data)))
        self._shape = (len(data), 0 if len(data) == 0 else len(data[0]))

    @property
    def shape(self):
        return self._shape

    def __add__(self, other):
        if self.shape != other.shape:
            raise ValueError("Shapes should be equal")

        new_data = [[0 for _ in range(self.shape[1])] for _ in range(self.shape[0])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                new_data[i][j] = self._data[i][j] + other._data[i][j]

        return Matrix(new_data)

    def __mul__(self, other):
        if self.shape != other.shape:
            raise ValueError("Shapes should be equal")

        new_data = [[0 for _ in range(self.shape[1])] for _ in range(self.shape[0])]
        for i in range(self.shape[0]):
            for j in range(self.shape[1]):
                new_data[i][j] = self._data[i][j] * other._data[i][j]

        return Matrix(new_data)

    def __matmul__(self, other):
        if self.shape[1] != other.shape[0]:
            raise ValueError("Width of first should be equal height of second")

        new_data = [[0 for _ in range(other.shape[1])] for _ in range(self.shape[0])]
        for i in range(self.shape[0]):
            for j in range(other.shape[1]):
                for k in range(other.shape[0]):
                    new_data[i][j] += self._data[i][k] * other._data[k][j]

        return Matrix(new_data)


if __name__ == "__main__":
    import numpy as np

    np.random.seed(0)
    a = np.random.randint(0, 10, (10, 10))
    b = np.random.randint(0, 10, (10, 10))
    A = Matrix(a)
    B = Matrix(b)
    print(a @ b)

    (A + B).to_file("artifacts/easy/matrix+.txt")
    (A * B).to_file("artifacts/easy/matrix*.txt")
    (A @ B).to_file("artifacts/easy/matrix@.txt")
    A.to_file("artifacts/easy/A.txt")
    B.to_file("artifacts/easy/B.txt")
