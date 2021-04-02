#Crear funcion adivinar que permita adivinar un numero entre 0 y 100, el numero debe crearse
#dentro de la función y debe recibir como parametros la cantidad de intentos y si la cantidad 
#de intentos se supera programa debe cortar. Si se adivina antes con el numero de intenos

import random 

def adivinar (intentos):

	i = 0

	if(intentos < 0):
		print("Número de intento no válido")
		return

	numero = random.randint(0,100)

	while(i<intentos):

		print("Numero de intentos {} de {}" .format(i, intentos))

		aux = int(input("Ingrese número:")) 

		if(numero == aux):
			print("Número adivinado")
			break
		else:
			print("numero incorrecto, intente de nuevo")
			i = i+1
			continue

	else:  #Else se ejecuta cuando el bucle while corte sin un break 
		print("Cantidad de intentos terminada, el numero era {}" .format(numero))
	return
	

intentos = int(input("Seleccione la cantidad de intentos:"))

adivinar(intentos)
