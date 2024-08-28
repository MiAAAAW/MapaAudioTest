import OpenGL.GL as gl
import numpy as np
import math
import random
import sys

from fileloader import CargadorObj
from geometry.vec3 import Vec3
from geometry.face import Cara
from geometry.ray import Rayo
#from formulas.db_formulas import drop_off, sum_levels, db_to_color
from formulas.db_formulas import dist_critica,sumar_niveles,db_a_color,caida_db
from raytracing.brdf import generar_brdf
from geometry.materials import Materiales as mtl


class TrazadorDeRayos:
    def __init__(
        self,
        origen: Vec3,
        num_rayos: int,
        caras: np.ndarray,
        db_inicial=120.0,
        frecuencia=1000,
        reflexiones=0,
    ):
        self.origen = origen
        self.num_rayos = num_rayos
        self.caras = caras
        self.db_inicial = db_inicial
        self.frecuencia = frecuencia
        self.diccionario_puntos = dict()

        for rayo in self.generar_rayos():
            exito = self.intersectar(rayo, reflexiones)
            if not exito:
                print("Error")

    def renderizar(self):
        """
        Devuelve una lista de llamadas renderizables de los puntos generados por el trazado de rayos en el modelo.
        """
        lista_gl = gl.glGenLists(1)
        gl.glNewList(lista_gl, gl.GL_COMPILE)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glPointSize(5)
        gl.glBegin(gl.GL_POINTS)
        for vec, dB in sorted(
            self.diccionario_puntos.items(), key=lambda item: item[1], reverse=True
        ):
            if dB > 100:
                gl.glColor4f(*db_to_color(dB), 1)
            elif dB > 80:
                gl.glColor4f(*db_to_color(dB), 0.65)
            elif dB > 60:
                gl.glColor4f(*db_to_color(dB), 0.25)
            elif dB > 40:
                gl.glColor4f(*db_to_color(dB), 0.125)
            else:
                gl.glColor4f(*db_to_color(dB), 0.0625)

            gl.glVertex3fv(vec)
        gl.glEnd()
        gl.glEndList()
        return lista_gl

    def generar_rayos(self) -> list:
        """
        Genera un array de rayos para usar en el trazado de rayos
        """
        rnd = random.random() * self.num_rayos

        puntos = []
        offset = 2.0 / self.num_rayos
        incremento = math.pi * (3.0 - math.sqrt(5.0))

        for i in range(self.num_rayos):
            y = ((i * offset) - 1) + (offset / 2)
            r = math.sqrt(1 - pow(y, 2))

            phi = ((i + rnd) % self.num_rayos) * incremento

            x = math.cos(phi) * r
            z = math.sin(phi) * r

            puntos.append(Rayo(self.origen, Vec3(x, y, z).normalizar(), 1, self.db_inicial))
        return puntos

    def intersectar(self, rayo: Rayo, numR=0) -> bool:
        """
        Determina el punto de intersección del rayo dado para el modelo actual
        """
        EPSILON = sys.float_info.epsilon
        for cara in self.caras:
            # Origen en el plano
            if self.esta_dentro(rayo.origen, *cara.vertices, cara.normal):
                continue

            # Verificar si el rayo es paralelo al plano
            pvec = rayo.direccion.producto_cruzado(cara.borde2)
            det = cara.borde1.producto_punto(pvec)
            if det > -EPSILON and det < EPSILON:
                continue

            inv_det = 1.0 / det
            tvec = rayo.origen.restar(cara.vertices[0])
            u = tvec.producto_punto(pvec) * inv_det
            if u < 0.0 or u > 1.0:
                continue

            qvec = tvec.producto_cruzado(cara.borde1)
            v = rayo.direccion.producto_punto(qvec) * inv_det
            if v < 0.0 or u + v > 1.0:
                continue

            # Distancia desde el origen del rayo
            t = cara.borde2.producto_punto(qvec) * inv_det
            # El rayo se aleja del plano
            if t < EPSILON:
                continue

            # Punto de intersección
            phit_largo = rayo.origen.sumar(Vec3(*(rayo.direccion * t)))
            phit = Vec3(*np.around(phit_largo.vec, decimals=2))

            # Calcular el nivel de dB en la intersección
            nueva_dist_desde_origen = rayo.dist_desde_origen + rayo.origen.distancia(phit)
            cambio_db = drop_off(rayo.dist_desde_origen, nueva_dist_desde_origen)
            punto_db = rayo.db_inicial - cambio_db

            # Registrar el punto
            db_punto_actual = self.diccionario_puntos.get((phit.x, phit.y, phit.z))
            if db_punto_actual is not None:
                self.diccionario_puntos[(phit.x, phit.y, phit.z)] = sum_levels(
                    [punto_db, db_punto_actual]
                )
            else:
                self.diccionario_puntos[(phit.x, phit.y, phit.z)] = punto_db

            if numR > 0:
                # Calcular los rayos reflejados
                db_reflejado = punto_db * (1 - mtl.absorcion(cara.material, self.frecuencia))
                reflexiones = generar_brdf(
                    rayo, phit, db_reflejado, nueva_dist_desde_origen, cara
                )

                for rayo in reflexiones:
                    if rayo.db_inicial > 0:
                        self.intersectar(rayo, numR - 1)

            return True
        return False

    def esta_dentro(
        self, punto: Vec3, v0: Vec3, v1: Vec3, v2: Vec3, normal: Vec3
    ) -> bool:
        """
        Determina si el punto está dentro de los límites del triángulo dado y en el mismo plano
        """
        borde0 = v1.restar(v0)
        borde1 = v2.restar(v1)
        borde2 = v0.restar(v2)
        C0 = punto.restar(v0)
        C1 = punto.restar(v1)
        C2 = punto.restar(v2)

        if (
            normal.producto_punto(borde0.producto_cruzado(C0)) >= 0
            and normal.producto_punto(borde1.producto_cruzado(C1)) >= 0
            and normal.producto_punto(borde2.producto_cruzado(C2)) >= 0
            and C0.producto_punto(C1.producto_cruzado(C2)) == 0.0
        ):
            return True
        return False
