import numpy as np

def move_to_point_direction(pos_o ,pos_f,vel = 50):
    """" 
    para ir a un punto lo mas rapido posible
    para ir a la max pos
    ubicar a jugadores cuando empiza el juego
    escapar de un max local si no ganamos para ir a un punto x
    """
    xo = pos_o[0]
    yo = pos_o[1]

    xf = pos_f[0]
    yf = pos_f[1]

    v = (xf - xo, yf - yo)
    v_direc = np.arctan(v[0]/v[1])

    if np.linalg.norm(v) < 50:
        vel = np.linalg.norm(v)
 
    return np.degrees(v_direc),vel


# print(move_to_point_direction((0,0),(10,10)))

def apply_gradient_ascent(pos_o, dx, dy, vel_x=0, vel_y=0, alpha=0.01, beta=0.5,vel=50):
    """
    para usar con el servidor
    """
    xo = pos_o[0]
    yo = pos_o[1]

    vel_x = beta * vel_x + alpha * dx
    vel_y = beta * vel_y + alpha * dy

    xf = xo - vel_x
    yf = yo - vel_x

    vx = xf - xo
    vy = yf - xo

    v_direc = np.arctan(vx/vy)
    v_dist = np.degrees(xf-xo, yf-yo)

    return v_direc, v_dist, vel_x, vel_y


def apply_momentum_gradient_ascent_2(pos_o, dx, dy, vel_x=0, vel_y=0, alpha=0.01, beta=0.5,vel=50):
    """
    para testear
    """
    xo = pos_o[0]
    yo = pos_o[1]

    vel_x = beta * vel_x + alpha * dx
    vel_y = beta * vel_y + alpha * dy

    xf = xo + vel_x
    yf = yo + vel_x

    return xf, yf

# def apply_stochastic_gradient_ascent():


def get_escalador_near_to_max(max_pos, pos_escaladores):
    """
    cual es el escalador mas cerca de un punnto
    y cual es la distancia
    """
    dist = {}
    for i in pos_escaladores:
        v = (((max_pos[0] - pos_escaladores[i][0]),(max_pos[1] - pos_escaladores[i][1])))
        d = (np.linalg.norm(v))
        dist[i] = d
    

    esc = min(dist, key=dist.get)
    dist_esc = dist[esc]

    return esc, dist_esc
    

# print(get_escalador_near_to_max((10,10), {'esc1':(1,1),'esc2':(9,9),'esc3':(9.5,9)}))


