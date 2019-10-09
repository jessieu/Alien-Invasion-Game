import pygame
from pygame.sprite import Sprite 

class Ship(Sprite):
	def __init__(self, ai_settings, screen):
		"""Initialize the ship and set its starting position"""
		super().__init__()
		self.screen = screen
		self.ai_settings = ai_settings

		#load the ship image and get its rect
		self.image = pygame.image.load('images/ship.bmp')
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()

		#Ship movement flag
		self.moving_left = False
		self.moving_right = False

		#Start each new ship at the bottom center of the screen
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom

		#Store a secimal value for the ship's center
		self.center = float(self.rect.centerx)


	def update(self):
		"""Update the ship's position based on the movement flag"""
		#Check the ship's position and make sure it would not move out of screen
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor

		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor

		#Update rect object from self.center	
		#The centerx would only store the integer part of the center
		#But it is fine enought to display the ship on the screen	
		self.rect.centerx = self.center



	def blitme(self):
		"""Draw the ship at its current location"""
		self.screen.blit(self.image, self.rect)	

	def center_ship(self):
		"""Center the ship on the screen"""
		self.rect.centerx = self.screen_rect.centerx
