import pygame
import neat
import time
import os
import random

WIN_WIDTH = 550
WIN_HEIGHT = 800

BIRD_IMGS = [
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
	pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png")))
]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))

class Bird:
	IMGS = BIRD_IMGS
	MAX_ROTATION = 25
	ROT_VEL = 20
	ANIM_TIME = 5

	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.tilt = 0
		self.tick_count = 0
		self.vel = 0
		self.height = self.y
		self.img_count = 0
		self.anim_index = 0
		self.img = self.IMGS[0]

	def jump(self):
		self.vel = -10.5
		self.tick_count = 0
		self.height = self.y	# store what height the bird jumped at

	def move(self):
		self.tick_count += 1	# bird updates move every frame (tick)

		d = self.vel*self.tick_count + 1.5*self.tick_count**2	# calculate displacement -> as tick_count goes up, displacement becomes more positive pointing downwards -> falls.
		if d >= 16:
			d = 16 # terminal velocity cap

		if d < 0: # jump boost, tweak
			d -= 2

		self.y += d # move bird vertically using calculated displacement

		if d < 0 or self.y < self.height + 50:
			# if bird is moving upward, or is still above height jumped at
			if self.tilt < self.MAX_ROTATION:
				self.tilt = self.MAX_ROTATION
			
		else:
			# tilt the bird downward: bird's displacement is positive, or height is below jumped height.
			if self.tilt > -90:
				self.tilt -= self.ROT_VEL # gradually rotate the bird to face the ground when falling.

	def draw(self, window):
		self.img_count += 1

		if (self.img_count % 3 == 0):
			# every 3 frames
			self.anim_index += 1
			if self.anim_index > 3:
				self.anim_index = 0

		self.img = self.IMGS[self.anim_index]

		if self.tilt <= -80:
			self.img = self.IMGS[1]
			self.anim_index = 1

		rotated_image = pygame.transform.rotate(self.img, self.tilt) # img, angle
		new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
		window.blit(rotated_image, new_rect.topleft)
	
	def get_mask(self):
		return pygame.mask.from_surface(self.img)


def draw_window(window, bird):
	window.blit(BG_IMG, (0, 0))
	bird.draw(window)

	pygame.display.update()

def main():
	bird = Bird(200, 200)
	window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
	clock = pygame.time.Clock()

	run = True

	while run:
		clock.tick(30) # 30 ticks/second max
		for event in pygame.event.get():
			# get any events occuring in pygame window
			if event.type == pygame.QUIT:
				run = False

		#bird.move()

		draw_window(window, bird)

	# ends loop when run = false is executed
	pygame.quit() # quit pygame
	quit() # close program

main()



		