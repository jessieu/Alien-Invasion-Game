class Settings():
	"""A class to store all settings for Alien Invasions"""
	def __init__(self):
		"""Initialize the game's settings"""
		#Screen Settings
		self.screen_width = 1300
		self.screen_height = 650
		self.bg_color = (230,230,230)

		#Ship setting
		self.ship_speed_factor = 1.5
		self.ship_limit = 3

		#Bullet settings
		self.bullet_speed_factor = 1
		self.bullet_width = 5
		self.bullet_height = 5
		self.bullet_color = (60,60,60)
		self.bullets_allowed = 3

		#Alien settings
		self.alien_speed_factor = 1
		self.fleet_drop_speed = 10
		#Set fleet_direction to 1 == right
		self.fleet_direction = 1

		#How quickly the game speeds up
		self.speedup_scale = 1.1

		#How quickly the alien point value increase
		self.score_scale = 1.5

		#Scoring
		self.alien_points = 50

		self.initialize_dynamic_settings()

	def initialize_dynamic_settings(self):
		"""Initialize settings that change throughout the game"""
		self.ship_speed_factor = 1.5
		self.bullet_speed_factor =3
		self.alien_speed_factor = 1

		self.fleet_direction = 1

	def increase_speed(self):
		"""Increase the speed setting"""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale) 	
