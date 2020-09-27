
# Knight-Chess
Knight-Chess es un desafío en el que nuestro equipo desarrollo un programa o controlador que juegue aquella variante del ajedrez en el cual todas las piezas se remplazan por caballos. El proposito del Controlador sera que a partir de un estado dado, el deberá ser capaz de decidir el movimiento a realizar.

## Como ejecutar 
Para ejecutar el controlador, solo se debe abrir main.py. Este archivo se encargará de manejar el controlador, ubicado en OwervanzController.py
```
python main.py
```
## Evaluación (Reward)
El estado se evaluará según la [siguiente mapa](https://www.chessprogramming.org/Simplified_Evaluation_Function#Knights), sacado de la wikipedia de programación de ajedrez.
Dónde cada posición corresponderá a un puntaje, para el jugador actual será positivo, y para el enemigo será negativo.

```
				-50,-40,-30,-30,-30,-30,-40,-50,
				-40,-20,  0,  0,  0,  0,-20,-40,
				-30,  0, 10, 15, 15, 10,  0,-30,
				-30,  5, 15, 20, 20, 15,  5,-30,
				-30,  0, 15, 20, 20, 15,  0,-30,
				-30,  5, 10, 15, 15, 10,  5,-30,
				-40,-20,  0,  5,  5,  0,-20,-40,
				-50,-40,-30,-30,-30,-30,-40,-50,
```
Además de esta evaluación, tenemos una que será la diferencia de las piezas, dónde será positiva si favorece al jugador, caso contrario negativa.

Si es una jugada final, dará como resultado un +1 en caso de ganar, -1 en caso de perder.

En resumen, la evaluación será:
```
Si juego aun no terminado:
	= Posicion + Diferencia
Si juego terminado:
	Si gane = 1
	sino = -1
```

## Presentacion del Desafio Knight-Chess
