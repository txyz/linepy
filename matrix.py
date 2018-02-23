#!/usr/bin/env python3

# This module is pdoc-ready.  Generate document by
# "PYTHONPATH=.:$PYTHONPATH pdoc --html --html-no-source --overwrite THIS_FILE".

"""Linear algebra library"""

import copy
import math

class Vector(object):
    """A mathematical vector with some components."""
    def __init__(self, *comps):
        """Construct a vector from its components."""
        self.Components = list(comps)

    @property
    def Size(self):
        """Number of components in the vector."""
        return len(self.Components)

    def __getitem__(self, i):
        return self.Components[i]

    def __setitem__(self, i, x):
        self.Components[i] = x

    def __eq__(self, rhs):
        return self.Components == rhs.Components

    def __len__(self):
        return self.Size

    def __str__(self):
        return ', '.join("{:.3e}".format(c) for c in self.Components)

    def __hash__(self):
        return hash(tuple(self.Components))

    def distanceFrom(self, rhs):
        """Return the distance from self to `rhs`, calculated with Euclidean
        metric.  `Rhs` should have the same size as self.  If not,
        raise a `TypeError`.
        """
        if self.Size != rhs.Size:
            raise TypeError("Vector size do not match.")

        return math.sqrt(sum((self.Components[i] - rhs.Components[i]) ** 2
                             for i in range(self.Size)))

    def dot(self, rhs):
        """Euclidean inner product with `rhs`."""
        if self.Size != len(rhs):
            raise TypeError("Vector size do not match.")

        return sum(self[i] * rhs[i] for i in range(self.Size))

    def norm2(self):
        """Squre of norm of vector."""
        return sum(x*x for x in self.Components)

    def norm(self):
        """Norm of vector."""
        return math.sqrt(self.norm2())

    def __neg__(self):
        NegVec = copy.copy(self)
        for i in range(NegVec.Size):
            NegVec[i] = -NegVec[i]
        return NegVec

    def __add__(self, rhs):
        if self.Size != rhs.Size:
            raise TypeError("Vector size do not match.")

        Result = copy.copy(self)
        for i in range(Result.Size):
            Result[i] = self[i] + rhs[i]
        return Result

    def __sub__(self, rhs):
        if self.Size != rhs.Size:
            raise TypeError("Vector size do not match.")

        Result = copy.copy(self)
        for i in range(Result.Size):
            Result[i] = self[i] - rhs[i]
        return Result

    def __mul__(self, rhs):
        """Multiply vector with a number."""
        try:
            float(rhs)
        except TypeError:
            raise TypeError("Vector can only be multiplied by a number.")
        else:
            Result = copy.copy(self)
            for i in range(Result.Size):
                Result[i] = self[i] * rhs
            return Result

class Vector3D(Vector):
    """Specialized vector in 3-dimensional space."""
    def __init__(self, x=0, y=0, z=0):
        super(Vector3D, self).__init__(x, y, z)

    @property
    def x(self):
        """The x corrdinate of the atom."""
        return self.Components[0]

    @x.setter
    def x(self, value):
        self.Components[0] = value

    @property
    def y(self):
        """The y corrdinate of the atom."""
        return self.Components[1]

    @y.setter
    def y(self, value):
        self.Components[1] = value

    @property
    def z(self):
        """The z corrdinate of the atom."""
        return self.Components[2]

    @z.setter
    def z(self, value):
        self.Components[2] = value

class Matrix(object):
    def __init__(self, n_rows, n_cols):
        self._Cols = []         # A list of column vectors
        for col in range(n_cols):
            self._Cols.append(Vector(*([0,] * n_rows)))

        self._NRows = n_rows
        self._NCols = n_cols

    @property
    def NRows(self):
        """Number of rows."""
        return self._NRows

    @property
    def NCols(self):
        """Number of columns."""
        return self._NCols

    def __getitem__(self, row_col):
        Row, Col = row_col
        return self._Cols[Col][Row]

    def __setitem__(self, row_col, value):
        Row, Col = row_col
        self._Cols[Col][Row] = value

    def rows(self):
        """Iterator over all row vectors."""
        for Row in range(self.NRows):
            yield Vector(*tuple(self._Cols[c][Row] for c in range(self.NCols)))

    def cols(self):
        """Iterator over all col vectors."""
        for v in self._Cols:
            yield v

    def __str__(self):
        return '\n'.join(str(v) for v in self.rows())

    def __mul__(self, rhs):
        """Matrix multiplication with a matrix or vector."""
        import itertools

        if isinstance(rhs, Matrix):
            # self.NCols == rhs.NRows  <--- this should be true.
            if self.NCols != rhs.NRows:
                raise RuntimeError("Matrix multiplication dimension mismatch.")

            Result = Matrix(self.NRows, rhs.NCols)
            RowsLhs = self.rows()
            for Row in range(self.NRows):
                RowV = next(RowsLhs)
                ColsRhs = rhs.cols()
                for Col in range(rhs.NCols):
                    Result[Row, Col] = RowV.dot(next(ColsRhs))
            return Result

        else:
            # `rhs' should be some sequence that is index-able.
            try:
                rhs[0]
                len(rhs)
            except:
                raise TypeError("RHS for matrix multiplication should be "
                                "index-able, and have a length.")

            if self.NCols != len(rhs):
                raise RuntimeError("Matrix multiplication dimension mismatch.")

            Result = Vector(*([0,] * self.NRows))
            RowsLhs = self.rows()
            for Row in range(self.NRows):
                Result[Row] = next(RowsLhs).dot(rhs)
            return Result

    def __eq__(self, rhs):
        if self.NRows == rhs.NRows and self.NCols == rhs.NCols:
            ColsL = self.cols()
            ColsR = rhs.cols()
            for i in range(self.NCols):
                if next(ColsL) != next(ColsR):
                    return False
            return True
        return False
