
import pygame
import random

#variables globales
ancho=900
alto=480
listaEnemigo = []


class naveEspacial(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.ImagenNave=pygame.image.load('Imagenes/nave.jpg')
        self.rect=self.ImagenNave.get_rect()
        self.rect.centerx = (ancho / 2)  
        self.rect.centery = (alto - 30) 

        self.listaDisparo = []

        self.Vida = True     #estado vivo

        self.velocidad = 20 #velocidad

        self.sonidoDisparo=pygame.mixer.Sound("Sonido/pium.wav")

    def movimiento(self):
        if self.Vida == True:
            if self.rect.left <= 0: #pygame.image.load('nave.jpg').get_rect().left
                self.rect.left = 0
            elif self.rect.right > 870: #pygame.image.load('nave.jpg').get_rect().right
                self.rect.right = 840

    def movimientoDerecha(self):
        self.rect.right+=self.velocidad
        self.movimiento()

    def movimientoIzquierda(self):
        self.rect.right-=self.velocidad
        self.movimiento()

    def disparar(self,x,y):
        miProyectil=Proyectil(x,y,"Imagenes/disparoa.jpg",True)
        self.listaDisparo.append(miProyectil)
        self.sonidoDisparo.play()
    


    def dibujar(self, superficie):
        superficie.blit(self.ImagenNave, self.rect) 
                #(pygame.image.load('nave.jpg'),pygame.image.load('nave.jpg').get_rect())

class Proyectil(pygame.sprite.Sprite):
    def __init__(self,posx,posy,ruta,personaje):
        pygame.sprite.Sprite.__init__(self)

        self.imageProyectil = pygame.image.load(ruta)
        self.rect = self.imageProyectil.get_rect()
        self.velocidadDisparo = 5

        self.rect.top = posy
        self.rect.left = posx

        self.disparoPersonaje = personaje

    def trayectoria(self):
        if self.disparoPersonaje == True:
            self.rect.top = self.rect.top - self.velocidadDisparo
        else:
            self.rect.top = self.rect.top + self.velocidadDisparo

    def dibujar(self,superficie):
        superficie.blit(self.imageProyectil, self.rect)

class Invasor(pygame.sprite.Sprite):
    def __init__(self,posx,posy,imagen1,Imagen2):
        pygame.sprite.Sprite.__init__(self)

        self.imagenA = pygame.image.load(imagen1)
        self.imagenB = pygame.image.load(Imagen2)
        
        self.listaImagenes=[self.imagenA,self.imagenB]
        self.posImagen=0

        self.imagenInvasor = self.listaImagenes[self.posImagen]
        self.rect = self.imagenInvasor.get_rect() 

        self.listaDisparo = []
        self.velocidad=5
        self.rect.top = posy
        self.rect.left = posx

        self.rangoDisparo = 5    
        self.tiempoCambio = 1

        self.derecha=True
        self.contador=0
        self.maxdescenso=self.rect.top+40




    def dibujar(self,superficie):
        self.imagenInvasor = self.listaImagenes[self.posImagen]
        superficie.blit(self.imagenInvasor, self.rect)

    def comportamiento(self,tiempo):
        self.__movimiento()
        self.__ataque()
        if self.tiempoCambio == tiempo:
            self.posImagen += 1
            self.tiempoCambio += 1

            if self.posImagen > len(self.listaImagenes)-1:
                self.posImagen=0

    def __ataque(self):
        if (random.randint(0,100) < self.rangoDisparo):
            self.__disparo()

    def __disparo(self):
        x,y = self.rect.center
        miProyectil=Proyectil(x,y,"Imagenes/disparob.jpg",False)
        self.listaDisparo.append(miProyectil)

    def __movimiento(self):
        if self.contador < 2:
            self.__movimientoLateral()
        else:
            self.__descenso()

    def __descenso(self):
        if self.maxdescenso==self.rect.top:
            self.contador=0
            self.maxdescenso=self.rect.top+40
        else:
            self.rect.top+=2

    def __movimientoLateral(self):
        if self.derecha==True:
            self.rect.left+=self.velocidad
            if self.rect.left > 837:
                self.derecha=False
                self.contador+=1

        else:
            self.rect.left-=self.velocidad
            if self.rect.left < 0:
                self.derecha = True

def cargarEnemigos():
    enemigo = Invasor(100,100,"Imagenes/MarcianoA.jpg","Imagenes/MarcianoB.jpg")
    listaEnemigo.append(enemigo)

def SpaceInvader():
    pygame.init()
    ventana = pygame.display.set_mode((ancho,alto))
    pygame.display.set_caption("Space Invader")
    ImagenFondo = pygame.image.load("Imagenes/fondo.jpg")
    

    enJuego = True
    if enJuego == True:
        pygame.mixer.music.load("Musica/OneeyedMaestro.mp3")
        pygame.mixer.music.play(10)

    jugador = naveEspacial()
    cargarEnemigos()

    


    crashed = False
    reloj = pygame.time.Clock()
    
    while not crashed:
        
        reloj.tick(60)
        tiempo = pygame.time.get_ticks()/1000

        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                crashed = True

            elif enJuego == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        jugador.movimientoIzquierda()

                    elif event.key == pygame.K_RIGHT:
                        jugador.movimientoDerecha()

                    elif event.key == pygame.K_a:
                        x,y = jugador.rect.center
                        jugador.disparar(x-6,y-55)


        ventana.blit(ImagenFondo,(0,0))
        
        jugador.dibujar(ventana)
        


        if len(jugador.listaDisparo)>0:
            for e in jugador.listaDisparo:
                e.dibujar(ventana)
                e.trayectoria()

                if e.rect.top<-10:
                    jugador.listaDisparo.remove(e)
                else:
                    for enemigo in listaEnemigo:
                        if e.rect.colliderect(enemigo.rect):
                            listaEnemigo.remove(enemigo)
                            jugador.listaDisparo.remove(e)



        if len(listaEnemigo)>0:
            for enemigo in listaEnemigo:
                enemigo.comportamiento(tiempo)
                enemigo.dibujar(ventana)

                if enemigo.rect.colliderect(jugador.rect):
                    pass

                if len(enemigo.listaDisparo)>0:
                    for e in enemigo.listaDisparo:
                        e.dibujar(ventana)
                        e.trayectoria()

                        if e.rect.colliderect(jugador.rect):
                            pass

                        if e.rect.top>900:
                            enemigo.listaDisparo.remove(e)
                        else:
                            for disparo in jugador.listaDisparo:
                                if e.rect.colliderect(disparo.rect):
                                    jugador.listaDisparo.remove(disparo)
                                    enemigo.listaDisparo.remove(e)





        pygame.display.update()

    pygame.quit()


SpaceInvader()

