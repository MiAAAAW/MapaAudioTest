from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import QAction, QMenuBar, QFileDialog


class BarraMenu(QMenuBar):
    abrir = pyqtSignal(str)
    guardar = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.app = parent
        self.agregar_pestaña_archivo()
        self.agregar_pestaña_editar()
        self.agregar_pestaña_vista()

    def agregar_pestaña_archivo(self):
        """
        Agrega la pestaña Archivo al menú
        """
        pestaña_archivo = self.addMenu("Archivo")
        # Abrir
        accion_abrir = QAction("Abrir", self)
        accion_abrir.setShortcut("Ctrl+O")
        accion_abrir.triggered.connect(self.abrir_archivo)
        pestaña_archivo.addAction(accion_abrir)
        # Exportar
        accion_exportar = QAction("Exportar...", self)
        accion_exportar.setShortcut("Ctrl+E")
        accion_exportar.triggered.connect(self.guardar_archivo)
        pestaña_archivo.addAction(accion_exportar)

    def agregar_pestaña_editar(self):
        """
        Agrega la pestaña Editar al menú
        """
        pestaña_editar = self.addMenu("Editar")
        # Deshacer
        accion_deshacer = QAction("Deshacer", self)
        accion_deshacer.setShortcut("Ctrl+Z")
        pestaña_editar.addAction(accion_deshacer)
        # Rehacer
        accion_rehacer = QAction("Rehacer", self)
        accion_rehacer.setShortcut("Ctrl+Y")
        pestaña_editar.addAction(accion_rehacer)

    ### No implementado ###
    def agregar_pestaña_vista(self):
        """
        Agrega la pestaña Vista al menú
        """
        pestaña_vista = self.addMenu("Vista")
        # Apariencia
        subpestaña_apariencia = pestaña_vista.addMenu("Apariencia")
        # Pantalla completa
        accion_pantalla_completa = QAction("Pantalla completa", self)
        accion_pantalla_completa.setShortcut("F11")
        subpestaña_apariencia.addAction(accion_pantalla_completa)
        # Mostrar barra lateral
        accion_barra_lateral = QAction("Ver barra lateral", self, checkable=True)
        accion_barra_lateral.setChecked(True)
        subpestaña_apariencia.addAction(accion_barra_lateral)

    @pyqtSlot()
    def abrir_archivo(self):
        """
        Abre el cuadro de diálogo de archivos para que el usuario seleccione un archivo de entrada
        """
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.DontUseNativeDialog
        nombre_archivo, _ = QFileDialog.getOpenFileName(
            self, "Abrir Archivo", "", "Archivos 3D (*.obj)", options=opciones
        )

        if nombre_archivo:
            self.abrir.emit(nombre_archivo)

    @pyqtSlot()
    def guardar_archivo(self):
        """
        Abre el cuadro de diálogo de archivos para que el usuario seleccione un archivo para guardar
        """
        if self.app.modelo_cargado:
            opciones = QFileDialog.Options()
            opciones |= QFileDialog.DontUseNativeDialog
            nombre_archivo, _ = QFileDialog.getSaveFileName(
                self, "Guardar Archivo", "", "Imágenes (*.png *.xpm *.jpg)", options=opciones
            )
            self.guardar.emit(nombre_archivo)
