import pygame, random, math

WIDTH, HEIGHT = 800, 600
WIDTH_IMG, HEIGHT_IMG = 80, 80
WIDTH_IMG_ENEMY, HEIGHT_IMG_ENEMY = 50, 50
WIDTH_IMG_BULLET, HEIGHT_IMG_BULLET = 50, 50
SPACESHIPX, SPACESHIPY = 350, 500
CHANGEX, CHANGEY = 0, 0
BULLETX, BULLETY = 365, 520
score=0

pygame.init()

def picture_color(img):
    for x in range(img.get_width()):
        for y in range(img.get_height()):
            # Obtenemos el color de cada píxel
            color = img.get_at((x, y))
            # Si el píxel no es completamente transparente, cambiamos su color
            if color[3] != 0:
                # Redefinimos el color a un tono de naranja
                new_color = (255, 165, 0, color[3])  # Agregamos el canal alpha para mantener la transparencia
                # Asignamos el nuevo color al píxel
                img.set_at((x, y), new_color)
    return img


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter Game")
icon = pygame.image.load('./img/icon.png')
pygame.display.set_icon(icon)

background = pygame.image.load('./img/bg.jpg')

playerimg = pygame.image.load('./img/cohete.png')
player_scaled = pygame.transform.scale(playerimg, (WIDTH_IMG, HEIGHT_IMG))

enemyimg = pygame.image.load('./img/alien.png')
enemyimg_color = enemyimg.copy()

new_enemyimg_color = picture_color(enemyimg_color)

enemyimg_scaled = pygame.transform.scale(new_enemyimg_color, (WIDTH_IMG_ENEMY, HEIGHT_IMG_ENEMY))
alienX=random.randint(0, 740)
alienY=random.randint(30, 30)
alienSpeedX=0.5
alienSpeedY=30

bulletimg = pygame.image.load('./img/bala.png')
bulletimg_scaled = pygame.transform.scale(bulletimg, (WIDTH_IMG_BULLET, HEIGHT_IMG_BULLET))
check = False

def score_text():
    font = pygame.font.SysFont('Arial', 28, 'bold')
    img = font.render(f'Score: {score}', True, 'white')
    screen.blit(img, (5,5))

def game_over():
    font_gameover = pygame.font.SysFont('Arial', 64, 'bold')
    font_restart = pygame.font.SysFont('Arial', 32, 'bold')
    img = font_gameover.render('GAME OVER', True, 'white')
    img_restart = font_restart.render('Presiona R para volver a empezar', True, 'white')
    screen.blit(img, (220,180))
    screen.blit(img_restart, (200,250))

enemyimg_scaled = []
alienX = []
alienY = []
alienSpeedX = []
alienSpeedY = []
no_of_aliens = 6

for i in range(no_of_aliens):
    enemyimg = pygame.image.load('./img/alien.png')
    enemyimg_color = enemyimg.copy()
    new_enemyimg_color = picture_color(enemyimg_color)
    enemyimg_scaled.append(pygame.transform.scale(new_enemyimg_color, (WIDTH_IMG_ENEMY, HEIGHT_IMG_ENEMY)))
    alienX.append(random.randint(0, 740))
    alienY.append(random.randint(30, 30))
    alienSpeedX.append(0.5)
    alienSpeedY.append(30)

running = True
while running:
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running= False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                CHANGEX=-1
            if event.key == pygame.K_RIGHT:
                CHANGEX=1
            if event.key == pygame.K_SPACE:
                if check is False:
                    check=True
                    BULLETX=SPACESHIPX+15
            if event.key == pygame.K_r:  # Reiniciar juego al presionar 'R'
                if not running:
                    running = True
        if event.type == pygame.KEYUP:
            CHANGEX=0

    SPACESHIPX+=CHANGEX

    if SPACESHIPX<=0:
        SPACESHIPX=0
    elif SPACESHIPX>=720:
        SPACESHIPX=720

    for i in range(no_of_aliens):
        if alienY[i] > 470:
            for j in range(no_of_aliens):
                alienY[j]=2000
            game_over()
            break
         
        alienX[i]+=alienSpeedX[i]
        if alienX[i]<=7:
            alienSpeedX[i]=0.5
            alienY[i]+=alienSpeedY[i]
        elif alienX[i]>=740:
            alienSpeedX[i]=-0.5
            alienY[i]+=alienSpeedY[i]

        
        distance = math.sqrt(math.pow(BULLETX-alienX[i], 2)+math.pow(BULLETY-alienY[i],2))
        if distance<30:
            BULLETY=520
            check=False
            alienX[i]=random.randint(0, 740)
            alienY[i]=random.randint(30, 30)
            score+=1
        screen.blit(enemyimg_scaled[i], (alienX[i], alienY[i]))

    if BULLETY<=0:
        BULLETY=520
        check=False

    if check is True:
        screen.blit(bulletimg_scaled, (BULLETX, BULLETY))
        BULLETY-=0.7

    score_text()

    screen.blit(player_scaled, (SPACESHIPX, SPACESHIPY))
    pygame.display.update()