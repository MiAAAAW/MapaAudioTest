import random
import math
import numpy as np
from geometry.vec3 import Vec3
from geometry.face import Cara
from geometry.ray import Rayo


def generar_brdf(
    sm: Rayo, phit: Vec3, db_inicial: float, dist_desde_origen: float, cara: Cara
):
    """
    Genera un array de rayos cuyos niveles de dB iniciales se calculan utilizando el modelo BRDF de Phong
    ## D( kd( Sm.dot(normal) ) + ks( V.dot(Rm) ) )
    - D  - el porcentaje de energía acústica en cada rayo\n
    - kd - coeficiente de difusión\n
    - ks - coeficiente especular\n
    - Sm - rayo incidente\n
    - n  - normal de la superficie\n
    - V  - rayo reflejado\n
    - Rm - rayos del hemisferio desde la superficie
    """
    rm = sm.calc_reflejo(phit, cara.normal, dist_desde_origen, db_inicial)
    v = generar_v(
        phit,
        cara.normal,
        cara.normal.producto_punto(rm.direccion),
        db_inicial,
        dist_desde_origen,
        100,
    )
    difuso = cara.kd * sm.direccion.producto_punto(cara.normal)
    for rayo in v:
        especular = cara.ks * rm.direccion.producto_punto(rayo.direccion)
        rayo.db_inicial = db_inicial * (difuso + especular)

    v = [rm] + v
    return v


def generar_v(
    origen: Vec3,
    normal: Vec3,
    lado_valido: float,
    db_inicial: float,
    dist_desde_origen: float,
    num_rayos,
) -> list:
    """
    Genera rayos en un hemisferio para representar rayos reflejados
    """
    rnd = random.random() * num_rayos

    puntos = []
    offset = 2.0 / num_rayos
    incremento = math.pi * (3.0 - math.sqrt(5.0))

    for i in range(num_rayos):
        y = ((i * offset) - 1) + (offset / 2)
        r = math.sqrt(1 - pow(y, 2))

        phi = ((i + rnd) % num_rayos) * incremento

        x = math.cos(phi) * r
        z = math.sin(phi) * r

        vec = Vec3(x, y, z).normalizar()
        if np.sign(normal.producto_punto(vec)) != np.sign(lado_valido):
            # Asegura que los rayos estén dentro del objeto
            vec = -vec
        puntos.append(Rayo(origen, vec, dist_desde_origen, db_inicial))
    return puntos
