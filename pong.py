#!/usr/bin/python3
import pygame, sys, random
from pygame.locals import *
from fonts import *
BLUE = (72, 61, 139)
BLACK       = (0, 0, 0)
WHITE       = (255, 255, 255)
RED 		= (205, 92, 92)
WIDTH       = 700
HEIGHT      = 500
BALL_RADIUS = 8
PAD_WIDTH   = 8
PAD_HEIGHT  = 70
DIFF 		= 2
TOPSCORE    = 10	

pygame.init()
fpsClock = pygame.time.Clock()
window_obj = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption("Pong")



class Paddle_obj_class():
	def __init__(self, pos, vel, width, height, color, score):
		self.pos    = pos
		self.vel    = vel
		self.width  = width
		self.height = height
		self.color  = color
		self.score  = score
	def draw(self, window_obj):
		pygame.draw.line(window_obj, self.color, (self.pos[0], self.pos[1] - self.height/2), (self.pos[0], self.pos[1] + self.height/2), self.width)
	def update(self):
		if self.pos[1]+self.vel > int(self.height/2) and self.pos[1]+self.vel < int(HEIGHT-self.height/2):
			self.pos[1]=self.pos[1]+self.vel 
	
def check_collision(ball, paddle1, paddle2):
	if ball.pos[0] <= paddle1.width*2 + ball.radius or ball.pos[0] >= WIDTH - paddle1.width*2 - ball.radius:
		if (ball.pos[1] in range(paddle1.pos[1] - int(paddle1.height/2), paddle1.pos[1] + int(paddle1.height/2)) and ball.pos[0] > int(WIDTH/2)) or (ball.pos[1] in range(paddle2.pos[1] - int(paddle2.height/2), paddle2.pos[1] + int(paddle2.height/2)) and ball.pos[0] < int(WIDTH/2)):
			if ball.vel[0]<0:
				ball.vel[0] =- (ball.vel[0]-1)
			else:
				ball.vel[0] =- (ball.vel[0]+1)
		else:
			if ball.pos[0]>int(WIDTH/2):
				paddle1.score +=1
				ball.reset_game("Left")
			else:
				paddle2.score +=1
				ball.reset_game("Right")

def winning(window_obj, player):
	window_obj.fill(BLACK)
	try:
		font             = pygame.font.Font("fonts/Megadeth.ttf", 70)
	except:
		font             = pygame.font.Font(None, 70)
	msg 			= font.render(player + "", True, WHITE)
	msgRect         = msg.get_rect()
	msgRect.centerx = int(WIDTH/2)
	msgRect.centery = int(HEIGHT/2)
	window_obj.blit(msg, msgRect)
	pygame.display.update()
	while True:	
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				new_game(window_obj)
				return

def scores(window_obj, score1, score2):
	try:
		font          = pygame.font.Font("fonts/impact.ttf", 40)
	except:
		font          = pygame.font.Font(None, 40)
	message1          = font.render(str(score1), True, WHITE)
	message2          = font.render(str(score2), True, WHITE)
	message1Rect      = message1.get_rect()
	message2Rect      = message2.get_rect()
	message1Rect.left = int(WIDTH/4)
	message2Rect.left = int(WIDTH/4 * 3)
	message1Rect.top  = int(HEIGHT/4)
	message2Rect.top  = int(HEIGHT/4)
	window_obj.blit(message1, message1Rect)
	window_obj.blit(message2, message2Rect)

def draw_options(window_obj, highlight):
	try:
		font             = pygame.font.Font("fonts/Arial.ttf", 56)
		selected_font	 = pygame.font.Font("fonts/Arial.ttf", 70)

	except:
		font             = pygame.font.Font(None, 56)
		selected_font	 = pygame.font.Font(None, 70)

	opt_list	  	 = [font, selected_font]

	message1             = opt_list[highlight].render("PONG", True, (255, 255, 255))
	message1Rect         = message1.get_rect()
	message1Rect.centerx = int(WIDTH/2)
	message1Rect.centery = int(HEIGHT * 1/10)
	message2 = opt_list[highlight].render("AI --NO WALLS", True, (127, 255, 0))
	message2Rect = message2.get_rect()
	message2Rect.centerx = int(WIDTH / 2)
	message2Rect.centery = int(HEIGHT * 3 / 10)


	window_obj.blit(message1, message1Rect)
	window_obj.blit(message2, message2Rect)



def start_game(window_obj, ball, paddle1, paddle2):

	ball.update()
	ball.draw(window_obj)
	paddle1.update()
	paddle2.update()
	paddle1.draw(window_obj)
	paddle2.draw(window_obj)
	check_collision(ball, paddle1, paddle2)
	scores(window_obj, paddle1.score, paddle2.score)
class Ball():
	def __init__(self, radius, color):
		self.radius = radius
		self.color  = color
	def reset_game(self, direction):
		self.pos = [int(WIDTH/2),int(HEIGHT/2)]
		if direction == "Right":
			self.vel = [random.randint(2,4),-random.randint(1,3)]
		elif direction == "Left":
			self.vel = [-random.randint(2,4),-random.randint(1,3)]
	def draw(self, window_obj):
		pygame.draw.circle(window_obj, self.color, self.pos, self.radius)
	def update(self):
		if self.pos[1] <= BALL_RADIUS or self.pos[1] >= HEIGHT-BALL_RADIUS:
			self.vel[1] = -self.vel[1]
		self.pos[0] += self.vel[0]
		self.pos[1] += self.vel[1]	
def new_game(window_obj):

	ball      = Ball(BALL_RADIUS, RED)
	ball.reset_game("Left")
	paddle1   = Paddle_obj_class([int(WIDTH-PAD_WIDTH*2),int(HEIGHT/2)], 0, PAD_WIDTH, PAD_HEIGHT, WHITE, 0)
	paddle2   = Paddle_obj_class([int(PAD_WIDTH*2),int(HEIGHT/2)], 0, PAD_WIDTH, PAD_HEIGHT, WHITE, 0)
	option    = "nil"	
	highlight = 1
	while option == "nil":
		window_obj.fill(BLACK)
		draw_options(window_obj, highlight)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == KEYDOWN:
				if event.key in [K_UP, K_DOWN, K_w, K_s]:
					highlight = highlight ^ 1
				elif event.key == K_RETURN:
					option = bool(highlight ^ 1)
			pygame.display.update()
			fpsClock.tick(60)
	game_loop(window_obj, ball, paddle1, paddle2, option)

def game_loop(window_obj, ball, paddle1, paddle2, AI): #this is the main loop for the game

	while True:
			window_obj.fill(BLUE)
			pygame.draw.aaline(window_obj, WHITE, [350, 0], [350, 500], True)
			start_game(window_obj, ball, paddle1, paddle2)

			if paddle1.score == 1:
				winning(window_obj, 'AI won!')
				return
			elif paddle2.score == 1:
				winning(window_obj, 'You won!')
				return
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
				elif event.type == KEYDOWN:	
					if event.key == K_ESCAPE:
						new_game(window_obj)
						return
					elif event.key == K_UP:
						paddle1.vel = -3
					elif event.key == K_DOWN:
						paddle1.vel = 3				
				elif event.type == KEYUP:
					if event.key == K_UP:
						paddle1.vel = 0
					elif event.key == K_DOWN:
						paddle1.vel = 0




				#this part is for the AI player.
				if ball.vel[0] > 0:
					if paddle2.pos[1] < int(HEIGHT/2):
						paddle2.vel = DIFF
					elif paddle2.pos[1] > int(HEIGHT/2):
						paddle2.vel = -DIFF					

				elif ball.vel[0] < 0:
					if paddle2.pos[1] < ball.pos[1]:
						paddle2.vel = DIFF
					else :
						paddle2.vel = -DIFF
			pygame.display.update()
			fpsClock.tick(60)

new_game(window_obj)
