import numpy as np

from geometry.vec3 import Vec3
from formulas.geometric_formulas import area_triangulo
from geometry.materials import Materiales as mtl


class Cara:
    """
    Representa la cara triangular de un objeto 3D
    """

    def __init__(
        self,
        vertices: np.ndarray,
        normal: Vec3 = None,
        kd: float = 0.1,
        ks: float = 0.9,
        material: int = mtl.MADERA_DURA,
    ):
        self.vertices = vertices
        if normal is not None:
            self.normal = normal
        elif len(vertices) >= 3:
            self.normal = self.calcular_normal()
        self.borde1 = self.vertices[1].sub(self.vertices[0])
        self.borde2 = self.vertices[2].sub(self.vertices[0])
        self.kd = kd
        self.ks = ks
        self.area_superficie = area_triangulo(*self.vertices)
        self.material = material

    def __str__(self):
        """
        Proporciona una representación en cadena de texto útil de un objeto Cara.
        """
        cadena = "Vértices: ["
        for v in self.vertices:
            cadena += v.__str__()
        cadena += "] Normal de la Cara: " + self.normal.__str__()
        cadena += " Material: " + mtl.nombre(self.material)
        return cadena

    def calcular_normal(self):
        """
        Calcula la normal de la cara usando los vértices
        """
        normal = np.cross(
            self.vertices[1].vec - self.vertices[0].vec,
            self.vertices[2].vec - self.vertices[0].vec,
        )
        return Vec3(*normal).normalizar()
