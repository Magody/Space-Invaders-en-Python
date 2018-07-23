import pygame

ancho = 1000
alto = 500

enJuego = False #0 intro,1 medio,2 enrage,3 final



class NaveEspacial(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)	

		self.ImagenNave=pygame.image.load('Imagenes/nave.jpg')
		self.rect = self.ImagenNave.get_rect()
		self.rect.centerx = 446
		self.rect.centery = 415
		self.velocidad=20
		self.listaDisparo = []

	def controlEncuadre(self):
		pass
		

	def movimientoIzquierda(self):
		self.rect.right-=self.velocidad
		

	def movimientoDerecha(self):
		self.rect.right+=self.velocidad
	

	def movimientoArriba(self):
		self.rect.top-=self.velocidad


	def movimientoAbajo(self):
		self.rect.top+=self.velocidad
		

	def dibujar(self,superficie):
		superficie.blit(pygame.image.load('Imagenes/nave.jpg'),self.rect)


	def disparar(self,x,y):
		bala=Proyectil(x,y,"Imagenes/disparoa.jpg",1)
		self.listaDisparo.append(bala)
		Musica().disparoaSonido()

class Proyectil(pygame.sprite.Sprite):
	def __init__(self,x,y,imagen,personaje):
		pygame.sprite.Sprite.__init__(self)

		self.imagenProyectil=pygame.image.load(imagen)
		self.rect = self.imagenProyectil.get_rect()
		self.rect.top = y
		self.rect.right = x

		self.velocidadDisparo = 5
		self.disparoPersonaje = personaje


	def trayectoria(self):
		if self.disparoPersonaje == 1:
			self.rect.top = self.rect.top - self.velocidadDisparo
		elif self.disparoPersonaje == 2:
			self.rect.top = self.rect.top + self.velocidadDisparo

	def dibujar(self,superficie):
		superficie.blit(self.imagenProyectil, self.rect)

class Musica:
	
	def musicaIntro(self):
		pygame.mixer.music.load("Musica/Undertale.mp3")	
		pygame.mixer.music.play(10)

	def musicaFondo(self):
		musica = pygame.mixer.music.load("Musica/OneeyedMaestro.mp3")	
		pygame.mixer.music.play(10)

	def disparoaSonido(self):
		pium = pygame.mixer.Sound("Sonido/pium.wav")
		pium.play()



def game():
	pygame.init()
	ventana = pygame.display.set_mode((ancho,alto))
	pygame.display.set_caption("Juegazo alv")
	fondo=pygame.image.load("Imagenes/Fondo.jpg")



	imagenPony=pygame.image.load("Imagenes/pony.jpg")
	
	nave = pygame.image.load("Imagenes/nave.jpg")

	fuenteIntro= pygame.font.SysFont("Arial",30)
	textoIntro=fuenteIntro.render("Presione 'i' para empezar o reiniciar",0,(250,250,250))

	posx,posy = 360,100	
	velocidad = 20

	jugador = NaveEspacial()

	crash = False
	enJuego = False
	#reloj = pygame.time.Clock()


	if enJuego == False:
		Musica().musicaIntro()
	
	image = ventana.blit(imagenPony,(posx,posy))

	while not crash:
		
		ventana.blit(fondo,((0,0)))
		#reloj.tick(60)
		#tiempo = pygame.time.get_ticks()/1000
		

		for event in pygame.event.get():

			if event.type == pygame.QUIT:
				crash = True
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_i:
					
					enJuego = True
					Musica().musicaFondo()
				if enJuego == True:	
					if event.key == pygame.K_UP:
						#posy-=velocidad
						jugador.movimientoArriba()

					if event.key == pygame.K_DOWN:
						#posy+=velocidad
						jugador.movimientoAbajo()

					if event.key == pygame.K_RIGHT:
						#posx+=velocidad
						jugador.movimientoDerecha()

					if event.key == pygame.K_LEFT:
						#posx-=velocidad
						jugador.movimientoIzquierda()

					if event.key == pygame.K_a:
						x,y = jugador.rect.center
						jugador.disparar(x+6,y-33)
						
					
		
		
		
		if enJuego == False:
			ventana.blit(imagenPony,(posx,posy))
			ventana.blit(textoIntro,(300,300))
		elif enJuego == True:
			jugador.dibujar(ventana)


		if len(jugador.listaDisparo)>0:
			for bala in jugador.listaDisparo:
				bala.dibujar(ventana)
				bala.trayectoria()

				if bala.rect.top < -10:
					jugador.listaDisparo.remove(bala)



		pygame.display.update()


	pygame.quit()


game()

