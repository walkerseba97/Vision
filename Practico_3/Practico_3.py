# Práctico_3: Obtener las imágenes por segundo o fps usando las OpenCV? Usarlo para no tener que harcodear el delay del waitKey.
#             Obtener el tamño de la imagen

import cv2

filename = input("Ingresar nombre de video:")
cap = cv2.VideoCapture(filename)

fourcc = cv2.VideoWriter_fourcc(*'mp4v') #formato para codigo de cuatro caracteres

tam_img = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) #Recibo tamaño de la imagen
fps = cap.get(cv2.CAP_PROP_FPS) #Obtengo FPS de la imagen

print("Tamaño de imagen es:{} y los fps son:{}" .format(tam_img, int(fps)))

copia = cv2.VideoWriter('video2.mp4',fourcc,fps,tam_img) #nombre archivo de salida, codificacion del video, fps y size video 

while (cap.isOpened()):
    ret, frame = cap.read()
    if ret == True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        copia.write(gray)
        cv2.imshow('Video',gray)
        if((cv2.waitKey(int(fps)) & 0xFF) == ord('q')):
            break
    else:
        break

copia.release()
cap.release()
cv2.destroyAllWindows()