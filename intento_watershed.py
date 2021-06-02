import numpy as np
from typing import List, Tuple, Literal, Any
import queue
import matplotlib.pyplot as plt
import cv2

class Stack():
    def __init__(self) -> None:
        self.list = []

    def append(self, item: Any) -> None:
        self.list.append(item)

    def pop(self) -> Any:
        if(len(self.list) != 0):
            return self.list.pop()
        else:
            raise IndexError()

    def peek(self) -> Any:
        if(len(self.list) != 0):
            return self.list[-1]
        else:
            raise IndexError()

    def __len__(self) -> int:
        return len(self.list)

def ObtenerVecindad(coordenadas: List, resolucion: Tuple, tipo_vecindad: Literal[4,8]) -> List[List[int]]:
    vecinos = []
    i = coordenadas[0]
    j = coordenadas[1]

    def ObtenerVecindadCuatro(resolucion: Tuple) -> None:
        for fila in range(-1,2):
            fila_vecino = i + fila
            
            if((fila_vecino >= 0) and (fila_vecino < resolucion[0])):
                vecinos.append([fila_vecino, j])

        for columna in range(-1,2):
            columna_vecino = j + columna

            if((columna_vecino >= 0) and (columna_vecino < resolucion[1])):
                vecinos.append([i, columna_vecino])
    
    def ObtenerVecindadOcho(resolucion: Tuple) -> None:
        for fila in range(-1,2):
            fila_vecino = i + fila
            for columna in range(-1,2):
                columna_vecino = j + columna
                
                if(((fila_vecino >= 0) and (fila_vecino < resolucion[0])) and ((columna_vecino >= 0) and (columna_vecino < resolucion[1]))):
                    vecinos.append([fila_vecino, columna_vecino])

    switch_vecinos = {
        4: lambda : ObtenerVecindadCuatro(resolucion),
        8: lambda : ObtenerVecindadOcho(resolucion)
    }

    switch_vecinos[tipo_vecindad]()
    vecinos.remove([i,j])

    return vecinos

s = Stack()

img = np.array([[0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,4,4,4,4,0,0], [0,0,2,0,0,0,0,0,4,4,4,4,0,0], [0,0,2,0,0,0,0,0,4,4,4,4,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,5,5,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0]])

# img = cv2.imread(r"D:\raulg\Pictures\crunchyroll.png", cv2.IMREAD_GRAYSCALE)
# _, img = cv2.threshold(img, 50, 255, cv2.THRESH_BINARY)

# plt.figure()
# plt.imshow(img)
# plt.show()

salida = np.copy(img)
img_original = np.copy(img)

for fila in range(len(img)):
    for columna in range(len(img[fila])):
        if img[fila][columna] != 0:
            bandera = 255

            vecinos = ObtenerVecindad([fila, columna], img.shape, 8)
            
            for vecino in vecinos:
                bandera = bandera & img[vecino[0],vecino[1]]

            if(bandera == 0):
                s.append([fila, columna])

while (len(s) > 0):
    p = s.pop()
    vecinos = ObtenerVecindad(p, img.shape, 8)

    for vecino in vecinos:
        if(img[vecino[0], vecino[1]] == 0):
            vecinos_recargados = ObtenerVecindad(vecino, img.shape, 8)

            for vecino_recargado in vecinos_recargados:
                if (img[vecino_recargado[0], vecino_recargado[1]] != 0 and vecino_recargado != p):
                    salida[vecino[0], vecino[1]] = 255
                img[vecino[0], vecino[1]] = img[p[0], p[1]]

                s.append(vecino)

# print(salida)
# print(img)

plt.figure()
plt.imshow(salida)
plt.show()


