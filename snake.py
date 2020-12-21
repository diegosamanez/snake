import turtle
import time
import random
import pygame
import sys
import os
pygame.init()

#Recursos para sistema operativo
def resource_path(relative_path):
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

#Sonidos
url_musica_fondo = resource_path("media/Child_s-Nightmare.wav")
url_colision = resource_path("media/colision.wav")
url_comer = resource_path("media/comer.wav")

musica_fondo = pygame.mixer.Sound(url_musica_fondo)
colision = pygame.mixer.Sound(url_colision)
comer = pygame.mixer.Sound(url_comer)

musica_fondo.play(-1)
musica_fondo.set_volume(0.3)



posponer = 0.1

#Marcador
score = 0
#Base de datos del mejor marcador
with open("db/high_score_snake.csv","r") as dto_high_score:    
    high_score = int(str(dto_high_score.read()))
    dto_high_score.close()

#características del canvas 
wn = turtle.Screen()
wn.title("juego de Snake")
wn.bgcolor("black")
wn.setup(width = 600, height = 600)
wn.tracer(0)

#cabeza serpiente
cabeza = turtle.Turtle()
cabeza.speed(0)
	#para dibujar un cuadrado "square"
cabeza.shape("square")
cabeza.color("white")
cabeza.penup()
cabeza.goto(0,0)
cabeza.direction = "stop"

#comida
comida = turtle.Turtle()
comida.speed(0)
	#para dibujar un cuadrado "square"
comida.shape("circle")
comida.color("red")
comida.penup()
comida.goto(0,100)

# Cuerpo serpiente / lista
segmentos = []

#Texto marcador
texto = turtle.Turtle()
texto.speed()
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0,260)
texto.write(" Score :0    High Score:{}".format(high_score), align = "center", font = ("Courier", 24, "normal"))


#funciones
def arriba():
	cabeza.direction = "up"
def abajo():
	cabeza.direction = "down"
def izquierda():
	cabeza.direction = "left"
def derecha():
	cabeza.direction = "right"


def mov():
	if cabeza.direction == "up":
		y = cabeza.ycor()
		cabeza.sety(y + 20)

	if cabeza.direction == "down":
		y = cabeza.ycor()
		cabeza.sety(y - 20)

	if cabeza.direction == "left":
		x = cabeza.xcor()
		cabeza.setx(x - 20)

	if cabeza.direction == "right":
		x = cabeza.xcor()
		cabeza.setx(x + 20)

#Teclado
wn.listen()
wn.onkeypress(arriba, "Up")
wn.onkeypress(abajo, "Down")
wn.onkeypress(izquierda, "Left")
wn.onkeypress(derecha, "Right")

#bucle principal
while True:
	wn.update()

	#Colisiones bordes
	if cabeza.xcor() > 280 or cabeza.xcor() < -280 or cabeza.ycor() > 280 or cabeza.ycor() < -280:
		colision.play()
		musica_fondo.stop()
		time.sleep(1)
		cabeza.goto(0,0)
		cabeza.direction = "stop"
		musica_fondo.play(-1)


		#Esconder los segmentos.
		for segmento in segmentos:
			segmento.hideturtle()
		segmentos.clear()

		#Reset marcador
		score = 0
		texto.clear()
		texto.write(" Score :{}    High Score:{}".format(score, high_score),
					align = "center", font = ("Courier", 24, "normal"))

	#Colisiones comida
	if cabeza.distance(comida) < 20:
		comer.play()
		x = random.randint(-280,280)
		y = random.randint(-280,280)
		comida.goto(x,y)

		nuevo_segmento = turtle.Turtle()
		nuevo_segmento.speed(0)
		nuevo_segmento.shape("square")
		nuevo_segmento.color("grey")
		nuevo_segmento.penup()
		segmentos.append(nuevo_segmento)

		#Aumentar marcador
		score += 10 

		if score > high_score:
			high_score = score
			#Guardar mejor marcador en base de datos
			with open("db/high_score_snake.csv","a") as dto_high_score:
				dto_high_score.truncate(0)
				dto_high_score.close()
			with open("db/high_score_snake.csv","a") as dto_high_score:
				dto_high_score.write(str(high_score))
				dto_high_score.close()


		texto.clear()
		texto.write(" Score :{}    High Score:{}".format(score, high_score),
					align = "center", font = ("Courier", 24, "normal"))

	#Mover el cuerpo de la serpiente
	totalSeg = len(segmentos)
	for index in range(totalSeg - 1, 0, -1):
		x = segmentos[index-1].xcor()
		y = segmentos[index-1].ycor()
		segmentos[index].goto(x,y)

	if totalSeg > 0:
		x = cabeza.xcor()
		y = cabeza.ycor()
		segmentos[0].goto(x,y)

	mov()

	#Colisiones cuerpo
	for segmento in segmentos:
		if segmento.distance(cabeza) < 20 :
			colision.play()
			musica_fondo.stop()
			time.sleep(1)
			cabeza.goto(0,0)
			cabeza.direction = "stop"
			musica_fondo.play(-1)

			#Esconder los segmentos.
			for segmento in segmentos:
				segmento.hideturtle()

			#limpiar los elementos de una lista
			segmentos.clear()

			#Reset marcador
			score = 0
			texto.clear()
			texto.write(" Score :{}    High Score:{}".format(score, high_score),
						align = "center", font = ("Courier", 24, "normal"))

	time.sleep(posponer)
