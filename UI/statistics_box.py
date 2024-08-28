from PyQt5.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt5.QtWidgets import (
    QGroupBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QComboBox,
    QSizePolicy,
    QMessageBox,
    QSpacerItem,
)
from PyQt5.QtGui import QValidator, QDoubleValidator, QIntValidator

import webbrowser
import numpy as np


class CajaEstadisticas(QGroupBox):
    actualizar_fuente_sonido = pyqtSignal(float, float, float)
    actualizar_frecuencia = pyqtSignal(int)
    calcular_mapa_db = pyqtSignal(int, int)
    calcular_rt60 = pyqtSignal(QLineEdit)
    calcular_distancia_critica = pyqtSignal(QLineEdit)

    def __init__(self, str, parent=None):
        super().__init__(str, parent)
        self.app = parent
        self.politica_minima_tamaño = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.db_inicial = 120
        self.reflexion = 0
        self.frecuencia = 1000

        layout = QVBoxLayout()
        layout.setSpacing(10)
        self.agregar_fuente_sonido(layout)
        self.agregar_mapa_db(layout)
        self.agregar_reverberacion(layout)
        self.agregar_distancia_critica(layout)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.setLayout(layout)

    def agregar_fuente_sonido(self, layout: QVBoxLayout) -> QGridLayout:
        """
        Agrega el componente de Fuente de Sonido a la Caja de Estadísticas
        """
        etiqueta_fuente_sonido = QLabel("Fuente de Sonido")
        etiqueta_fuente_sonido.setAlignment(Qt.AlignLeft)

        # Coordenada X
        etiqueta_x_fuente_sonido = QLabel("X:")
        etiqueta_x_fuente_sonido.setAlignment(Qt.AlignRight)
        x_fuente_sonido = QLineEdit()
        # x_fuente_sonido.setValidator(QDoubleValidator())
        x_fuente_sonido.setSizePolicy(self.politica_minima_tamaño)
        x_fuente_sonido.setAlignment(Qt.AlignCenter)
        # Coordenada Y
        etiqueta_y_fuente_sonido = QLabel("Y:")
        etiqueta_y_fuente_sonido.setAlignment(Qt.AlignRight)
        y_fuente_sonido = QLineEdit()
        # y_fuente_sonido.setValidator(QDoubleValidator())
        y_fuente_sonido.setSizePolicy(self.politica_minima_tamaño)
        y_fuente_sonido.setAlignment(Qt.AlignCenter)
        # Coordenada Z
        etiqueta_z_fuente_sonido = QLabel("Z:")
        etiqueta_z_fuente_sonido.setAlignment(Qt.AlignRight)
        z_fuente_sonido = QLineEdit()
        # z_fuente_sonido.setValidator(QDoubleValidator())
        z_fuente_sonido.setSizePolicy(self.politica_minima_tamaño)
        z_fuente_sonido.setAlignment(Qt.AlignCenter)

        # Botón "Establecer" para la Fuente de Sonido
        btn_establecer_fuente_sonido = QPushButton("Establecer")
        btn_establecer_fuente_sonido.setToolTip("Establece las coordenadas de la fuente de sonido")
        btn_establecer_fuente_sonido.clicked.connect(
            lambda: self.establecer_fuente_sonido(
                x_fuente_sonido, y_fuente_sonido, z_fuente_sonido
            )
        )

        layout_fuente_sonido = QGridLayout()
        layout_fuente_sonido.setContentsMargins(20, 0, 20, 0)
        layout_fuente_sonido.setSpacing(20)
        layout_fuente_sonido.addWidget(etiqueta_x_fuente_sonido, 0, 0, 1, 1)
        layout_fuente_sonido.addWidget(x_fuente_sonido, 0, 1, 1, 1)
        layout_fuente_sonido.addWidget(etiqueta_y_fuente_sonido, 1, 0, 1, 1)
        layout_fuente_sonido.addWidget(y_fuente_sonido, 1, 1, 1, 1)
        layout_fuente_sonido.addWidget(etiqueta_z_fuente_sonido, 2, 0, 1, 1)
        layout_fuente_sonido.addWidget(z_fuente_sonido, 2, 1, 1, 1)
        layout_fuente_sonido.addWidget(btn_establecer_fuente_sonido, 0, 3, 3, 2)

        layout.addWidget(etiqueta_fuente_sonido)
        layout.addLayout(layout_fuente_sonido)

    def agregar_mapa_db(self, layout: QVBoxLayout) -> QGridLayout:
        """
        Agrega el componente de Mapa de Decibelios a la Caja de Estadísticas
        """
        # Mapa de Decibelios
        etiqueta_mapa_db = QLabel("Generar Mapa de Decibelios")
        etiqueta_mapa_db.setAlignment(Qt.AlignLeft)
        # etiqueta_mapa_db.setFont(QFont("Arial", 16))

        # Entrada de Decibelios Iniciales
        etiqueta_db_inicial = QLabel("Nivel de Decibelios Inicial")
        etiqueta_db_inicial.setAlignment(Qt.AlignLeft)

        db_inicial = QLineEdit()
        db_inicial.setText("120")
        # db_inicial.setValidator(QIntValidator(0, 120))
        db_inicial.setSizePolicy(self.politica_minima_tamaño)
        db_inicial.setAlignment(Qt.AlignCenter)
        db_inicial.setToolTip("En el rango de 0-120")
        db_inicial.textChanged.connect(lambda: self.establecer_db_inicial(db_inicial))

        # Selección de Frecuencia
        etiqueta_seleccion_frecuencia = QLabel("Frecuencia")
        etiqueta_seleccion_frecuencia.setAlignment(Qt.AlignLeft)

        seleccion_frecuencia = QComboBox()
        seleccion_frecuencia.addItems(["125", "250", "500", "1000", "2000", "4000"])
        seleccion_frecuencia.setCurrentText("1000")
        seleccion_frecuencia.currentTextChanged.connect(self.establecer_frecuencia)

        # Reflexiones
        etiqueta_seleccion_reflexion = QLabel("Reflexiones")
        etiqueta_seleccion_reflexion.setAlignment(Qt.AlignLeft)

        seleccion_reflexion = QComboBox()
        seleccion_reflexion.addItems(["0", "1", "2"])
        seleccion_reflexion.setCurrentText("0")
        seleccion_reflexion.currentTextChanged.connect(self.establecer_reflexion)

        btn_mapa_db = QPushButton("Calcular")
        btn_mapa_db.setToolTip("Genera el Mapa de Decibelios")
        btn_mapa_db.clicked.connect(self.mapa_db)

        btn_info_mapa_db = QPushButton("Ver Detalles")
        btn_info_mapa_db.setToolTip("Ver detalles del cálculo del Mapa de Decibelios")
        btn_info_mapa_db.clicked.connect(self.info_decibelios)

        layout_btn_mapa_db = QGridLayout()
        layout_btn_mapa_db.setContentsMargins(20, 0, 20, 0)
        layout_btn_mapa_db.setSpacing(20)
        layout_btn_mapa_db.addWidget(etiqueta_db_inicial, 0, 0, 1, 1)
        layout_btn_mapa_db.addWidget(db_inicial, 0, 1, 1, 1)
        layout_btn_mapa_db.addWidget(etiqueta_seleccion_frecuencia, 1, 0, 1, 1)
        layout_btn_mapa_db.addWidget(seleccion_frecuencia, 1, 1, 1, 1)
        layout_btn_mapa_db.addWidget(etiqueta_seleccion_reflexion, 2, 0, 1, 1)
        layout_btn_mapa_db.addWidget(seleccion_reflexion, 2, 1, 1, 1)
        layout_btn_mapa_db.addWidget(btn_mapa_db, 3, 0, 1, 1)
        layout_btn_mapa_db.addWidget(btn_info_mapa_db, 3, 1, 1, 1)

        layout.addWidget(etiqueta_mapa_db)
        layout.addLayout(layout_btn_mapa_db)

    def agregar_reverberacion(self, layout: QVBoxLayout) -> QGridLayout:
        """
        Agrega el componente de tiempo de reverberación a la Caja de Estadísticas.
        """
        etiqueta_reverberacion = QLabel("Tiempo de Reverberación")
        etiqueta_reverberacion.setAlignment(Qt.AlignLeft)

        salida_reverberacion = QLineEdit()
        salida_reverberacion.setAlignment(Qt.AlignCenter)
        salida_reverberacion.setReadOnly(True)

        btn_calcular_reverberacion = QPushButton("Calcular")
        btn_calcular_reverberacion.setToolTip("Calcular Tiempo de Reverberación")
        btn_calcular_reverberacion.clicked.connect(lambda: self.calcular_rt60(salida_reverberacion))

        btn_info_reverberacion = QPushButton("Ver Detalles")
        btn_info_reverberacion.setToolTip("Ver detalles del cálculo del Tiempo de Reverberación")
        btn_info_reverberacion.clicked.connect(self.info_rt60)

        layout_btn_reverberacion = QGridLayout()
        layout_btn_reverberacion.setContentsMargins(20, 0, 20, 0)
        layout_btn_reverberacion.setSpacing(20)
        layout_btn_reverberacion.addWidget(salida_reverberacion, 0, 1, 1, 2)
        layout_btn_reverberacion.addWidget(btn_calcular_reverberacion, 1, 0, 1, 2)
        layout_btn_reverberacion.addWidget(btn_info_reverberacion, 1, 2, 1, 2)

        layout.addWidget(etiqueta_reverberacion)
        layout.addLayout(layout_btn_reverberacion)

    def agregar_distancia_critica(self, layout: QVBoxLayout) -> QGridLayout:
        """
        Agrega el componente de distancia crítica a la Caja de Estadísticas.
        """
        etiqueta_distancia_critica = QLabel("Distancia Crítica")
        etiqueta_distancia_critica.setAlignment(Qt.AlignLeft)

        salida_distancia_critica = QLineEdit()
        salida_distancia_critica.setAlignment(Qt.AlignCenter)
        salida_distancia_critica.setReadOnly(True)

        btn_calcular_distancia_critica = QPushButton("Calcular")
        btn_calcular_distancia_critica.setToolTip("Calcular Distancia Crítica")
        btn_calcular_distancia_critica.clicked.connect(
            lambda: self.calcular_distancia_critica(salida_distancia_critica)
        )

        btn_info_distancia_critica = QPushButton("Ver Detalles")
        btn_info_distancia_critica.setToolTip(
            "Ver detalles del cálculo de la Distancia Crítica"
        )
        btn_info_distancia_critica.clicked.connect(self.info_distancia_critica)

        layout_btn_distancia_critica = QGridLayout()
        layout_btn_distancia_critica.setContentsMargins(20, 0, 20, 0)
        layout_btn_distancia_critica.setSpacing(20)
        layout_btn_distancia_critica.addWidget(salida_distancia_critica, 0, 1, 1, 2)
        layout_btn_distancia_critica.addWidget(btn_calcular_distancia_critica, 1, 0, 1, 2)
        layout_btn_distancia_critica.addWidget(btn_info_distancia_critica, 1, 2, 1, 2)

        layout.addWidget(etiqueta_distancia_critica)
        layout.addLayout(layout_btn_distancia_critica)

    @pyqtSlot()
    def establecer_fuente_sonido(self, x_in: QLineEdit, y_in: QLineEdit, z_in: QLineEdit):
        """
        Valida y establece la ubicación de la fuente de sonido en el modelo.
        """
        if self.app.modelo_cargado:
            x, y, z = 0, 0, 0
            validador = QDoubleValidator()
            estado_x, _, _ = validador.validate(x_in.text(), 0)
            estado_y, _, _ = validador.validate(y_in.text(), 0)
            estado_z, _, _ = validador.validate(z_in.text(), 0)

            if estado_x == QValidator.Acceptable:
                x = float(x_in.text())
            else:
                x_in.setText("0.0")

            if estado_y == QValidator.Acceptable:
                y = float(y_in.text())
            else:
                y_in.setText("0.0")

            if estado_z == QValidator.Acceptable:
                z = float(z_in.text())
            else:
                z_in.setText("0.0")
            self.actualizar_fuente_sonido.emit(x, y, z)

    @pyqtSlot(str)
    def establecer_frecuencia(self, freq_str: str):
        """
        Establece la frecuencia a usar al calcular el mapa de decibelios del modelo.
        """
        self.frecuencia = int(freq_str)
        self.actualizar_frecuencia.emit(self.frecuencia)

    @pyqtSlot(str)
    def establecer_db_inicial(self, input: QLineEdit):
        """
        Establece el nivel de decibelios inicial a usar al calcular el mapa de decibelios del modelo.
        """
        estado, _, _ = QIntValidator(0, 120).validate(input.text(), 0)
        if estado == QValidator.Acceptable:
            self.db_inicial = int(input.text())
        else:
            input.setText("0")

    @pyqtSlot(str)
    def establecer_reflexion(self, reflection_str: str):
        """
        Establece el número de reflexiones a usar al calcular el mapa de decibelios del modelo.
        """
        self.reflexion = int(reflection_str)

    @pyqtSlot()
    def mapa_db(self):
        """
        Calcula el mapa de decibelios del objeto.
        """
        if self.app.modelo_cargado:
            cuadro_mensaje = QMessageBox(self)
            cuadro_mensaje.setWindowTitle("Generar Mapa dB")
            cuadro_mensaje.setIcon(QMessageBox.Question)
            cuadro_mensaje.setText(
                "<p>¿Desea generar el mapa de decibelios para esta sala?</p>"
                "<p><i>Esto puede tardar un poco</i></p>"
            )
            cuadro_mensaje.addButton(QPushButton("No"), QMessageBox.NoRole)
            cuadro_mensaje.addButton(QPushButton("Sí"), QMessageBox.YesRole)

            respuesta_boton = cuadro_mensaje.exec()

            if respuesta_boton == 1:  # Sí
                self.calcular_mapa_db.emit(self.db_inicial, self.reflexion)

    @pyqtSlot()
    def info_decibelios(self):
        """
        Abre un modal que contiene información sobre los decibelios y el proceso de cómo
        se calcula el mapa de decibelios.
        """
        cuadro_info = QMessageBox(self)
        cuadro_info.setWindowTitle("Información sobre el Mapa de Decibelios")
        cuadro_info.setIcon(QMessageBox.Information)
        cuadro_info.setText(
            """
            <head>
            <style>
            .caja-color {
                width: 10px;
                height: 10px;
                display: inline-block;
                background-color: #ccc;
            }
            </style>
            </head>
            <p>El nivel de presión sonora se mide en decibelios (dB), que son la medida objetiva de cuán 'fuerte' 
            es un sonido a una distancia determinada de la fuente del sonido. Los decibelios operan en una escala logarítmica 
            de base 10 que se alinea muy de cerca con la forma en que el oído humano percibe los niveles de sonido.</p>
            <p>Las propiedades interesantes del nivel de presión sonora en decibelios incluyen:</p>
            <ul>
            <li>Duplicar la distancia del oyente a la fuente de sonido resulta en un cambio de -6 dB</li>
            <li>Reducir a la mitad la distancia del oyente a la fuente de sonido resulta en un cambio de +6 dB</li>
            </ul>
            <p>La fórmula para encontrar el nivel de decibelios de una fuente de sonido a una nueva distancia r<sub>2</sub> es:</p>
            <p><strong>L<sub>2</sub> = L<sub>1</sub> + 20log(r<sub>2</sub>/r<sub>1</sub>)</p>
            <p>L<sub>1</sub> = el nivel de presión sonora en dB a r<sub>1</sub></p>
            <p>r<sub>2</sub> = la nueva distancia desde la fuente de sonido</p>
            <p>r<sub>1</sub> = la distancia antigua desde la fuente de sonido</p>
            <p>La escala de colores dB utilizada es:</p>
            <div class="caja-color" style="background-color: #ff0000;">120 dB</div>
            <div class="caja-color" style="background-color: #ff7f00;">100 dB</div>
            <div class="caja-color" style="background-color: #ffff00;">80 dB</div>
            <div class="caja-color" style="background-color: #7fff00;">60 dB</div>
            <div class="caja-color" style="background-color: #00ff00;">40 dB</div>
            <div class="caja-color" style="background-color: #00ff7f;">20 dB</div>
            <div class="caja-color" style="background-color: #00ffff;">0 dB</div>
            """
        )
        cuadro_info.addButton(QPushButton("Más Información"), QMessageBox.HelpRole)
        cuadro_info.addButton(QPushButton("Cerrar"), QMessageBox.RejectRole)
        respuesta_boton = cuadro_info.exec()

        if respuesta_boton == 0:
            webbrowser.open(
                "https://es.wikipedia.org/wiki/Decibelio", new=0, autoraise=True
            )

    @pyqtSlot()
    def calcular_rt60(self, salida):
        """
        Calcula el valor de RT60 del modelo actual.
        """
        if self.app.modelo_cargado:
            self.calcular_rt60.emit(salida)

    @pyqtSlot()
    def info_rt60(self):
        """
        Abre un modal que contiene información sobre la reverberación y el proceso de cómo
        se calcula el tiempo de reverberación.
        """
        cuadro_info = QMessageBox(self)
        cuadro_info.setWindowTitle("Información sobre RT60")
        cuadro_info.setIcon(QMessageBox.Information)
        cuadro_info.setText(
            """
            <p>La reverberación es la persistencia del sonido en una sala después de que se produce y se puede escuchar fácilmente 
            si haces un sonido en un espacio grande, como una iglesia, y puedes escuchar el sonido en la sala mucho después de que hayas dejado de hacerlo.</p>
            <p>La reverberación de una sala depende de:</p>
            <ul>
            <li>La banda de frecuencia del sonido producido</li>
            <li>El área de la sala</li>
            <li>De qué materiales están hechas sus superficies y cuánta energía sonora absorben</li>
            </ul>
            <p>Una medida objetiva común de la reverberación se conoce como RT60 (Tiempo de Reverberación 60dB), que es la medida 
            de cuánto tiempo tarda el nivel de presión sonora de una sala en disminuir en 60 dB después de que se haya generado.</p>
            <p>La fórmula utilizada para calcular el RT60 de una sala:</p>
            <p><strong>RT60 = 0.161 * V/A</strong></p>
            <p>V = volumen de la sala en m<sup>3</sup></p>
            <p>A = ∑𝑎∗𝑆 donde a = el coeficiente de absorción y S = el área de la superficie en m<sup>2</sup></p>
            """
        )
        cuadro_info.addButton(QPushButton("Más Información"), QMessageBox.HelpRole)
        cuadro_info.addButton(QPushButton("Cerrar"), QMessageBox.RejectRole)
        respuesta_boton = cuadro_info.exec()

        if respuesta_boton == 0:
            webbrowser.open(
                "https://es.wikipedia.org/wiki/Reverberaci%C3%B3n", new=0, autoraise=True
            )

    @pyqtSlot()
    def calcular_distancia_critica(self, salida):
        """
        Calcula el valor de la Distancia Crítica del modelo actual.
        """
        if self.app.modelo_cargado:
            self.calcular_distancia_critica.emit(salida)

    @pyqtSlot()
    def info_distancia_critica(self):
        """
        Abre un modal que contiene información sobre las distancias críticas y el proceso de cómo
        se calcula la distancia crítica.
        """
        cuadro_info = QMessageBox(self)
        cuadro_info.setWindowTitle("Información sobre la Distancia Crítica")
        cuadro_info.setIcon(QMessageBox.Information)
        cuadro_info.setText(
            """
            <p>La distancia crítica de una sala es el punto dentro de ella donde el nivel de presión sonora de los sonidos reverberantes (reflejados) 
            es igual al nivel de presión sonora directamente desde la fuente.</p>
            <p>Este ‘punto dulce’ se puede encontrar manualmente si te mueves por una sala mientras un altavoz está sonando y puedes encontrar un punto 
            donde el sonido es mucho más fuerte que en cualquier otro lugar.</p>
            <p>Esta ubicación depende del área de la sala, así como de la composición de sus superficies reflectantes y se calcula convenientemente 
            con el valor de RT60 de una sala, lo que lo convierte en una estadística fácil de proporcionar al usuario si también se proporciona el tiempo de reverberación.</p>
            <p>La fórmula utilizada para calcular la Distancia Crítica de una sala:</p>
            <p><strong>Distancia Crítica = 0.057 * &radic;(V/RT60)</strong></p>
            <p>V = volumen de la sala en m<sup>3</sup></p>
            <p>RT60 = la medida de RT60 para la sala</p>
            """
        )
        cuadro_info.addButton(QPushButton("Más Información"), QMessageBox.HelpRole)
        cuadro_info.addButton(QPushButton("Cerrar"), QMessageBox.RejectRole)
        respuesta_boton = cuadro_info.exec()

        if respuesta_boton == 0:
            webbrowser.open(
                "https://es.wikipedia.org/wiki/Distancia_cr%C3%ADtica", new=0, autoraise=True
            )
