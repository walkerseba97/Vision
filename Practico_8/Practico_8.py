#Práctico 8: Teniendo en cuenta que:
#                - Una homografía se representa con una matriz de 3x3 (pero tiene solo 8 grados de libertad).
#                - Y puede ser recuperada con 4 puntos no colineales. 
#            A- Crear una función que conmute la homografía entre los 4 pares de puntos correspondientes.
#            B- Usando como base el programa anterior, escriba un programa que con la letra "h" permita seleccionar con el mouse
#               4 puntos no colineales en una imagen y transforme (rectifique) la selección en una nueva imagen rectangular.
#   Ayuda:
#           - cv2.cv2.getPerspectiveTransform
#           - cv2.warpPerspective

import cv2
import numpy as np
import math

p1x, p1y = -1, -1 #Punto de inicio
p2x, p2y = -1, -1 #Punto de fin

puntos_afin = [[-1, -1], [-1, -1], [-1, -1]]
puntos_rect = [[-1, -1], [-1, -1], [-1, -1], [-1, -1]]

drawing = False #true si el botón está presionado

filename = "messi.jpg"
filename_2 = "crisitano.png"
filename_3 = "ajedrez.jpg"

N=0
A=0

def puntos_trans_rect(event, x, y, flags, param):
    global A
    if event == cv2.EVENT_LBUTTONUP:
        if A == 0:
            puntos_rect[0] = x,y
            cv2.circle(img_2,(x,y),4,(255,0,0),-1)
            A = A+1
        elif A == 1:
            puntos_rect[1] = x,y
            cv2.circle(img_2,(x,y),4,(0,255,0),-1)
            A = A+1
        elif A == 2:
            puntos_rect[2] = x,y
            cv2.circle(img_2,(x,y),4,(0,0,255),-1)
            A = A+1
        elif A == 3:
            puntos_rect[3] = x,y
            cv2.circle(img_2,(x,y),4,(255,255,255),-1)
            A = A+1
        else:
            print("Ya coloco los 4 puntos.")


def mascara(img_afin,img_1_aux):
    
    mascara = img_afin.copy()
    mascara[mascara != 0] = 255
    mascara = cv2.bitwise_not(mascara)
    mascara = cv2.bitwise_and(mascara,img_1_aux)

    return mascara

def trans_afin(img_cristiano):

    print("Los puntos seleccionados:{}".format(puntos_afin))
    
    (rows,columns) = (img_cristiano.shape[0],img_cristiano.shape[1])

    puntos_origen = np.float32([[0,0],[0,rows-1],[columns-1,rows-1]]) 
    puntos_destino = np.float32([puntos_afin[0],puntos_afin[1],puntos_afin[2]]) 
    
    M = cv2.getAffineTransform(puntos_origen,puntos_destino)
    
    img_transformada = cv2.warpAffine(img_cristiano,M,(columns,rows))
    
    return img_transformada

def puntos_trans_afin(event, x, y, flags, param):
    global N
    if event == cv2.EVENT_LBUTTONUP:
        if N == 0:
            puntos_afin[0] = x,y
            cv2.circle(img_1,(x,y),4,(255,0,0),-1)
            N = N+1
        elif N == 1:
            puntos_afin[1] = x,y
            cv2.circle(img_1,(x,y),4,(0,255,0),-1)
            N = N+1
        elif N == 2:
            puntos_afin[2] = x,y
            cv2.circle(img_1,(x,y),4,(0,0,255),-1)
            N = N+1
        else:
            print("Ya coloco los 3 puntos.")


def trans_euclidiana_escalada(img, rows, columns, tx, ty, angle, s):
 
    (rows,columns) = (img.shape[0],img.shape[1])

    rad_angle = math.radians(angle)

    M = np.float32([[s*np.cos(rad_angle),s*np.sin(rad_angle),tx],
                    [-s*np.sin(rad_angle),s*np.cos(rad_angle),ty]])
    
    shifted_s = cv2.warpAffine(img,M,(columns,rows))
  
    return shifted_s

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

print("Seleccione:\n")
print("\ta-Realizar recorte, transfromada euclediana y transformada euclediana escalada.")
print("\tb-Realizar transformación afin y mascara.")
print("\tc-Rectificación de imagen.")

sel = input("Elección:")

if sel == 'a':
    
    print("\nDibuje un rectangulo sobre la imagen")
    print("\nSeleccione sobre la imagen:")
    print("\tq: Salir.")
    print("\tg: Recorte (una vez dibujado el rectángulo).")
    print("\tr: Limpiar imagen.")
    print("\te: Transformación euclediana (una vez hecho el recorte).")
    print("\ts: Transformación euclediana y escalada (una vez hecho el recorte).\n")
    
    img = cv2.imread(filename)
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
                tx = int(input("Ingrese traslación en el eje x:"))
                ty = int(input("Ingrese traslación en el eje y:"))

                messi_euclidiano = trans_euclidiana(img_recorte,rows,columns,tx,ty,angle)
                
                cv2.imwrite('Messi Euclidiano.jpg',messi_euclidiano)
                cv2.imshow('Messi_corte',img_recorte)
                cv2.imshow('Messi Euclidiano', messi_euclidiano)

            else:
                print("Primero se debe recortar la imagen.")

        elif k == ord ('s'): #Transformación eucliasiana escalada

            if(flag == 1):

                (rows,columns) = (img_recorte.shape[0],img_recorte.shape[1])
                
                angle = int(input("Ingrese ángulo de rotación:"))
                tx = int(input("Ingrese traslación en el eje x:"))
                ty = int(input("Ingrese traslación en el eje y:"))
                s= int(input("Ingrese la escala:"))

                messi_euclidiano_escalado = trans_euclidiana_escalada(img_recorte,rows,columns,tx,ty,angle,s)
                
                cv2.imwrite('Messi Euclidiano y escalado.jpg',messi_euclidiano_escalado)
                cv2.imshow('Messi_corte',img_recorte)
                cv2.imshow('Messi Euclidiano y escalado', messi_euclidiano_escalado)

            else:
                print("Primero se debe recortar la imagen.")

    cv2.destroyAllWindows()

if sel == 'b':

    img_1 = cv2.imread(filename)
    cv2.namedWindow('img_1')
    cv2.setMouseCallback('img_1',puntos_trans_afin)

    img_1_aux = img_1.copy() #Para hacer la mascara sin que salgan los puntos

    img_cristiano = cv2.imread(filename_2,1)
    (rows,columns) = (img_1.shape[0],img_1.shape[1])
    img_cristiano = cv2.resize(img_cristiano,(columns,rows))

    print("\n\nSeleccione 3 puntos en la imagen y presione a sobre la imagen 'a'.")
    print("\nPara salir seleccione 'q' sobre la imagen.")

    while(1):
        
        cv2.imshow('img_1', img_1)
        k = cv2.waitKey(1) & 0xFF

        if k == ord ('a'):
            img_afin = trans_afin(img_cristiano)
            img_mascara = mascara(img_afin,img_1_aux)
            img_final = cv2.bitwise_or(img_mascara, img_afin)

            cv2.imwrite('Messi_Cristiano.jpg', img_final)
            cv2.namedWindow('Messi_Cristiano')
            cv2.imshow('Messi_Cristiano', img_final) 

        if k == ord ('q'): #Salgo
            break

    cv2.destroyAllWindows()

if sel == 'c':

    print("\n\nSeleccione 4 puntos en la imagen y presione a sobre la imagen 'h'.")
    print("\nPara salir seleccione q sobre la imagen.")
    img_2 = cv2.imread(filename_3)
    cv2.namedWindow('img_2')
    cv2.setMouseCallback('img_2',puntos_trans_rect)   

    while(1):
        
        cv2.imshow('img_2', img_2)
        k = cv2.waitKey(1) & 0xFF

        if k == ord ('h'): 

            (rows,columns) = (img_2.shape[0],img_2.shape[1])

            puntos_origen = np.float32([[0,0],[0,rows-1],[columns-1,rows-1],[columns-1,0]])
            puntos_destino = np.float32([puntos_rect[0],puntos_rect[1],puntos_rect[2],puntos_rect[3]]) 
            
            f_max = puntos_rect[0][0]

            for i in range(4):
                if(f_max < puntos_rect[i][0]):
                    f_max = puntos_rect[i][0]

            f_min = puntos_rect[0][0]

            for i in range(4):
                if(f_min > puntos_rect[i][0]):
                    f_min = puntos_rect[i][0]

            c_max = puntos_rect[0][0]

            for i in range(4):
                if(c_max < puntos_rect[i][1]):
                    c_max = puntos_rect[i][1]

            c_min = puntos_rect[0][0]

            for i in range(4):
                if(c_min > puntos_rect[i][1]):
                    c_min = puntos_rect[i][1]

            M = cv2.getPerspectiveTransform(puntos_destino,puntos_origen)
            
            img_rect = cv2.warpPerspective(img_2,M,((f_max-f_min),(c_max-c_min)),flags=cv2.INTER_LINEAR)
            
            cv2.imwrite('img_rect.jpg', img_rect)
            cv2.namedWindow('img_rect')
            cv2.imshow('img_rect', img_rect) 
            

        if k == ord ('q'): #Salgo
            break

    cv2.destroyAllWindows() 
