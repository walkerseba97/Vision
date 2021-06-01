#Práctico 5: A- Crear una función que aplique una transformación euclidiana, recibiendo los siguientes parámetros:
#                   1- Angle: Ángulo
#                   2- tx: translación en x
#                   3- ty: translación en y
#            B- Usando como base el programa anterior, escribir un programa que permita seleccionar una porción 
#            rectangular de una imagen y con la letra "e" aplique una transformación euclidiana a la porción de imagen
#            seleccionada y la guarde como una nueva imagen.

import cv2
import numpy as np
import math

p1x, p1y = -1, -1 #Punto de inicio
p2x, p2y = -1, -1 #Punto de fin

drawing = False #true si el botón está presionado

filename = "messi.jpg"
img = cv2.imread(filename)

def trans_euclidiana(img, rows, columns, tx, ty, angle):
 
    (rows,columns) = (img.shape[0],img.shape[1])

    rad_angle = math.radians(angle)

    M = np.float32([[np.cos(rad_angle),np.sin(rad_angle),tx],
                    [-np.sin(rad_angle),np.cos(rad_angle),ty]])
    
    shifted = cv2.warpAffine(img,M,(columns,rows))
  
    return shifted


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

flag = 0 #Para saber cuando se recorta

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
        flag = 1 #Si esta en uno quiere decir que se recorto

    elif k == ord('r'):  #Limpio imagen
        cv2.destroyAllWindows()
        img = cv2.imread(filename)
        cv2.namedWindow('img')
        cv2.setMouseCallback('img',recorte)

    elif k == ord ('e'): #Transformación eucliasiana

        if(flag == 1):

            (rows,columns) = (img_recorte.shape[0],img_recorte.shape[1])
            
            angle = int(input("Ingrese ángulo de rotación:"))
            tx = int(input("Ingrese traslación en el eje x: "))
            ty = int(input("Ingrese traslación en el eje y:"))

            messi_euclidiano = trans_euclidiana(img_recorte,rows,columns,tx,ty,angle)
            
            cv2.imwrite('Messi Euclidiano.jpg',messi_euclidiano)
            cv2.imshow('Messi_corte',img_recorte)
            cv2.imshow('Messi Euclidiano', messi_euclidiano)

        else:
            print("Primero se debe recortar la imagen.")
        
cv2.destroyAllWindows()
