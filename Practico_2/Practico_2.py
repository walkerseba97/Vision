import cv2
import numpy as np

img = cv2.imread('hojas.jpg',0)
img_modificada = np.zeros_like(img)

filas = img.shape[0]
columnas = img.shape[1]

print("Cantidad de filas y columnas:{} {}".format(filas,columnas))

for f in range (filas):
	
	for c in range (columnas):
   		
		if img[f][c]>190:
			
			img_modificada[f][c] = 255


cv2.imshow("Imagen modificada",img_modificada)
cv2.waitKey(0)

cv2.destroyAllWindows()

