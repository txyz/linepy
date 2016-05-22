#!/usr/bin/env python3

import unittest
from matrix import *

class TestMatrix(unittest.TestCase):
    def test_vec_itemization(self):
        v1 = Vector(1, 2, 3)
        self.assertEqual(v1[1], 2)

    def test_vec_equality(self):
        self.assertTrue(Vector(0,1) == Vector(0,1))
        self.assertTrue(Vector() == Vector())
        self.assertTrue(Vector(0) != Vector())
        self.assertTrue(Vector(0,1,2) != Vector(1,1,2))
        self.assertTrue(Vector(1,1,2) != Vector(1,1,1))

    def test_vec_size(self):
        self.assertEqual(Vector(0,1).Size, 2)
        self.assertEqual(len(Vector(0,1)), 2)
        self.assertEqual(Vector().Size, 0)
        self.assertEqual(Vector3D().Size, 3)

    def test_vec_arithmic(self):
        self.assertEqual(-(Vector(1, 2)), Vector(-1, -2))
        self.assertEqual(-(Vector()), Vector())
        self.assertEqual(Vector(0, 1) + Vector(1, 2),
                         Vector(1, 3))
        self.assertEqual(Vector(0, 1) - Vector(1, 2),
                         Vector(-1, -1))
        self.assertEqual(Vector(1, 2) * 2.0, Vector(2.0, 4.0))

        v1 = Vector(1, 2)
        v1 += Vector(1, 3)
        self.assertEqual(v1, Vector(2, 5))

    def test_vec_distance(self):
        self.assertEqual(Vector(1, 1).distanceFrom(Vector(5, 4)), 5.0)
        self.assertEqual(Vector().distanceFrom(Vector()), 0)
        try:
            Vector(1, 2).distanceFrom(Vector(3, 5, 6))
        except TypeError:
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    def test_mat_mult_vec(self):
        m = Matrix(3, 3)
        m._Cols[0] = Vector(0,1,2)
        m._Cols[1] = Vector(3,4,5)
        m._Cols[2] = Vector(6,7,8)

        v = Vector(1,2,3)
        Result = Vector(24, 30, 36)

        self.assertEqual(m * v, Result)
        v = Vector3D(1,2,3)
        self.assertEqual(m * v, Result)

    def test_mat_mult_mat(self):
        m = Matrix(3, 3)
        m._Cols[0] = Vector(0,1,2)
        m._Cols[1] = Vector(3,4,5)
        m._Cols[2] = Vector(6,7,8)

        n = Matrix(3, 3)
        n._Cols[0] = Vector(1,3,5)
        n._Cols[1] = Vector(2,4,6)
        n._Cols[2] = Vector(7,8,9)

        Result = Matrix(3, 3)
        Result._Cols[0] = Vector(39, 48, 57)
        Result._Cols[1] = Vector(48, 60, 72)
        Result._Cols[2] = Vector(78, 102, 126)

        self.assertEqual(m*n, Result)

if __name__ == '__main__':
    unittest.main()
