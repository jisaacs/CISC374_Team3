import pygame
import spyral
import random
import math

TICKS_PER_SECOND = 6

operators = ["+","-","*","/"]
directions = {}
directions['up'] = 0
directions['down'] = 1
directions['right'] = 2
directions['left'] = 3

# locations are in terms of the discrete grid, with indexing beginning at 0. top-left is origin.
# pixel_x is grid_x*48 + 24, which corresponds to the centers of sprites

fonts = {}
geom = {}
images = {}
colors = {}
strings = {}

# snake is a list of locations occupied by the snake
def openSpace(foodItems,snake):
	taken = True
	while taken:
		taken = False
		loc = (random.randrange(0,25),random.randrange(0,18))
		for item in foodItems:
			if item.location == loc:
				taken = True
		for s in snake:
			if s == loc:
				taken = True
	return loc

class Score(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.val = 0
		self.render()
		
	def render(self):
		self.image = fonts['score'].render("SCORE: %d" % self.val,True,colors['score'])
		self.rect.midtop = (geom['scorex'],geom['text_height'])

# self.express is a list of strings, each of which is a number or operator
class Expression(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.express = []
		self.render()
		
	def render(self):
		self.image = fonts['Expression'].render( " ".join(self.express),True,colors['expression'])
		self.rect.midtop = (geom['expressionx'],geom['text_height'])
		
class Goal(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.val = random.randrange(0,20,1)
		self.render()
	
	def render(self)
		self.image = fonts['goal'].render("Goal: %d" % self.val,True,colors['goal'])
		self.rect.midtop = geom['goalx'],geom['text_height'])

class Length(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.val = 0
		self.render()
		
	def render(self):
		self.image = fonts['length'].render("Length: %d" % self.val,True,colors['length'])
		self.rect.midtop = (geom['lengthx'],geom['text_height'])
		
class Operator(spyral.sprite.Sprite)
	def __init__(self,foodItems,snake):
		spyral.sprite.Sprite.__init__(self)
		self.location = self.openSpace(foodItems,snake)
		self.val = operators[random.randrange(0,4,1)]
		self.image = fonts['operator'].render(self.val,True,colors['operator'])
		self.rect.center = (self.location[0]*48 + 24,self.location[1]*48 + 24)

class Number(spyral.sprite.Sprite):
	def __init__(self,foodItems,snake):
		spyral.sprite.Sprite.__init__(self)
		self.location = self.openSpace(foodItems,snake)
		self.val = random.randrange(0,15,1)
		self.image = fonts['number'].render("%d" % self.val,True,colors['number'])
		self.rect.center = (self.location[0]*48 + 24,self.location[1]*48 + 24)

class SnakeNode(spyral.sprite.Sprite):
	def __init__(self,val,dir,loc):
		sypral.sprite.Sprite.__init__(self)
		self.value = val
		self.next = None
		self.direction = dir
		self.location = loc
		self.render()
	
	def render(self):
		self.image = fonts['node'].render(str(self.value),True,colors['node'])
		self.rect.center = (self.location[0]*48 + 24,self.location[1]*48 + 24)
		
class Snake(spyral.sprite.Sprite):
	def __init__(self):
		spyral.sprite.Sprite.__init__(self)
		self.image = images['head']
		self.location = (11,8)
		self.firstNode = None
		self.clearing = False
		self.collapsing = False
		self.length = 0
		self.direction = directions['up']
		self.render()
	
	def render(self):
		self.rect.center = (self.location[0]*48 + 24,self.location[1]*48 + 24)
		
class Game(spyral.scene.Scene):
	def __init__(self):
		spyral.scene.Scene.__init__(self)
		self.camera = spyral.director.get_camera()
		self.group = spyral.sprite.Group(self.camera)
		background = spyral.util.new_surface((1200,900))
		background.fill(colors['background'])
		self.camera.set_background(background)
		self.goal = 15
		self.snake = Snake()
		self.group.add(self.snake)
		self.moving = False
	
	def update(self):
		for event in pygame.event.get([pygame.KEYUP, pygame.KEYDOWN]):
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					self.moving = True
					self.snake.direction = directions['up']
				elif event.key == pygame.K_DOWN:
					self.moving = True
					self.snake.direction = directions['down']
				elif event.key == pygame.K_RIGHT:
					self.moving = True
					self.snake.direction = directions['right']
				elif event.key == pygame.K_LEFT:
					self.moving = True
					self.snake.direction = directions['left']
			elif event.type == pygame.KEYUP:
				if event.key == pygame.K_UP and self.snake.direction == directions['up']:
					self.moving = False
				elif event.key == pygame.K_DOWN and self.snake.direction == directions['down']:
					self.moving = False
				elif event.key == pygame.K_RIGHT and self.snake.direction == directions['right']:
					self.moving = False
				elif event.key == pygame.K_LEFT and self.snake.direction == directions['left']:
					self.moving = False
		pygame.event.clear()
		
		self.group.update()
		
		
					