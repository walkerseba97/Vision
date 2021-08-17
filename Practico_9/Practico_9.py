#Práctico 9: Capturar una imagen de una fachada con perspectiva y hacer un programa que permita:
#               - encontrar la transformación perspectiva entre los 4 vértices del marco y un rectángulo
#               - con la misma relación de aspecto que la puerta real;
#               - aplicar dicha transformación a la imagen y mostrarla en una ventana;
#               - sobre esta ventana permitir que el usuario haga dos clicks y mostrar la distancia en metros entre dichos puntos;
#               - permitir que cuando se presione la tecla “r” se reinicie la medición;
#               - por último medir dos objetos en la imagen (ventana, casilla del gas, etc.) y comparar los resultados con la medida real.
#                


import cv2
import numpy as np
import math

puntos_rect = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]
puntos_med = [[-1,-1],[-1,-1]]

N=0
A=0

drawing = False

aux=0

def medicion(event, x, y, flags, param):
    global puntos_med, drawing, N

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        puntos_med[N] = x,y
        N=N+1

        if N==2:
            N=0
            drawing = False
            img_rect[:] = img_dibujada[:]


    elif event == cv2.EVENT_MOUSEMOVE:
        if(drawing == True):
            img_dibujada[:] = img_rect[:]
            medida = relacion(puntos_med[0][0],puntos_med[0][1],x,y)
            cv2.line(img_dibujada, (puntos_med[0][0],puntos_med[0][1]), (x,y), (0,0,0), 2)
            cv2.putText( img_dibujada , medida, (x+5, y+50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,0), 2)


def relacion(x1,y1,x2,y2):
	
	x = x2-x1 #puntos de mediciones
	y = y2-y1
	
	x_mt = (x*(1.99/1280))**2 #Pasaje de pixel a metro, sabiendo tamaño de imagen y tamaño en mts del lugar donde se realizo transformada de perspectiva
	y_mt = (y*(2.015/720))**2
	
	resultado = math.sqrt(x_mt + y_mt)
	resultado = round(resultado, 2)
	
	return str(resultado) + " mt"


filename = "Puerta_1.jpg"
img = cv2.imread(filename)


print("\nPara salir seleccione 'q' sobre la imagen.")
print("\nPara realizar transformada de perspectiva seleccione 'h' sobre la imagen.")

cv2.namedWindow('img')


while(1):

    cv2.imshow("img", img)
    k = cv2.waitKey(1) & 0xFF

    if k == ord('q'):
        aux=1
        break

    elif k == ord ('h'): #Transformada perspectiva

        (rows,columns) = (img.shape[0],img.shape[1])
            
        puntos_origen = np.float32([[0,0],[0,rows],[columns,rows],[columns,0]])

        puntos_rect[0] = 552, 9    #Puntos destinos ya definidos
        puntos_rect[1] = 560, 716
        puntos_rect[2] = 1183, 677
        puntos_rect[3] = 1263, 11

        puntos_destino = np.float32([[puntos_rect[0]], [puntos_rect[1]], [puntos_rect[2]], [puntos_rect[3]]])

        M = cv2.getPerspectiveTransform(puntos_destino, puntos_origen)

        img_rect = cv2.warpPerspective(img, M, (columns, rows))
        print(img_rect.shape)
        cv2.imwrite('img_rect.jpg', img_rect)
        cv2.namedWindow('img_rect')
        cv2.imshow('img_rect', img_rect)

        break

cv2.destroyAllWindows() 

if aux==0:

    print("\nPara salir seleccione 'q' sobre la imagen.")
    print("\nPara limpiar la imagen de las mediciones seleccione 'r' sobre la imagen.")
    print("\nPara guardar la imagen con las mediciones realizadas seleccione 'g' sobre la imagen.")

    img_rect_1 = img_rect.copy()
    img_dibujada = img_rect.copy()
    cv2.namedWindow('img')
    cv2.setMouseCallback('img',medicion)

    while(1):

        cv2.imshow("img", img_dibujada)
        k = cv2.waitKey(1) & 0xFF

        if k == ord('g'): #Presiono 'g' para guardar
            cv2.imwrite('img_dibujada.jpg', img_dibujada)
            break

        elif k == ord('r'): #Elimino medidas realizadas
            cv2.destroyAllWindows()
            img_dibujada = img_rect_1.copy()
            img_rect = img_rect_1.copy()
            cv2.imshow("img", img_dibujada)
            k = cv2.waitKey(1) & 0xFF
            cv2.setMouseCallback('img',medicion)

        elif k == ord('q'): #Presiono 'q' para salir
            break

    cv2.destroyAllWindows()