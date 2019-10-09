import pygame.font
from ship import Ship
from pygame.sprite import Group 

class Scoreboard():
	def __init__(self, ai_settings, screen, stats):
		"""Initialize scorekeeping attributes"""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats

		#Font settings for scoring information
		self.text_color = (30, 30, 30)
		self.font = pygame.font.SysFont(None, 48)

		#Prepare the initial score image
		self.prep_score()

		#Prepare the high score image
		self.prep_high_score()

		#Prepare the level image
		self.prep_level()

		#Prepare the ship image
		self.prep_ship()

	def prep_score(self):
		"""Turn the score into the rendered image"""
		#Round the value to the nearest 10
		rounded_score = int(round(self.stats.score, -1))
		#Insert comma into number
		score_str = "{:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True, self.text_color,
				self.ai_settings.bg_color)	

		#Display the score at the top right of the screen
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 20
		self.score_rect.top = 20

	def prep_high_score(self):
		"""Turn the high score into the rendered image"""
		high_score = int(round(self.stats.high_score, -1)) 	
		high_score_str = "{:,}".format(high_score)

		self.high_score_image = self.font.render(high_score_str, True, self.text_color,
				self.ai_settings.bg_color)	

		#Display the hight score at the top center of the screen
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx 
		self.high_score_rect.top = 20

	def prep_level(self):
		"""Turn the level into the rendered image"""
		self.level_image = self.font.render(str(self.stats.level), True, self.text_color,
				self.ai_settings.bg_color)	

		#Display the level underneath the score
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 10	

	def prep_ship(self):
		"""Show how many ship left"""
		self.ships = Group()
		for ship_number in range(self.stats.ships_left):
			ship = Ship(self.ai_settings, self.screen)
			ship.rect.x = 10 + ship_number * ship.rect.width
			ship.rect.y = 10
			self.ships.add(ship)


	def show_score(self):
		"""Draw score, high score level, and ship_left to the screen"""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.ships.draw(self.screen)


	

