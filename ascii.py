from classes.circulo_creator import Circle
from classes.mapa import Circular_map

def ascii(letter_asig: dict,client) -> Circular_map:
    """
    Generate an ASCII representation of the circular map based on the information received from the client.

    Parameters
    ----------
    letter_asig : dict
        Dictionary mapping team names to letters used in the representation.
    
    client : MountainClient
        The client object representing the connection to the servers.

    Returns
    -------
    Circular_map: 
        The circular map object with players added.

    """
    circle = Circle(46)
    mapa = Circular_map(circle)

    info = client.get_data()

    for equipo, escaladores in info.items():
        for escalador, infos in escaladores.items():
            x = infos['x']
            y = infos['y']

            if infos['cima'] is not True:
                cima = ""
            else:
                cima = True

            mapa.agregar_pj((x, y), letter_asig[equipo], cima)

    return mapa


if __name__ == "__main__":
    ascii()
