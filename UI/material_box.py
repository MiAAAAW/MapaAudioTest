from PyQt5.Qt import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QCheckBox,
    QComboBox,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

import numpy as np

from geometry.materials import Materiales as mtl


class CajaMaterial(QGroupBox):
    actualizar_vista = pyqtSignal(bool)

    def __init__(self, str, parent=None):
        super().__init__(str)
        layout = QVBoxLayout()
        layout.setSpacing(10)

        self.desplegable_superficie = self.crear_desplegable_superficie()
        self.desplegable_material = self.crear_desplegable_material()
        self.configurar_cambiador_material(layout)
        self.tabla_sabine = self.crear_tabla_sabine(freq=1000)
        layout.addWidget(self.tabla_sabine)
        self.crear_vista_material(layout)
        self.vista_material = False
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    def crear_desplegable_superficie(self, caras_modelo=None):
        """
        Llena el desplegable de superficies
        """
        self.caras_modelo = caras_modelo

        superficies = QComboBox()

        if caras_modelo is not None:
            for i, cara in enumerate(caras_modelo):
                if np.array_equal(cara.normal.vec, [0.0, 1.0, 0.0]):
                    str_cara = "Techo [" + str(i) + "]"
                elif np.array_equal(cara.normal.vec, [0.0, -1.0, 0.0]):
                    str_cara = "Suelo [" + str(i) + "]"
                else:
                    str_cara = "Pared [" + str(i) + "]"
                superficies.addItem(str_cara, cara)
            superficies.addItem("Todos", None)
            superficies.model().sort(0)

        return superficies

    def crear_desplegable_material(self):
        """
        Llena el desplegable de materiales
        """
        materiales = QComboBox()

        materiales.addItem("Madera Dura", mtl.HARDWOOD)
        materiales.addItem("Alfombra", mtl.CARPET)
        materiales.addItem("Tablaroca", mtl.DRYWALL)
        materiales.addItem("Ladrillo", mtl.BRICK)
        materiales.addItem("Concreto", mtl.CONCRETE)
        materiales.addItem("Espuma", mtl.FOAM)

        return materiales

    def configurar_cambiador_material(self, layout):
        """
        Crea la sección de cambiador de materiales en la Caja de Materiales.
        """
        etiqueta_superficie = QLabel("Superficie")
        etiqueta_superficie.setAlignment(Qt.AlignLeft)
        etiqueta_material = QLabel("Material")
        etiqueta_material.setAlignment(Qt.AlignLeft)

        btn_cambiar_material = QPushButton("Cambiar Material")
        btn_cambiar_material.setToolTip("Cambiar material para la superficie elegida")
        btn_cambiar_material.clicked.connect(
            lambda: self.cambiar_material(
                self.desplegable_superficie.itemData(self.desplegable_superficie.currentIndex()),
                self.desplegable_material.itemData(self.desplegable_material.currentIndex()),
            )
        )

        self.layout_cambiador_material = QGridLayout()
        self.layout_cambiador_material.addWidget(etiqueta_superficie, 0, 0, 1, 1)
        self.layout_cambiador_material.addWidget(etiqueta_material, 0, 1, 1, 1)
        self.layout_cambiador_material.addWidget(self.desplegable_superficie, 1, 0, 1, 1)
        self.layout_cambiador_material.addWidget(self.desplegable_material, 1, 1, 1, 1)
        self.layout_cambiador_material.addWidget(btn_cambiar_material, 2, 0, 1, 2)

        layout.addLayout(self.layout_cambiador_material)

    def crear_tabla_sabine(self, freq) -> QTableWidget:
        """
        Crea la tabla de referencia del coeficiente de absorción de Sabine para
        la frecuencia actual
        """
        tabla_sabine = QTableWidget()
        tabla_sabine.setRowCount(6)
        tabla_sabine.setColumnCount(2)
        tabla_sabine.setHorizontalHeaderLabels(["Material", "Absorción"])

        materiales = [
            mtl.HARDWOOD,
            mtl.CARPET,
            mtl.DRYWALL,
            mtl.BRICK,
            mtl.CONCRETE,
            mtl.FOAM,
        ]

        for i, m in enumerate(materiales):
            tabla_sabine.setItem(i, 0, QTableWidgetItem(mtl.nombre(m)))
            a = QTableWidgetItem(str(mtl.absorcion(m, freq)))
            a.setTextAlignment(Qt.AlignCenter)
            tabla_sabine.setItem(i, 1, a)

        return tabla_sabine

    def crear_vista_material(self, layout):
        """
        Crea la casilla de verificación que alterna la vista del material.
        """
        etiqueta_vista_material = QLabel("Vista del Material")
        etiqueta_vista_material.setAlignment(Qt.AlignLeft)

        checkbox_vista_material = QCheckBox()
        checkbox_vista_material.stateChanged.connect(self.cambiar_vista_material)

        layout_vista_material = QHBoxLayout()
        layout_vista_material.addWidget(etiqueta_vista_material)
        layout_vista_material.addWidget(checkbox_vista_material)

        layout.addLayout(layout_vista_material)

    def actualizar_caja_material(self, caras_modelo, freq):
        """
        Actualiza el desplegable de superficies para el modelo actual.
        """
        nuevo_desplegable_superficie = self.crear_desplegable_superficie(caras_modelo)
        self.layout_cambiador_material.replaceWidget(
            self.desplegable_superficie, nuevo_desplegable_superficie
        )
        self.desplegable_superficie.close()
        self.desplegable_superficie = nuevo_desplegable_superficie

        # Actualizar modelo basado en el estado actual de la opción de vista de material
        self.actualizar_vista.emit(self.vista_material)

    def actualizar_freq(self, freq):
        """
        Actualiza la tabla de Sabine basada en la frecuencia actual.
        """
        nueva_tabla_sabine = self.crear_tabla_sabine(freq)
        self.layout().replaceWidget(self.tabla_sabine, nueva_tabla_sabine)
        self.tabla_sabine.close()
        self.tabla_sabine = nueva_tabla_sabine

    @pyqtSlot()
    def cambiar_material(self, cara, mtl):
        """
        Cambia el material de la cara especificada.
        """
        if cara is None:
            for cara in self.caras_modelo:
                cara.material = mtl
        else:
            cara.material = mtl
        self.actualizar_vista.emit(self.vista_material)

    @pyqtSlot(int)
    def cambiar_vista_material(self, estado):
        """
        Alterna el estado de la opción de vista de material.
        """
        estado_vista = estado == Qt.Checked
        self.vista_material = estado_vista
        self.actualizar_vista.emit(estado_vista)
