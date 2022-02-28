import numpy as np


class ToStrMixin:
    def __str__(self):
        new_line = '\n'
        return f'[{new_line.join(map(lambda x: "[" + " ".join(map(str, x)) + "]", self._data))}]'


class ToFileMixin:
    def to_file(self, path):
        with open(path, 'w') as file:
            file.write(self.__str__())


class NPGetSetMixin:
    @property
    def shape(self):
        return self.data.shape

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = np.asarray(data)


class MatrixNP(np.lib.mixins.NDArrayOperatorsMixin, ToFileMixin, ToStrMixin, NPGetSetMixin):
    def __init__(self, data):
        self._data = np.asarray(data)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x.data if isinstance(x, MatrixNP) else x
                       for x in inputs)

        result = getattr(ufunc, method)(*inputs, **kwargs)

        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)


if __name__ == "__main__":
    np.random.seed(0)
    A = MatrixNP(np.random.randint(0, 10, (10, 10)))
    B = MatrixNP(np.random.randint(0, 10, (10, 10)))

    (A + B).to_file("artifacts/medium/matrix+.txt")
    (A * B).to_file("artifacts/medium/matrix*.txt")
    (A @ B).to_file("artifacts/medium/matrix@.txt")
    A.to_file("artifacts/medium/A.txt")
    B.to_file("artifacts/medium/B.txt")
