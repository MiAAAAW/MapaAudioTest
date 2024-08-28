import math
from colorsys import hsv_to_rgb
from geometry.materials import Materiales as mtl


def caida_db(dist_1, dist_2):
    """
    Calcula el cambio en el nivel de decibelios entre dos distancias.
    """
    if dist_1 <= 0 or dist_2 <= 0:
        raise Exception("Las distancias desde la fuente no pueden ser 0")

    cambio_db = 20 * math.log10(dist_2 / dist_1)
    return cambio_db


def sumar_niveles(niveles):
    """
    Suma múltiples niveles de sonido.
    """
    if len(niveles) == 0:
        return 0

    suma_nivel = 0.0
    for nivel in niveles:
        if nivel > 0:
            suma_nivel += math.pow(10, float(nivel) / 10)

    return 10 * math.log10(suma_nivel) if suma_nivel > 0 else 0


def rt60(volumen, caras) -> float:
    """
    Tiempo de reverberación de la habitación denotada por las caras dadas.
    """
    suma_a = 0
    for cara in caras:
        suma_a += cara.surface_area * mtl.absorption(cara.material, 1000)
    reverb = 0.161 * (volumen / suma_a)

    return reverb


def dist_critica(volumen, caras):
    """
    Distancia crítica desde la fuente de sonido
    - El volumen está en metros cúbicos
    """
    reverb = rt60(volumen, caras)
    critica = 0.057 * math.sqrt(volumen / reverb)
    return critica


def db_a_color(nivel):
    """
    Convierte el nivel de dB dado (0-120) a RGB usando valores HSV
    - Rango de Rojo a Cian 
    - Rojo  ( >= 120dB ) = (0, 1, 1) HSV
    - Cian ( <=   0dB ) = (180, 1, 1)  HSV
    """

    # Asegura que el nivel esté dentro de los límites adecuados
    nivel = 0 if nivel < 0 else nivel
    nivel = 120 if nivel > 120 else nivel

    tono = (nivel - 120) * -1.5  # Tono HSV
    return hsv_to_rgb(tono / 360, 1, 1)
