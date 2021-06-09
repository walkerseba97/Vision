#Práctico_4: Usando como base el programa anterior, crear un programa que
#            permita seleccionar un rectángulo de una imagen, luego:
#               * Con 'g': Guardamos a disco una nueva imagen y salimos
#               * Con 'r': Guardamos la imagen original y volvemos a realizar la seleccion
#               * Con 'q': Salimos
import cv2
import numpy as np

filename = "messi.jpg"
img = cv2.imread(filename)

drawing = False #true si el botón está presionado

p1x, p1y = -1, -1 #Punto de inicio
p2x, p2y = -1, -1 #Punto de fin

def recorte(event, x, y, flags, param):
    global p1x, p1y, p2x, p2y, drawing #variables globales
	
    if event == cv2.EVENT_LBUTTONDOWN: #pulso click izquierdo (coordenadas de inicio)
        drawing = True
        p1x, p1y = x, y
    elif event == cv2.EVENT_MOUSEMOVE: 
        if drawing is True:            
            p2x, p2y = x, y
    elif event == cv2.EVENT_LBUTTONUP: #suelto click izuierdo (coordenadas finales)
        drawing = False
        cv2.rectangle(img, (p1x, p1y), (p2x, p2y), (255, 255, 255) , 2)

cv2.namedWindow('img')
cv2.setMouseCallback('img',recorte)

print("\nDibuje un rectangulo sobre la imagen")
print("\nSeleccione sobre la imagen:")
print("\tq: Salir.")
print("\tg: Recorte (una vez dibujado el rectángulo).")
print("\tr: Limpiar imagen.")

while(1):

    cv2.imshow('img', img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord ('q'): #Salgo
        break

    elif k == ord ('g'): #Guardo
        if p1x > p2x: #Inviero si cordenadas estan al reves
            aux = p1x
            p1x = p2x
            p2x = aux
        if p1y > p2y:
            aux = p1y
            p1y = p2y
            p2y = aux

        img_recorte = img[p1y:p2y, p1x:p2x]
        cv2.imshow('imgen', img_recorte)
        cv2.waitKey(0)
        cv2.imwrite("messi_corte.jpg", img_recorte)

    elif k == ord('r'):  #Limpio imagen
        cv2.destroyAllWindows()
        img = cv2.imread(filename)
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',recorte)
        
cv2.destroyAllWindows()
