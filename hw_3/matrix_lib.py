import numpy as np
from numpy.lib.mixins import NDArrayOperatorsMixin
from functools import lru_cache


class MatrixMixin:
    def __str__(self):
        return str(self._data)

    def to_file(self, path):
        np.savetxt(path, self._data, fmt='%d')

    @property
    def data(self):
        return self._data.copy()

    @data.setter
    def data(self, value):
        if not isinstance(value, np.ndarray):
            raise TypeError("данные — ndarray")
        self._data = value.copy()


class HashableMatrixMixin:
    def __hash__(self):
        s = int(self._data.sum()) % (2**32)
        shape_sig = self._data.shape[0] * 1000 + self._data.shape[1]
        return hash(s + shape_sig)


class Matrix:
    def __init__(self, data):
        if isinstance(data, Matrix):
            data = data._data
        self._data = np.array(data, dtype=int)

    def __add__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self._data.shape != other._data.shape:
            raise ValueError("размеры не совпадают")
        return Matrix(self._data + other._data)

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self._data.shape != other._data.shape:
            raise ValueError("размеры не совпадают")
        return Matrix(self._data * other._data)

    def __matmul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        if self._data.shape[1] != other._data.shape[0]:
            raise ValueError("несовместимые размеры")
        return Matrix(self._data @ other._data)

    def __str__(self):
        return str(self._data)

    def to_file(self, path):
        np.savetxt(path, self._data, fmt='%d')


class SmartMatrix(NDArrayOperatorsMixin, MatrixMixin):
    def __init__(self, data):
        if isinstance(data, SmartMatrix):
            data = data._data
        self._data = np.array(data, dtype=int)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = [x._data if isinstance(x, SmartMatrix) else x for x in inputs]
        result = getattr(ufunc, method)(*inputs, **kwargs)
        if isinstance(result, np.ndarray):
            return SmartMatrix(result)
        return result


class CachedMatrix(Matrix, HashableMatrixMixin):
    @lru_cache(maxsize=128)
    def __matmul__(self, other):
        if not isinstance(other, CachedMatrix):
            return NotImplemented
        if self._data.shape[1] != other._data.shape[0]:
            raise ValueError("несовместимые размеры")
        return CachedMatrix(self._data @ other._data)


def find_hash_collision():
    A = np.array([[1, 2], [3, 4]])
    C = np.array([[2, 1], [4, 3]])
    B = np.eye(2, dtype=int)
    D = B.copy()
    mA, mC = CachedMatrix(A), CachedMatrix(C)
    mB, mD = CachedMatrix(B), CachedMatrix(D)
    return mA, mC, mB, mD