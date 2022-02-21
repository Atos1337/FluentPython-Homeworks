from collections import defaultdict

from easy import Matrix


class HashMixin:
    def __hash__(self):
        """Считаем сумму элементов в матрице"""
        return sum(map(sum, self._data))


class MatrixWithHash(Matrix, HashMixin):
    def __init__(self, data):
        if isinstance(data, Matrix):
            super().__init__(data._data)
        else:
            super().__init__(data)
        self._map = defaultdict(lambda: defaultdict(lambda: MatrixWithHash([[]])))

    def __matmul__(self, other):
        self_hash = self.__hash__()
        other_hash = other.__hash__()

        if self._map[self_hash].get(other_hash) is None:
            self._map[self_hash][other_hash] = MatrixWithHash(super().__matmul__(other))

        return self._map[self_hash][other_hash]


if __name__ == "__main__":
    A = MatrixWithHash([[1, 2]])
    C = MatrixWithHash([[2, 1]])
    BD = MatrixWithHash([[1], [2]])
    A.to_file("artifacts/hard/A.txt")
    C.to_file("artifacts/hard/C.txt")
    BD.to_file("artifacts/hard/B.txt")
    BD.to_file("artifacts/hard/D.txt")
    AB = (A @ BD)
    AB.to_file("artifacts/hard/AB.txt")
    CD = MatrixWithHash([[4]])
    CD.to_file("artifacts/hard/CD.txt")

    with open("artifacts/hard/hash.txt", 'w') as file:
        newline = '\n'
        file.write(f"A_hash = {A.__hash__()}{newline}")
        file.write(f"B_hash = {BD.__hash__()}{newline}")
        file.write(f"C_hash = {C.__hash__()}{newline}")
        file.write(f"D_hash = {BD.__hash__()}{newline}")
        file.write(f"AB_hash = {AB.__hash__()}{newline}")
        file.write(f"CD_hash = {CD.__hash__()}{newline}")

