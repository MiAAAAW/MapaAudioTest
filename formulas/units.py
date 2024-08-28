class Unidades:
    """
    Variables enumeradas para unidades de medida.
    """

    PULGADAS = 1
    PIES = 2
    CENTIMETROS = 3
    METROS = 4


def aPulgadas(valor, unidad):
    """
    Convierte el valor dado en su unidad dada a pulgadas.
    """
    nuevoValor = 0.0

    if unidad == Unidades.PULGADAS:
        nuevoValor = valor
    elif unidad == Unidades.PIES:
        nuevoValor = valor * 12
    elif unidad == Unidades.CENTIMETROS:
        nuevoValor = valor / 2.54
    elif unidad == Unidades.METROS:
        nuevoValor = valor * 39.37
    else:
        nuevoValor = -1

    return nuevoValor


def aPies(valor, unidad):
    """
    Convierte el valor dado en su unidad dada a pies.
    """
    nuevoValor = 0.0

    if unidad == Unidades.PULGADAS:
        nuevoValor = valor / 12
    elif unidad == Unidades.PIES:
        nuevoValor = valor
    elif unidad == Unidades.CENTIMETROS:
        nuevoValor = valor / 30.48
    elif unidad == Unidades.METROS:
        nuevoValor = valor * 3.281
    else:
        nuevoValor = -1

    return nuevoValor


def aCentimetros(valor, unidad):
    """
    Convierte el valor dado en su unidad dada a centímetros.
    """
    nuevoValor = 0.0

    if unidad == Unidades.PULGADAS:
        nuevoValor = valor * 2.54
    elif unidad == Unidades.PIES:
        nuevoValor = valor * 30.48
    elif unidad == Unidades.CENTIMETROS:
        nuevoValor = valor
    elif unidad == Unidades.METROS:
        nuevoValor = valor * 100
    else:
        nuevoValor = -1

    return nuevoValor


def aMetros(valor, unidad):
    """
    Convierte el valor dado en su unidad dada a metros.
    """
    nuevoValor = 0.0

    if unidad == Unidades.PULGADAS:
        nuevoValor = valor / 39.37
    elif unidad == Unidades.PIES:
        nuevoValor = valor / 3.281
    elif unidad == Unidades.CENTIMETROS:
        nuevoValor = valor / 100
    elif unidad == Unidades.METROS:
        nuevoValor = valor
    else:
        nuevoValor = -1

    return nuevoValor


def convertirUnidades(valor, unidadActual, nuevaUnidad):
    """
    Convierte el valor dado de sus unidades actuales a las unidades deseadas.
    """
    nuevoValor = 0

    opciones = {
        Unidades.PULGADAS: aPulgadas(valor, unidadActual),
        Unidades.PIES: aPies(valor, unidadActual),
        Unidades.CENTIMETROS: aCentimetros(valor, unidadActual),
        Unidades.METROS: aMetros(valor, unidadActual),
    }

    nuevoValor = opciones.get(nuevaUnidad)
    return nuevoValor
