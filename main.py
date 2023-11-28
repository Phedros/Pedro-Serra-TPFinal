import pygame as pg
import sys
from constantes import *
from player import Player
from plataforma import Platform
from enemigo import *

pygame.init()

# Superficie principal
screen = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
clock = pygame.time.Clock()

# control tiempo
tiempo = 0
tiempo_mil = 0

# define fonts
font = pygame.font.SysFont("ITC Machine",40)

def draw_text(text,font,text_col,x,y):
    img = font.render(text,True,text_col)
    screen.blit(img,(x,y))


# Bullet
bullet_group = pygame.sprite.Group()

# Musica
background_music = pg.mixer.Sound("sound\Saint Seiya Opening Version 8 BITS.mp3")
background_music.play()

imagen_fondo = pygame.image.load("images/locations/forest/Santuario_Abel.png")
imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA)) # Escalamos la imagen de fondo a la dimension de la ventana

player_1 = Player(
    x=0,
    y=530,
    speed_walk=5,
    speed_run=10,
    gravity=8,
    jump_power=25,
    max_high_jump = 450,      
    animation_speed=12
    )

enemigo_1 = Enemy(
    x=200,
    y=530,
    speed_walk= 2,
    speed_run=8,
    gravity=8,
    jump_power=25,
    max_high_jump = 450,      
    animation_speed=12
)

tiempo = Auxiliar()



lista_plataformas = []
lista_plataformas.append(Platform(300,450,60,60))
lista_plataformas.append(Platform(360,450,60,60))
lista_plataformas.append(Platform(420,450,60,60))


while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if not player_1.is_hit:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player_1.jump_control(True,animation_speed=8)   
                # if event.key == pygame.K_LALT:
                #     player_1.is_running = True 
                #     player_1.walk_control(player_1.direccion,animation_speed=6,is_running=True)   

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    player_1.jump_control(False,animation_speed=8)
                # if event.key == pygame.K_LALT:
                #     player_1.is_running = False 


    keys = pygame.key.get_pressed()
    if not player_1.is_hit:
        if(keys[pygame.K_LCTRL]):
            player_1.punch(animation_speed=2)
            player_1.is_punching = True
        else:
            player_1.is_punching = False
            if(keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LALT]):
                player_1.walk_control(DIRECCION_L,animation_speed=6,is_running=False)
            
            elif(keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT] and keys[pygame.K_LALT]):
                player_1.walk_control(DIRECCION_L,animation_speed=6,is_running=True)

            elif(not keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and not keys[pygame.K_LALT]):
                player_1.walk_control(DIRECCION_R,animation_speed=6,is_running=False)

            elif(not keys[pygame.K_LEFT] and keys[pygame.K_RIGHT] and keys[pygame.K_LALT]):
                player_1.walk_control(DIRECCION_R,animation_speed=6,is_running=True)

            elif(not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]):
                player_1.stay_control(animation_speed=12)

            elif(keys[pygame.K_LEFT] and keys[pygame.K_RIGHT]):
                player_1.stay_control(animation_speed=12)
    else:
        player_1.hit_animation(delta_ms,False)

    screen.blit(imagen_fondo,imagen_fondo.get_rect()) #fundimos la imagen de fondo

    for plataforma in lista_plataformas:
        plataforma.draw(screen)

    delta_ms = clock.tick(FPS)  #limitando que vaya a una velocidad determinada
    player_1.update(delta_ms,lista_plataformas)
    player_1.draw(screen)

    enemigo_1.animation_enemy(delta_ms)
    enemigo_1.update(delta_ms,lista_plataformas)
    enemigo_1.draw(screen)

    for bullet in enemigo_1.bullet_group.sprites():
        if(bullet.rect.colliderect(player_1.rect_limit_colition)) or \
            enemigo_1.rect.colliderect(player_1.rect_limit_colition):

            player_1.animation = player_1.hit_animation(delta_ms,True)
            bullet.kill()
    if (player_1.is_punching):
        if(player_1.rect.colliderect(enemigo_1.rect)) or enemigo_1.is_hit:
            enemigo_1.hit_animation(delta_ms,False)
            enemigo_1.move_x = 0
            enemigo_1.ready = False
    
    
    # enemigos update
    # player dibujarlo
    # dibujar todo el nivel
    
    
    time = tiempo.temporizador(int(delta_ms))
    draw_text(f"Vidas: {player_1.lives}", font, NEGRO, ANCHO_VENTANA/8,80)
    draw_text(f"Time: {time}", font, YELLOW, ANCHO_VENTANA/2,80)

    pygame.display.flip()
    
    tiempo_mil += delta_ms
    tiempo_int = int(tiempo_mil/1000)

    print(f'clock: {tiempo_int}')



    






