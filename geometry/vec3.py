import math
import numpy as np


class Vec3:
    """
    Una tupla mejorada que contiene 3 puntos
    """

    def __init__(self, x: float, y: float, z: float):
        self.vec = np.array([x, y, z], dtype=float)
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __str__(self):
        """
        Proporciona una representación en cadena de texto útil de un objeto Vec3.
        """
        return self.vec.__str__()

    def __iter__(self):
        """
        Iterador de Vec3.
        """
        self.num = 0
        return self

    def __next__(self):
        """
        Función next de Vec3 para iteración.
        """
        if self.num >= 3:
            raise StopIteration

        self.num += 1
        if self.num == 1:
            return self.x
        elif self.num == 2:
            return self.y
        else:
            return self.z

    def __neg__(self):
        """
        Para negar objetos Vec3.
        """
        return Vec3(-self.x, -self.y, -self.z)

    def __mul__(self, otro: float):
        """
        Para la multiplicación escalar de un objeto Vec3 por un float.
        """
        return Vec3(self.x * otro, self.y * otro, self.z * otro)

    def sumar(self, v: "Vec3"):
        """
        Suma 2 objetos Vec3 juntos
        """
        return Vec3(self.x + v.x, self.y + v.y, self.z + v.z)

    def restar(self, v: "Vec3"):
        """
        Resta 2 objetos Vec3 juntos
        """
        return Vec3(self.x - v.x, self.y - v.y, self.z - v.z)

    def producto_punto(self, v: "Vec3"):
        """
        Calcula el producto punto de 2 objetos Vec3
        """
        return self.x * v.x + self.y * v.y + self.z * v.z

    def producto_cruzado(self, v: "Vec3"):
        """
        Calcula el producto cruzado de 2 objetos Vec3
        """
        return Vec3(
            self.y * v.z - self.z * v.y,
            self.z * v.x - self.x * v.z,
            self.x * v.y - self.y * v.x,
        )

    def longitud(self):
        """
        Calcula la longitud del objeto Vec3
        """
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalizar(self):
        """
        Normaliza el objeto Vec3
        """
        l = self.longitud()
        return Vec3(self.x / l, self.y / l, self.z / l)

    def distancia_cuadrada(self, otro: "Vec3"):
        """
        Calcula la distancia al cuadrado entre 2 vértices
        """
        dx = (self.x - otro.x) ** 2
        dy = (self.y - otro.y) ** 2
        dz = (self.z - otro.z) ** 2
        return dx + dy + dz

    def distancia(self, otro: "Vec3"):
        """
        Calcula la distancia entre 2 vértices
        """
        return math.sqrt(self.distancia_cuadrada(otro))
