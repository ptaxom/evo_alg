

import sys
const_max_dist = sys.float_info.max

class Vector:
    def __init__(self, *args):
        cords_list = []
        for x in args:
            cords_list.append(x)
        self.cords = cords_list

    @staticmethod
    def createZeroVector(dims):
        return Vector(*[0 for x in range(dims)])

    def dim(self):
        return len(self.cords)

    def normalize(self):
        self.cords = (self * (1.0 / abs(self))).cords
        return self

    def toRGB(self):
        if self.dim() != 3:
            raise RuntimeError("Convert error")
        color = []
        for x in self.cords:
            if x < 0:
                x = 0
            if x > 1:
                x = 1
            x = int(255 * x)
            color.append(x)
        return color

    def __abs__(self):
        sum = 0
        for cord in self.cords:
            sum += (1.0 * cord) ** 2
        return sum ** 0.5

    def __str__(self):
        out = ""
        for x in self.cords:
            out += str(x) + ","
        return "(" + out[:-1] + ")"

    # Adding
    def __iadd__(self, other):
        self.cords = self + other

    def __add__(self, other):
        if other == 0 or other == "0":
            rhs = Vector.createZeroVector(len(self.cords))
        elif type(other) == Vector:
            rhs = other
        else:
            raise TypeError("Unsupported type {}".format(type(other)))
        if self.dim() == rhs.dim():
            return Vector(*[(self.cords[i] + rhs.cords[i]) for i in range(self.dim())])
        # if self.dim() > rhs.dim():
        #     return self + Vector(*(rhs.cords + [0 for i in range(self.dim() - rhs.dim())]))
        # else:
        #     return rhs + self

    def __radd__(self, other):
        return self + other

    #Multiplying
    def __mul__(self, other):
        if type(other) == int or type(other) == float:          # vector * const
            return Vector(*[(x * other) for x in self.cords])
        if type(other) == Vector:
            if self.dim() == other.dim():
                return sum([(self.cords[i] * other.cords[i]) for i in range(self.dim())])
            else:
                raise AttributeError("Incomparable dimensions")
        raise TypeError("Unsupported type")

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        if type(other) == int or type(other) == float:          # vector * const
            self.cords = (self * other).cords
        else:
            raise TypeError("Unsupported type")

    # Negative
    def __neg__(self):
        return self * -1

    # Substract

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return other + (-self)

    def __getitem__(self, item):
        if type(item) != int:
            raise TypeError("Non-int index!")
        if 0 <= item < self.dim():
            return self.cords[item]
        else:
            raise AttributeError("Out of bounds")



