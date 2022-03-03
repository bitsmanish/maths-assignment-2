from random import random
from copy import deepcopy
import math
from turtle import update

class Matrix:

    # constructor
    def __init__(self, rows=0, cols=0, array=None, precision=4):
        self.precision = precision

        if array != None:
            self.A = array
        else:
            self.A = self.zeros(rows, cols)

    def pad_value(self, value):
        if self.precision is None or self.precision < 0:
            return str(value)
        return format(value, f".{self.precision}f")

    def round(self):
        (m, n) = self.A
        for i in range(m):
            for j in range(n):
                self.A[i][j] = round(self.A[i][j], self.precision)

    def matrix(self, copy=False):
        if copy:
            return deepcopy(self.A)
        return self.A

    def copy(self):
        return Matrix(array=self.matrix(True), precision=self.precision)

    # print matrix

    def __str__(self):
        m, n = self.shape()

        str_matrix = "["
        for i in range(m):
            str_matrix += "["
            for j in range(n):
                value = self.pad_value(self.A[i][j])
                str_matrix += f" {value} "
            str_matrix += "]"
            if i != m-1:
                str_matrix += "\n"
        return str_matrix + ']'

    # returns shape of matrix
    def shape(self):
        rows, cols = 0, 0
        if len(self.A):
            rows, cols = len(self.A), len(self.A[0])
        return rows, cols

    # fills matrix with zeros
    def zeros(self, rows=None, cols=None):
        if rows and cols:
            m, n = rows, cols
        else:
            m, n = self.shape()
        return [[0 for j in range(n)] for i in range(m)]

    # fills matrix with random
    def random(self):
        m, n = self.shape()
        self.A = [[random() for j in range(n)] for i in range(m)]

    # fetch or update row

    def row(self, row, update=None):
        m, n = self.shape()

        if row >= m:
            if update:
                return False
            return []

        # update row
        if update:
            if len(update) == n:
                self.A[row] = update
                return True
            return False

        # fetch row
        return self.A[row]

    # fetch or update column
    def col(self, col, update=None):
        m, n = self.shape()
        if col >= n:
            if update:
                return False
            return []

        # update column
        if update:
            if len(update) == m:
                for row in range(m):
                    self.A[row][col] = update[row]
                return True
            return False

        # fetch col
        values = []
        for row in range(m):
            values.append(self.A[row][col])
        return values

    # transpose matrix
    def transpose(self, copy=False):
        m, n = self.shape()
        AT = [[self.A[j][i] for j in range(m)] for i in range(n)]
        if copy:
            return Matrix(array=AT, precision=self.precision)
        self.A = AT

    # swap rows or cols
    def swap(self, type, i, j):

        # rows
        if type == 'row':
            row1 = self.row(i)
            row2 = self.row(j)
            self.row(i, row2)
            self.row(j, row1)

        # columns
        if type == 'col':
            col1 = self.col(i)
            col2 = self.col(j)
            self.col(i, col2)
            self.col(j, col1)

    # sum of all values
    def sum(self, A=None, makeAbs=False, onlyRow=False):
        if A is None:
            A = self.A
        arr = []

        if makeAbs:
            arr = [sum([abs(c) for c in r]) for r in A]
        else:
            arr = [sum(r) for r in A]

        if onlyRow:
            return arr
        return sum(arr)

    # returns a sqaure matrix by padding with 0 if required

    def square(self, A, r, c):
        m = max(r, c)
        B = self.zeros(m, m)
        for i in range(r):
            for j in range(c):
                B[i][j] = A[i][j]
        return B

    # rank of matrix
    def rank(self):
        m, n = self.shape()
        A = self.matrix(True)
        A = self.square(A, m, n)

        r = n

        for i in range(r):
            if A[i][i] != 0:
                for j in range(m):
                    if j != i:
                        factor = A[j][i]/A[i][i]
                        for k in range(r):
                            A[j][k] -= (factor * A[i][k])
            else:
                reduce = True
                for k in range(i + 1, m):
                    if A[k][i] != 0:
                        for c in range(r):
                            temp = A[i][c]
                            A[i][c] = A[i][c]
                            A[k][c] = temp
                        reduce = False
                        break
                if reduce:
                    r -= 1
                    for k in range(m):
                        A[k][i] = A[k][r]
                i -= 1
        return r

    # scalar operations
    def scalar(self, n, opr='*', update=False, makeAbs=False):
        (r, c) = self.shape()
        R = self.zeros(r, c)
        for i in range(r):
            for j in range(c):
                value = self.A[i][j] * n
                if opr == '+':
                    value = self.A[i][j] + n
                elif opr == '-':
                    value = self.A[i][j] - n
                elif opr == '/':
                    value = self.A[i][j] / n
                elif opr == '**':
                    value = self.A[i][j] ** n
                if makeAbs:
                    value = abs(value)
                R[i][j] = value

        if update:
            self.A = R
        return R

    # dot product i.e. matrix multiplication
    def multiply(self, B, update=False, copy=False):
        (rA, cA) = self.shape()
        (rB, cB) = B.shape()
        A = self.matrix()
        B = B.matrix()

        if cA != rB:
            print("Uncompatible Operation")
            return

        R = self.zeros(rA, cB)
        for i in range(rA):
            for j in range(cB):
                for k in range(cA):
                    R[i][j] += A[i][k]*B[k][j]

        if update:
            self.A = R
        if copy:
            return Matrix(array=R, precision=self.precision)
        return R

    def dot(self, B):
        (rA, cA) = self.shape()
        (rB, cB) = B.shape()
        A = self.matrix()
        B = B.matrix()

        if rA != rB or cA != cB:
            print("Uncompatible Operation")
        total = 0
        for i in range(rA):
            for j in range(cA):
                total += A[i][j]*B[i][j]
        return total

    # element wise operations
    def eOps(self, B, opr='*', update=False, copy=True):
        A = self.matrix()
        B = B.matrix()
        C = self.zeros(self.shape())

        for i in range(len(A)):
            for j in range(len(A[i])):
                if opr == '*':
                    C[i][j] = A[i][j] * B[i][j]
                elif opr == '+':
                    C[i][j] = A[i][j] + B[i][j]
                elif opr == '-':
                    C[i][j] = A[i][j] - B[i][j]
                elif opr == '/':
                    C[i][j] = A[i][j] / B[i][j]

        if update:
            self.A = C
        if copy:
            return Matrix(array=C, precision=self.precision)
        return C

    # norm

    def norm(self, type='inf'):
        value = 0

        # norm - 2
        if type == 2:
            A = self.copy()
            AT = self.transpose(copy=True)
            AT.multiply(A,update=True)
            (m,n) = AT.shape()
            trace = 0
            for i in range(m):
                trace += AT.matrix()[i][i]
            value = math.sqrt(trace)

        # inf norm
        elif type == 'inf':
            value = max(self.sum(makeAbs=True, onlyRow=True))

        # forbinous norm
        elif type == 'fro':
            value = math.sqrt(
                self.sum(self.scalar(2, opr='**')))

        return value


# solution 1
# take input
def process_input(msg, type='+int'):
    value = input(msg)
    try:
        if type == '+int':
            value = int(value)
            if value < 0:
                raise Exception()
            return value
    except:
        print("Invalid input!!!, Try again")
        process_input(msg, type)
