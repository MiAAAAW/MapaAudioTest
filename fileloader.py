import OpenGL.GL as gl
import numpy as np

from geometry.vec3 import Vec3
from geometry.face import Cara
from geometry.materials import Materiales as mtl


class CargadorObj:
    def __init__(self, nombreArchivo):
        self.vertices = np.empty((0), dtype=Vec3)
        self.normales = np.empty((0), dtype=Vec3)
        self.caras = np.empty((0), dtype=Cara)

        # Parsear el archivo y construir la lista de vértices, caras y normales de las caras
        try:
            archivo = open(nombreArchivo)
            for linea in archivo:
                if linea.startswith("v "):
                    linea = linea.strip().split()
                    vertice = Vec3(linea[1], linea[2], linea[3])

                    self.vertices = np.append(self.vertices, vertice)

                elif linea.startswith("vn"):
                    linea = linea.strip().split()
                    normal = Vec3(linea[1], linea[2], linea[3])

                    self.normales = np.append(self.normales, normal)

                elif linea.startswith("f"):
                    if "/" in linea:
                        linea = linea.strip().split()
                        datosCara = [
                            linea[1].split("/"),
                            linea[2].split("/"),
                            linea[3].split("/"),
                        ]
                        refVertices = [
                            int(datosCara[0][0]),
                            int(datosCara[1][0]),
                            int(datosCara[2][0]),
                        ]
                        vertices = np.array(
                            [
                                self.vertices[refVertices[0] - 1],
                                self.vertices[refVertices[1] - 1],
                                self.vertices[refVertices[2] - 1],
                            ]
                        )
                        # Calcular la normal de la cara usando las normales de los vértices
                        normalCara = None
                        if len(self.normales) > 0:
                            normalCara = (
                                np.sum(
                                    np.array(
                                        [
                                            self.normales[int(datosCara[0][2]) - 1].vec,
                                            self.normales[int(datosCara[1][2]) - 1].vec,
                                            self.normales[int(datosCara[2][2]) - 1].vec,
                                        ],
                                        dtype=float,
                                    ),
                                    axis=0,
                                )
                                / 3
                            )
                            normalCara = Vec3(*(-normalCara))
                    else:
                        linea = linea.strip().split()
                        vertices = (int(linea[1]), int(linea[2]), int(linea[3]))
                        normalCara = Vec3(0, 0, 0)

                    self.caras = np.append(self.caras, Cara(vertices, normalCara))

            archivo.close()
        except IOError:
            print("Archivo .obj no encontrado.")

    def renderizar(self, vista_material=False):
        """
        Devuelve una lista de llamadas renderizables de vértices que representan el modelo.
        """
        if vista_material:
            modo_poligono = gl.GL_FILL
        else:
            modo_poligono = gl.GL_LINE

        if len(self.caras) > 0:
            lista_gl = gl.glGenLists(1)
            gl.glNewList(lista_gl, gl.GL_COMPILE)
            gl.glPolygonMode(gl.GL_FRONT_AND_BACK, modo_poligono)
            gl.glBegin(gl.GL_TRIANGLES)
            for cara in self.caras:
                for vertice in cara.vertices:
                    verticeDibujo = vertice.vec
                    gl.glColor4fv(mtl.color(cara.material))
                    gl.glVertex3fv(verticeDibujo)
            gl.glEnd()
            gl.glEndList()
        return lista_gl
