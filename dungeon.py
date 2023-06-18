import random

def gen_matrix(fil, col, p = 30):
  """
  Genera una matriz (con listas) de dimensiones fil x col.
  Cada elemento puede ser 0 ó 1, que se asignan aleatoriamente con cierta
  probabilidad p (% de veces que sale 1).
  Inputs:
  fil-- cantidad de filas
  col-- cantidad de columnas
  Return:
  N -- matriz generada
  """
  # generamos una matriz de fil x col, rellena de ceros
  N = [[0 for _ in range(col)] for _ in range(fil)]
  # recorremos cada fila y columna para asignar unos y ceros aleatoriamente
  # (p es la probabilidad de elegir un 1)
  for i in range(fil):
    for j in range(col):
      N[i][j]=random.choice([1]*p + [0]*100)
  return N

def render_map(map, o, f, p):
  """
  Imprime por la terminal el mapa generado. Para representar los ceros y unos
  Se utilizan caracteres espeficicos para representar puntos solidos o vacíos
  del mapa generado (por ejemplo: aire o rocas).
  Inputs:
  map -- matriz de ceros y unos
  Return -- None
  """
  # Extraemos las dimensiones de la matriz
  fil = len(map)
  col = len(map[0])
  # Generamos una matriz de bloques vacíos
  M=[[f for _ in range(col)] for j in range(fil)]
  # Recorremos filas y columnas asignando un bloque solido cuando corresponda
  # Luego de recorrer una fila completa, se imprime una línea
  for i in range(fil):
    for j in range(col):
      if map[i][j]==1: M[i][j]=o
      if map[i][j]==p: M[i][j]=p
    print(''.join(M[i]))
