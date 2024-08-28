from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QGroupBox, QHBoxLayout, QLayout

from gl_widget import GLWidget
from geometry.vec3 import Vec3
from geometry.face import Cara
import formulas.db_formulas as db


class CajaOpenGL(QGroupBox):
    actualizar_caja_estadisticas = pyqtSignal(Vec3)

    def __init__(self, str, parent=None):
        super().__init__(str)
        self.gl_widget = GLWidget()
        layout = QHBoxLayout()
        layout.addWidget(self.gl_widget)
        self.setLayout(layout)

    def cargar_modelo(self, nombre_archivo: str):
        """
        Carga el modelo del archivo especificado en OpenGL.
        """
        self.gl_widget.load_model(nombre_archivo)

        self.actualizar_caja_estadisticas.emit(self.gl_widget.centro_objeto)

    def obtener_caras_modelo(self) -> [Cara]:
        return self.gl_widget.caras_objeto

    def actualizar_fuente_sonido(self, x: float, y: float, z: float):
        """
        Actualiza la posición de la fuente de sonido.
        """
        self.gl_widget.set_sound_source(x, y, z)

    def calcular_mapa_db(self, db_inicial: int, frecuencia: int, num_rayos: int):
        """
        Ejecuta el algoritmo de trazado de rayos para calcular el mapa de decibelios del modelo.
        """
        self.gl_widget.run_raytracer(start_db=db_inicial, freq=frecuencia, reflections=num_rayos)

    def calcular_rt60(self) -> float:
        """
        Calcula el valor de RT60 del modelo.
        """
        return db.rt60(self.gl_widget.volumen_objeto, self.gl_widget.caras_objeto)

    def calcular_distancia_critica(self) -> float:
        """
        Calcula el valor de la Distancia Crítica del modelo.
        """
        return db.crit_dist(self.gl_widget.volumen_objeto, self.gl_widget.caras_objeto)

    def actualizar_vista(self, vista_material):
        """
        Actualiza los materiales del modelo y si la vista de materiales está activa o no.
        """
        self.gl_widget.refresh_model(vista_material)

    def guardar_buffer_frame(self, nombre_archivo: str):
        """
        Guarda el buffer de cuadros actual en el archivo especificado.
        """
        imagen = self.gl_widget.grabFramebuffer()
        imagen.save(nombre_archivo, "PNG")
