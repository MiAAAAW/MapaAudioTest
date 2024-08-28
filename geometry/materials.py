class Materiales:
    MADERA_DURA = 0
    ALFOMBRA = 1
    TABLAROCA = 2
    LADRILLO = 3
    CONCRETO = 4
    ESPUMA = 5

    @staticmethod
    def nombre(material: int):
        """
        Devuelve el nombre en cadena de texto de cada material.
        """
        return {
            Materiales.MADERA_DURA: "Madera Dura",
            Materiales.ALFOMBRA: "Alfombra",
            Materiales.TABLAROCA: "Tablaroca",
            Materiales.LADRILLO: "Ladrillo",
            Materiales.CONCRETO: "Concreto",
            Materiales.ESPUMA: "Espuma",
        }.get(material, "")

    @staticmethod
    def absorcion(material: int, freq: int) -> float:
        """
        Coeficiente de absorción a la frecuencia dada
        """
        if material == Materiales.MADERA_DURA:
            return {
                125: 0.19,
                250: 0.23,
                500: 0.25,
                1000: 0.30,
                2000: 0.37,
                4000: 0.42,
            }.get(freq, 0)
        elif material == Materiales.ALFOMBRA:
            return {
                125: 0.03,
                250: 0.09,
                500: 0.20,
                1000: 0.54,
                2000: 0.70,
                4000: 0.72,
            }.get(freq, 0)
        elif material == Materiales.TABLAROCA:
            return {
                125: 0.29,
                250: 0.10,
                500: 0.05,
                1000: 0.04,
                2000: 0.07,
                4000: 0.09,
            }.get(freq, 0)
        elif material == Materiales.LADRILLO:
            return {
                125: 0.05,
                250: 0.04,
                500: 0.02,
                1000: 0.04,
                2000: 0.05,
                4000: 0.05,
            }.get(freq, 0)
        elif material == Materiales.CONCRETO:
            return {
                125: 0.01,
                250: 0.01,
                500: 0.01,
                1000: 0.02,
                2000: 0.02,
                4000: 0.02,
            }.get(freq, 0)
        elif material == Materiales.ESPUMA:
            return {
                125: 0.25,
                250: 0.50,
                500: 0.85,
                1000: 0.95,
                2000: 0.90,
                4000: 0.90,
            }.get(freq, 0)
        else:
            return 0

    @staticmethod
    def color(material: int):
        """
        Devuelve el valor de color de cada material.
        """
        return {
            Materiales.MADERA_DURA: [0.34, 0.26, 0.01, 0.5],
            Materiales.ALFOMBRA: [0.23, 0.40, 0.72, 0.5],
            Materiales.TABLAROCA: [0.92, 0.89, 0.78, 0.5],
            Materiales.LADRILLO: [0.63, 0.09, 0, 0.5],
            Materiales.CONCRETO: [0.45, 0.45, 0.45, 0.5],
            Materiales.ESPUMA: [0.81, 0.77, 0.10, 0.5],
        }.get(material, [0, 0, 0, 0])
