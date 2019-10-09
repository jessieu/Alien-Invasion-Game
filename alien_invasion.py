import pygame
import sys
from settings import Settings
from ship import Ship 
import game_functions as gf 
from pygame.sprite import Group
from game_stats import GameStats 
from button import Button
from scoreboard import Scoreboard

def run_game():
	#Initialize the game and create a screen object
	pygame.init()
	
	#Access the Settings
	ai_settings = Settings()
	screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))

	#set the caption of the screen to the name of our game
	pygame.display.set_caption("Alien Invasion") 

	#Make the play button
	play_button = Button(ai_settings, screen, "Play")

	#Game statistics
	stats = GameStats(ai_settings)

	#Scoreboard
	sb = Scoreboard(ai_settings, screen, stats)

	#Make a ship
	ship = Ship(ai_settings, screen)

	#Make a group to store bullets in
	bullets = Group()

	#Make a group to store aliens
	aliens = Group()

	#Create the fleet of aliens
	gf.create_fleet(ai_settings, screen, aliens, ship)

	#Start the main loop for the game
	while True:
		gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)
		
		if stats.game_active:
			ship.update()
			gf.update_bullets(ai_settings, sb, screen, ship, bullets, aliens, stats)
			gf.update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)
		
		gf.update_screen(ai_settings, stats, screen, ship, bullets, aliens, play_button, sb)

run_game()				
