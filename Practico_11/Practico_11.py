#Práctico 11: Alineación de imagenes usando SIFT
# 
# Considerando los pasos detallados a continuación, realizar una alineación entre
# imágenes:
#   
#   1- Capturar dos imágenes con diferentes vistas del mismo objeto
#   2- Computar puntos de interés y descriptores en ambas imágenes
#   3- Establecer matches entre ambos conjuntos de descriptores
#   4- Eliminar matches usando criterio de Lowe
#   5- Computar una homografía entre un conjuntos de puntos y otro
#   6- Aplicar la homografía sobre una de las imagenes y guardarla en otra (mezclarla con
#   un alpha de 50%)
  
import numpy as np
import cv2

MIN_MATCH_COUNT = 10

img1 = cv2.imread('img1.jpeg') # Leemos la imagen 1
img2 = cv2.imread('img2.jpeg') # Leemos la imagen 2

dscr = cv2.xfeatures2d.SIFT_create(100) 	# Inicializamos el detector y el descriptor

kp1, des1 = dscr.detectAndCompute(img1, None)	#Encontramos los puntos clave y los descriptores con SIFT en imagen 1
kp2, des2 = dscr.detectAndCompute(img2, None)	#Encontramos los puntos clave y los descriptores con SIFT en imagen 2

matcher = cv2.BFMatcher(cv2.NORM_L2)
matches = matcher.knnMatch(des1, des2, k=2)

# Guardamos los buenos matches usando el test de razón de Lowe
good = []
for m,n in matches:
	if m.distance < 0.7*n.distance:
		good.append(m)

if(len(good)>MIN_MATCH_COUNT):
	scr_pts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2) 
	dst_pts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
	
	H,mask = cv2.findHomography(dst_pts, scr_pts, cv2.RANSAC, 5.0) 	#Computamos la homografía con RANSAC

wimg2 = cv2.warpPerspective(img2, H, img2.shape[:2][::-1])			#Aplicamos la transformación perspectiva H a imagen 2
alpha = 0.5
blend = np.array( wimg2*alpha + img1*(1-alpha), dtype=np.uint8)																	

# Puntos plots
cv2.drawKeypoints(img1,kp1,img1,(0, 0, 0))
cv2.drawKeypoints(img1,kp2,img2,(255, 0, 0))
img_conc = np.concatenate((img1, img2), axis=1)	
cv2.imshow('Puntos de img', img_conc)
cv2.imwrite('Puntos.jpeg',img_conc)
cv2.waitKey(0)

# Lowe plot
img_match = cv2.drawMatches(img1, kp1, img2, kp2, good, None)	
cv2.imshow('Lowe', img_match)
cv2.imwrite('Lowe.jpeg',img_match)
cv2.waitKey(0)

#Mezclo imagenes con alpha 
cv2.imshow('Imagenes mezcladas', blend)
cv2.imwrite('ImagenMezcla.jpeg',blend)
cv2.waitKey(0)
cv2.destroyAllWindows