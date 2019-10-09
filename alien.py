import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	def __init__(self, ai_settings, screen):
		super().__init__()
		self.ai_settings = ai_settings
		self.screen = screen

		#load the alien image and get its rect
		self.image = pygame.image.load('images/alien.bmp')
		self.rect = self.image.get_rect()
		
		#Start each new alien near the top left of the screen
		#(x and y is the distance from the screen to the image)
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height

		#Store alien's exact position
		self.x = float(self.rect.x)

	def blitme(self):
		"""Draw the alien at its current location"""
		self.screen.blit(self.image, self.rect)		

	def update(self):
		"""Move the alien left or right"""
		speed = self.ai_settings.alien_speed_factor
		direction = self.ai_settings.fleet_direction
		self.x += (speed * direction)
		self.rect.x = self.x 

	def check_edge(self):
		"""Return True if the alien is at the edge of screen"""
		screen_rect = self.screen.get_rect()
		if self.rect.right >=  screen_rect.right:
			return True
		elif self.rect.left <= 0:
			return True	


	
