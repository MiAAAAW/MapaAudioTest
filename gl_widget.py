import math

from PyQt5.QtCore import pyqtSignal, QPoint, QSize, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QHBoxLayout, QOpenGLWidget, QSlider, QWidget

import OpenGL.GL as gl
import OpenGL.GLU as glu
import OpenGL.GLUT as glut
import numpy as np

from fileloader import *
from raytracing.raytracer import TrazadorDeRayos
from formulas.geometric_formulas import volumen,area_superficie,calcular_centro
from geometry.vec3 import Vec3


class GLWidget(QOpenGLWidget):
    x_rotacion_cambiada = pyqtSignal(int)
    y_rotacion_cambiada = pyqtSignal(int)
    z_rotacion_cambiada = pyqtSignal(int)
    x_posicion_cambiada = pyqtSignal(int)
    y_posicion_cambiada = pyqtSignal(int)
    zoom_grado_cambiado = pyqtSignal(int)

    def __init__(self, parent=None, nombre_archivo=""):
        super().__init__(parent)

        self.nombre_archivo = nombre_archivo
        self.objeto = None
        self.volumen_objeto = 0
        self.area_superficial_objeto = 0
        self.centro_objeto = Vec3(0, 0, 0)
        self.raytracer = 0
        self.rayos = None
        self.x_rot = 0
        self.y_rot = 0
        self.z_rot = 0
        self.x_pos = 0
        self.y_pos = 0
        self.zoom = -5.0
        self.fuente_sonido = None

        self.ultima_pos = QPoint()

        self.color_negro = QColor.fromRgb(0, 0, 0)
        self.color_blanco = QColor.fromRgb(255, 255, 255)

    def establecer_x_rotacion(self, angulo):
        """
        Establece la rotación en X del modelo.
        """
        angulo = self.normalizar_angulo(angulo)
        if angulo != self.x_rot:
            self.x_rot = angulo
            self.x_rotacion_cambiada.emit(angulo)
            self.update()

    def establecer_y_rotacion(self, angulo):
        """
        Establece la rotación en Y del modelo.
        """
        angulo = self.normalizar_angulo(angulo)
        if angulo != self.y_rot:
            self.y_rot = angulo
            self.y_rotacion_cambiada.emit(angulo)
            self.update()

    def establecer_z_rotacion(self, angulo):
        """
        Establece la rotación en Z del modelo.
        """
        angulo = self.normalizar_angulo(angulo)
        if angulo != self.z_rot:
            self.z_rot = angulo
            self.z_rotacion_cambiada.emit(angulo)
            self.update()

    def establecer_x_posicion(self, unidades):
        """
        Establece la posición en X de la cámara.
        """
        if unidades != self.x_pos:
            self.x_pos = unidades
            self.x_posicion_cambiada.emit(unidades)
            self.update()

    def establecer_y_posicion(self, unidades):
        """
        Establece la posición en Y de la cámara.
        """
        if unidades != self.y_pos:
            self.y_pos = unidades
            self.y_posicion_cambiada.emit(unidades)
            self.update()

    def establecer_zoom(self, angulo):
        """
        Establece el factor de zoom de la cámara.
        """
        if angulo < 0:
            angulo = self.centro_objeto.z * 0.2
        else:
            angulo = -self.centro_objeto.z * 0.2
        self.zoom += angulo
        self.zoom_grado_cambiado.emit(angulo)
        self.update()

    def establecer_fuente_sonido(self, x, y, z):
        """
        Establece la posición visual de la fuente de sonido.
        """
        self.fuente_sonido = Vec3(x, y, z)
        self.update()

    def cargar_modelo(self, nombre_archivo):
        """
        Carga el archivo especificado y genera el modelo correspondiente.
        """
        self.nombre_archivo = nombre_archivo
        self.archivo_obj = CargadorObj(nombre_archivo)
        self.vertices_objeto = self.archivo_obj.vertices
        self.caras_objeto = self.archivo_obj.caras

        # Calcular las propiedades geométricas del objeto
        self.volumen_objeto = volumen(self.vertices_objeto, self.caras_objeto)
        self.area_superficial_objeto = area_superficial(self.caras_objeto)
        self.centro_objeto = calc_centro(self.vertices_objeto, self.caras_objeto)

        self.x_pos = -self.centro_objeto.x
        self.y_pos = -self.centro_objeto.y
        self.zoom = -self.centro_objeto.z * 10
        self.fuente_sonido = Vec3(*self.centro_objeto)
        self.objeto = self.archivo_obj.renderizar()
        self.update()

    def refrescar_modelo(self, vista_material):
        """
        Refresca el modelo para mostrar cualquier cambio de material o de vista.
        """
        self.objeto = self.archivo_obj.renderizar(vista_material)
        self.update()

    def initializeGL(self):
        """
        Método del ciclo de vida de OpenGL. No cambiar el nombre. 
        """
        self.establecer_color_fondo(self.color_blanco)
        self.establecer_color(self.color_negro)

        gl.glShadeModel(gl.GL_FLAT)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        gl.glEnable(gl.GL_BLEND)

    def paintGL(self):
        """
        Método del ciclo de vida de OpenGL. No cambiar el nombre. 
        """
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()

        # Centrar en el modelo
        gl.glTranslate(self.x_pos, self.y_pos, self.zoom)

        # Rotar el modelo alrededor de su centro
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glTranslate(self.centro_objeto.x, self.centro_objeto.y, self.centro_objeto.z)

        gl.glRotated(self.x_rot / 16.0, 1.0, 0.0, 0.0)
        gl.glRotated(self.y_rot / 16.0, 0.0, 1.0, 0.0)
        gl.glRotated(self.z_rot / 16.0, 0.0, 0.0, 1.0)

        gl.glTranslate(
            -self.centro_objeto.x, -self.centro_objeto.y, -self.centro_objeto.z
        )

        if self.objeto is not None:
            gl.glCallList(self.objeto)
        if self.fuente_sonido is not None:
            gl.glPointSize(10)
            gl.glBegin(gl.GL_POINTS)
            gl.glColor3f(1.0, 0, 0)
            gl.glVertex3fv(self.fuente_sonido.vec)
            gl.glEnd()
        if self.rayos is not None:
            gl.glCallList(self.rayos)

        gl.glPopMatrix()

    def resizeGL(self, ancho, alto):
        """
        Método del ciclo de vida de OpenGL. No cambiar el nombre. 
        """
        lado = min(ancho, alto)
        if lado < 0:
            return

        gl.glViewport(0, 0, lado, lado)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        glu.gluPerspective(45.0, float(ancho) / float(alto), 0.1, 100000.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def ejecutar_raytracer(self, db_inicial=120, frecuencia=1000, reflexiones=0):
        """
        Ejecuta el algoritmo de trazado de rayos para generar el mapa de decibelios del modelo.
        """
        self.raytracer = RayTracer(
            self.fuente_sonido, 1000, self.archivo_obj.caras, db_inicial, frecuencia, reflexiones
        )
        self.rayos = self.raytracer.renderizar()
        self.update()

    def mousePressEvent(self, evento):
        """
        Registra dónde se hizo clic con el mouse.
        """
        self.ultima_pos = evento.pos()

    def mouseMoveEvent(self, evento):
        """
        Registra qué botones del mouse se hicieron clic cuando se mueve.
        """
        dx = evento.x() - self.ultima_pos.x()
        dy = evento.y() - self.ultima_pos.y()

        modificadores = QApplication.keyboardModifiers()

        # Arrastrar para mover el objeto
        # Shift + Arrastrar para rotar el objeto
        if evento.buttons() & Qt.LeftButton and modificadores == Qt.ShiftModifier:
            self.establecer_x_rotacion(self.x_rot + 8 * dy)
            self.establecer_y_rotacion(self.y_rot + 8 * dx)
        elif evento.buttons() & Qt.LeftButton:
            self.establecer_x_posicion(self.x_pos + dx / 100)
            self.establecer_y_posicion(self.y_pos - dy / 100)
        elif evento.buttons() & Qt.RightButton and modificadores == Qt.ShiftModifier:
            self.establecer_x_rotacion(self.x_rot + 8 * dy)
            self.establecer_z_rotacion(self.z_rot + 8 * dx)

        self.ultima_pos = evento.pos()

    def wheelEvent(self, evento):
        """
        Registra cuánto se movió la rueda del mouse.
        """
        # Usar la rueda del mouse para acercar/alejar
        self.ultima_pos = evento.pos()
        d = -float(evento.angleDelta().y())
        self.establecer_zoom(d)

    def normalizar_angulo(self, angulo):
        """
        Normaliza el ángulo que gira la rueda del mouse.
        """
        while angulo < 0:
            angulo += 360 * 16
        while angulo > 360 * 16:
            angulo -= 360 * 16
        return angulo

    def establecer_color_fondo(self, c):
        """
        Establece el color de fondo de la escena.
        """
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def establecer_color(self, c):
        """
        Establece el conjunto de colores de la escena.
        """
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())
