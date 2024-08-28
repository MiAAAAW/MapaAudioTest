import sys

from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QSizePolicy,
    QGridLayout,
    QTabWidget,
    QWidget,
    QApplication,
    QMainWindow,
    QLineEdit,
)

import numpy as np
import webbrowser

from UI.menu_bar import BarraMenu
from UI.opengl_box import CajaOpenGL
from UI.statistics_box import CajaEstadisticas
from UI.material_box import CajaMaterial


class App(QMainWindow):
    ventanaRedimensionada = pyqtSignal(int, int)
    ventanaMovida = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        self.titulo = "dB-mapper"
        self.izquierda = 50
        self.arriba = 30
        self.ancho = 1400
        self.alto = 900
        self.modelo_cargado = False
        self.politicaMinimaTamaño = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.frecuencia = 1000
        self.reflexion = 0
        self.vista_material = False
        self.iniciarUI()

    def iniciarUI(self):
        """
        Configura los elementos de la interfaz de usuario de la aplicación.
        """
        self.setWindowTitle(self.titulo)
        self.setGeometry(self.izquierda, self.arriba, self.ancho, self.alto)

        # self.createMenuBar()
        self.menu_bar = BarraMenu(parent=self)
        self.setMenuBar(self.menu_bar)
        self.menu_bar.abrir.connect(self.cargar_modelo)
        self.menu_bar.guardar.connect(self.guardar_modelo)
        # self.createOpenGLBox()
        self.opengl_box = CajaOpenGL("Vista del Modelo")
        # self.createStatBox()
        self.stat_box = CajaEstadisticas("Cálculos Acústicos", parent=self)
        self.stat_box.actualizar_fuente_sonido.connect(self.actualizar_fuente_sonido)
        self.stat_box.actualizar_frecuencia.connect(self.actualizar_frecuencia)
        self.stat_box.calcular_mapa_db.connect(self.calcular_mapa_db)
        self.stat_box.calcular_rt60.connect(self.calcular_rt60)
        self.stat_box.calcular_distancia_critica.connect(self.calcular_distancia_critica)
        # self.createTreatmentBox()
        self.material_box = CajaMaterial("Materiales")
        self.material_box.actualizar_vista.connect(self.actualizar_vista)

        layoutPrincipal = QGridLayout()
        layoutPrincipal.addWidget(self.opengl_box, 0, 0, 2, 2)

        pestañas = QTabWidget()
        pestañas.setTabPosition(QTabWidget.East)
        pestañas.addTab(self.stat_box, "Estadísticas")
        pestañas.addTab(self.material_box, "Materiales")
        pestañas.setSizePolicy(self.politicaMinimaTamaño)

        layoutPrincipal.addWidget(pestañas, 0, 2, 2, 1)

        widget = QWidget()
        widget.setLayout(layoutPrincipal)
        self.setCentralWidget(widget)

        self.statusBar().showMessage("v1.0.0")
        self.show()

    def resizeEvent(self, event):
        """
        Evento de Qt\n
        Se activa cuando la ventana es redimensionada.
        """
        ancho = event.size().width()
        alto = event.size().height()

        self.ancho = ancho
        self.alto = alto

        self.ventanaRedimensionada.emit(ancho, alto)

    def moveEvent(self, event):
        """
        Evento de Qt\n
        Se activa cuando la ventana es movida.
        """
        izquierda = event.pos().x()
        arriba = event.pos().y()

        self.izquierda = izquierda
        self.arriba = arriba

        self.ventanaMovida.emit(izquierda, arriba)

    @pyqtSlot(str)
    def cargar_modelo(self, nombre_archivo):
        """
        Señal emitida cuando se selecciona un archivo para cargar.
        """
        self.opengl_box.load_model(nombre_archivo)
        caras_modelo = self.opengl_box.obtener_caras_modelo()
        self.material_box.actualizar_caja_material(caras_modelo, self.frecuencia)
        self.modelo_cargado = True

    @pyqtSlot(str)
    def guardar_modelo(self, nombre_archivo):
        """
        Señal emitida cuando se selecciona un archivo para guardar 
        el buffer de cuadros actual.
        """
        if self.modelo_cargado:
            self.opengl_box.guardar_buffer_frame(nombre_archivo)

    @pyqtSlot(list)
    def actualizar_caja_estadisticas(self, centro_modelo: list):
        """
        TODO\n
        Actualiza los campos de la caja de estadísticas cuando se carga un modelo. 
        Es decir, establece los campos de la fuente de sonido en las coordenadas del centro del objeto.
        """
        pass

    @pyqtSlot(float, float, float)
    def actualizar_fuente_sonido(self, x: float, y: float, z: float):
        """
        Señal emitida cuando se actualizan los campos de la fuente de sonido.
        """
        self.opengl_box.actualizar_fuente_sonido(x, y, z)

    @pyqtSlot(int)
    def actualizar_frecuencia(self, frecuencia: int):
        """
        Señal emitida cuando se actualiza el campo de frecuencia.
        """
        self.frecuencia = frecuencia
        self.material_box.actualizar_frecuencia(frecuencia)

    @pyqtSlot(int, int)
    def calcular_mapa_db(self, db_inicial: int, num_reflexiones: int):
        """
        Señal emitida cuando se hace clic en el botón de calcular para renderizar el 
        mapa de decibelios del modelo.
        """
        self.opengl_box.calcular_mapa_db(db_inicial, self.frecuencia, num_reflexiones)

    @pyqtSlot(QLineEdit)
    def calcular_rt60(self, salida):
        """
        Señal emitida cuando se hace clic en el botón de calcular para determinar 
        el valor RT60 del modelo.
        """
        reverberacion = self.opengl_box.calcular_rt60()
        salida.setText(str(np.round(reverberacion, 3)))

    @pyqtSlot(QLineEdit)
    def calcular_distancia_critica(self, salida):
        """
        Señal emitida cuando se hace clic en el botón de calcular para determinar 
        el valor de Distancia Crítica del modelo.
        """
        distancia_critica = self.opengl_box.calcular_distancia_critica()
        salida.setText(str(np.round(distancia_critica, 3)))

    @pyqtSlot(bool)
    def actualizar_vista(self, vista_material):
        """
        Señal emitida cuando se cambia el material de una superficie o se 
        hace clic en la casilla de verificación de vista de materiales.
        """
        self.opengl_box.actualizar_vista(vista_material)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
