import numpy as np
from geometry.vec3 import Vec3


def volumen(vertices, caras):
    """
    Calcula el volumen del objeto representado por los vértices
    y caras dadas utilizando la triangulación.
    """
    vols = []
    for cara in caras:
        vols = np.append(
            vols,
            volumen_firma_triangulo(
                cara.vertices[0], cara.vertices[1], cara.vertices[2]
            ),
        )
    return np.abs(np.sum(vols))


def volumen_firma_triangulo(v1: Vec3, v2: Vec3, v3: Vec3):
    """
    Calcula el volumen firmado de un triángulo en relación
    al origen como un tetraedro.
    """
    return v1.dot(v2.cross(v3)) / 6.0


def area_superficie(caras):
    """
    Calcula el área de la superficie del objeto representado por los vértices
    y caras dadas utilizando la triangulación.
    """
    area = []
    for cara in caras:
        area.append(area_triangulo(cara.vertices[0], cara.vertices[1], cara.vertices[2]))
    return np.sum(area)


def area_triangulo(v1, v2, v3):
    """
    Calcula el área de un triángulo usando sus vértices.
    """
    return 0.5 * np.linalg.norm(np.cross(v2.vec - v1.vec, v3.vec - v1.vec))


def calcular_centro(vertices, caras):
    """
    Calcula el centro del objeto representado por los vértices
    y caras dadas utilizando la triangulación.
    """
    centros = []
    for cara in caras:
        centros.append(
            centro_triangulo(cara.vertices[0], cara.vertices[1], cara.vertices[2])
        )
    return Vec3(*np.mean(centros, axis=0))


def centro_triangulo(v1, v2, v3):
    """
    Calcula el centro de un triángulo.
    """
    return np.mean([v1.vec, v2.vec, v3.vec], axis=0)
