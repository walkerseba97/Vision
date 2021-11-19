# Practico 10: Se propone realizar una aplicación simple en base al teórico presentado 
#              de ArUCo y a los videos que se listan a continuación:
#    - https://www.youtube.com/watch?v=nsu9tNIJ6F0
#    - https://youtu.be/VsIMl8O_F1w?t=55
#    - https://www.youtube.com/watch?v=qqDXwKDr0vE
#    - https://www.youtube.com/watch?v=RNwTGPvuhPw&t=8
#    - https://www.youtube.com/watch?v=xzG2jQfxLlY
#    - https://www.youtube.com/watch?v=jwu9SX3YPSk
#    - https://www.youtube.com/watch?v=FBl4Y55V2Z4
#
#              El trabajo puede ser, por ejemplo, referido a realidad virtual en 2D o 
#              en 3D, estimación de posición y orientación de objetos en movimiento, 
#              seguimiento de objetos, etc. También puede tomarse como base algún repositorio 
#              interesante, instalarlo, hacerlo funcionar y aplicarlo para un uso personal o 
#              particular. 


import cv2
import cv2.aruco as aruco
import numpy as np

def findMarkers(img, markerSize = 5, totalMarkers = 250):
	imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	key = getattr(aruco,f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
	arucoDict = aruco.Dictionary_get(key)
	arucoParam = aruco.DetectorParameters_create()
	bbox, ids, rejected = aruco.detectMarkers(imgGray, arucoDict, parameters=arucoParam)
	
	return [bbox, ids]

def processingImg(cornes, id, img, Enable, Marks):
	arucoInd = [-1,-1,-1,-1]
	
	for i in range(4):
		arucoInd[i] = int(id[i])

	aruco1 = arucoInd.index(1)
	aruco2 = arucoInd.index(2)
	aruco3 = arucoInd.index(0)
	aruco4 = arucoInd.index(3)

	topLeft = cornes [aruco1][0][0][0], cornes [aruco1][0][0][1] 
	topRight = cornes [aruco2][0][1][0], cornes [aruco2][0][1][1] #Esta en el medio
	bottomRight = cornes [aruco3][0][1][0], cornes [aruco3][0][0][1]
	bottomLeft = cornes [aruco4][0][0][0], cornes [aruco4][0][1][1] 

	topRightPicture = int(bottomRight[0]),int(topLeft[1]) # Obtengo punto cuadro arriba derecha

	def correction(): #Ajuste de correciones para obtener el tamano completo de cuadro
		offset = -0.5*(cornes[aruco1][0][0][1] - cornes[aruco4][0][1][1])
		bottomLeft = cornes[aruco4][0][0][0], cornes[aruco4][0][1][1] + offset
		bottomRight = cornes[aruco3][0][1][0], cornes[aruco3][0][0][1] + offset
		return bottomLeft,bottomRight

	bottomLeft,bottomRight = correction()

	centerLeft = cornes [aruco2][0][0][0], cornes [aruco2][0][0][1] 
	centerRight = cornes [aruco2][0][1][0], cornes [aruco2][0][1][1]

	lenght = int(centerRight[0])-int(centerLeft[0]) #Obtengo distancia con aruco central

	if lenght<50:
		img_color = cv2.imread("negro.jpg")
	elif lenght<60:
		img_color = cv2.imread("verde.jpg")
	elif lenght<70:
		img_color = cv2.imread("amarillo.jpg")
	else:
		img_color = cv2.imread("rojo.png")

	height, width, ch = img_color.shape #altura y ancho

	p1 = np.array([topLeft,topRightPicture,bottomRight,bottomLeft])
	p2 = np.float32([[0,0],[width,0],[width,height],[0,height]])

	if Enable == False:
		if Marks == True:
			cv2.circle(img,(int(topLeft[0]),int(topLeft[1])),8,(255,0,0),-1)
			cv2.circle(img,(int(topRight[0]),int(topRight[1])),8,(0,255,0),-1)
			cv2.circle(img,(int(bottomRight[0]),int(bottomRight[1])),8,(0,0,255),-1)
			cv2.circle(img,(int(bottomLeft[0]),int(bottomLeft[1])),8,(255,255,255),-1)

			cv2.circle(img,(int(bottomRight[0]),int(topLeft[1])),8,(255,255,0),-1)

			cv2.circle(img,(int(centerLeft[0]),int(centerLeft[1])),8,(0,255,255),-1)
			cv2.circle(img,(int(centerRight[0]),int(centerRight[1])),8,(255,0,255),-1)
			return img
		else:
			return img

	conv,aux = cv2.findHomography(p2,p1)
	imgOut = cv2.warpPerspective(img_color, conv, (img.shape[1], img.shape[0]))
	
	cv2.fillConvexPoly(img, p1.astype(int),(0,0,0))
	imgOut = img + imgOut
	
	return imgOut

print("Muestra de color de acuerdo a distancia de video con respecto a cuadro:\n")
print("\tImagen negro muy lejos")
print("\tImagen verde lejos")
print("\tImagen amarilla cerca")
print("\tImagen roja muy cerca")
print("\n\nIngrese C para habilitar o desabilitar los colores")
print("\n\nSi colores estan desabilitados ingrese S para ver la deteccion de marcadores")
print("\nIngrese Q para salir del programa")

cap = cv2.VideoCapture("cuadro.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
Enable = True
Marks = False

while True:
	
	success, img = cap.read()
	arucoFound = findMarkers(img)

	if len(arucoFound[0]) == 4:
	    img = processingImg(arucoFound[0], arucoFound[1], img, Enable, Marks)		

	cv2.imshow("Image", img)

	key = cv2.waitKey(int(fps))
	
	if key == ord('c'):    # C para desabilitar
		if Enable == True:
			Enable = False
		else:
			Enable = True

	if key == ord('s'):    # C para desabilitar
		if Enable == False:
			if Marks == True:
				Marks = False
			else:
				Marks = True

	if key == ord('q'):    # Q para salir
		break

cap.release()	
cv2.destroyAllWindows()	
		

