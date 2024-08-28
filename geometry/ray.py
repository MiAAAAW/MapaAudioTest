from geometry.vec3 import Vec3
from geometry.materials import Materiales as mtl


class Rayo:
    def __init__(
        self,
        origen: Vec3,
        direccion: Vec3,
        dist_desde_origen: float = None,
        db: float = None,
    ):
        self.origen = origen
        self.direccion = direccion
        self.dist_desde_origen = dist_desde_origen
        self.db_inicial = db

    def __str__(self) -> str:
        """
        Proporciona una representación en cadena de texto útil de un objeto Rayo.
        """
        return (
            "Origen: "
            + self.origen.__str__()
            + " Dirección: "
            + self.direccion.__str__()
        )

    def calc_reflejo(self, phit, normal, dist_desde_origen, db) -> "Rayo":
        """
        Calcula el Rayo reflejado basado en la incidencia y la normal
        """
        rayo = Vec3(*(-(normal * (self.direccion.dot(normal) * 2)).sub(self.direccion)))
        return Rayo(phit, rayo, dist_desde_origen, db)
