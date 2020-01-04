import pygame
from pygame import mixer
import random
import math

pygame.init()

screen = pygame.display.set_mode((800,600))

pygame.display.set_caption("Space Invaders")

background = pygame.image.load('space.jpg')
mixer.music.load('background.wav')
mixer.music.play(-1)

playerImg = pygame.image.load('spaceship.png')
playerX = 370
playerY = 480 
dxp = 0
dyp = 0

enemyImg = []
enemyX = []
enemyY = []
dxe = []
dye = 0
en = 20

for i in range(en):
	enemyImg.append(pygame.image.load('ufo.png'))
	enemyX.append(random.randint(0,800-64))
	enemyY.append(random.randint(0,200))
	dxe.append(1)

bulletImg = []
bulletX = []
bulletY = []
bn = 0
bullet_fire = False

font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10

life = 3
kill = 0

def score(g,x,y):
	if not g:
		score_text = "Lives: " + str(life)+" Kills: " + str(kill)
	else:
		score_text = "Game Over"
	score = font.render(score_text, True, (255,255,255))
	screen.blit(score,(x,y))

def player(x,y):
	screen.blit(playerImg,(x,y))

def enemy(e,x,y):
	screen.blit(e,(x,y))

def fire(b,x,y):
	global bullet_fire
	bullet_fire = True
	screen.blit(b,(x,y))

def isCollision(eX,eY,x,y):
	distance = math.sqrt(math.pow(eX-x,2)+math.pow(eY-y,2))
	if distance < 50:
		return True
	else:
		return False

running = True
while running:
	screen.blit(background,(0,0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				dxp = -1
			if event.key == pygame.K_RIGHT:
				dxp = 1
			if event.key == pygame.K_UP:
				dyp = -1
			if event.key == pygame.K_DOWN:
				dyp = 1
			if event.key == pygame.K_SPACE:
				bulletImg.append(pygame.image.load('bullet.png'))
				bulletX.append(0)
				bulletY.append(480)
				bn += 1
				mixer.music.load('laser.wav')
				mixer.music.play()
				if not bullet_fire:
					bulletX[bn-1] = playerX
					fire(bulletImg[bn-1],bulletX[bn-1],bulletY[bn-1])
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or pygame.K_RIGHT:
				dxp = 0
			if event.key == pygame.K_UP or pygame.K_DOWN:
				dyp = 0
			if event.key == pygame.K_SPACE:
				bullet_fire = False
	playerX+=dxp
	playerY+=dyp
	for i in range(en):
		enemyX[i]+=dxe[i]

	if playerX<0:
		playerX = 0
	elif playerX>800-64:
		playerX = 800-64
	if playerY<0:
		playerY = 0
	elif playerY>600-64:
		playerY = 600-64
	for i in range(en):
		if enemyX[i]<0:
			enemyX[i] = 0
			dxe[i] = 1
			enemyY[i] += 10
		elif enemyX[i]>800-64:
			enemyX[i] = 800-64
			dxe[i] = -1
			enemyY[i] += 10
		if enemyY[i]<0:
			enemyY[i]=0
		elif enemyY[i]>600-64:
			enemyY[i]=600-64
	if bullet_fire:
		fire(bulletImg[bn-1],bulletX[bn-1],bulletY[bn-1])
		bulletY[bn-1] -= 10
	for i in range(en):
		if bn > 0:
			if isCollision(enemyX[i],enemyY[i],bulletX[bn-1],bulletY[bn-1]):
				mixer.music.load('explosion.wav')
				mixer.music.play()
				bulletY[bn-1] = 480
				bullet_fire = False
				kill += 1
				enemyX[i] = random.randint(0,800)
				enemyY[i] = random.randint(50,150)
		if isCollision(enemyX[i],enemyY[i],playerX,playerY):
			mixer.music.load('explosion.wav')
			mixer.music.play()
			playerX = 370
			playerY = 480
			life -= 1
	player(playerX,playerY)
	for i in range(en):
		enemy(enemyImg[i],enemyX[i],enemyY[i])
	if life == 0:
		screen.fill((0,0,0))
	score(life==0,textX,textY)
	

	pygame.display.update()
