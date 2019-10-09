import pygame
import sys
from bullet import Bullet
from alien import Alien
from time import sleep

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	"""Response to keypresses and mouse events"""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
		#Shortcut Q to quit	
		elif event.type == pygame.K_BACKSPACE:
			sys.exit()	
		elif event.type == pygame.K_RETURN:
			start_game(ai_settings, screen, stats, play_button, ship, aliens, bullets)			
		elif event.type == pygame.KEYDOWN:
			detect_keydown(ai_settings, screen, event, ship, bullets)
		elif event.type == pygame.KEYUP:
			detect_keyup(event, ship)	
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
				bullets, mouse_x, mouse_y)		 			

#Keys are pressed down
def detect_keydown(ai_settings, screen, event, ship, bullets):
	"""Enable the ship movement""" 
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_SPACE:
		fire_bullets(ai_settings,screen,ship,bullets)
		
#Keys are released
def detect_keyup(event, ship):
	"""Disable the movement"""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False		

def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, 
		bullets, mouse_x, mouse_y):
	"""Start a new game when the player clicks play"""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)


def start_game(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
	#Reset the game setting
	ai_settings.initialize_dynamic_settings()

	#Reset the game stats
	stats.reset_stats()
	stats.game_active = True

	#Reset the scoreboard images.
	sb.prep_score()
	sb.prep_high_score()
	sb.prep_level()
	sb.prep_ship()


	#Empty the list of aliens and bullets
	aliens.empty()
	bullets.empty()

	#Hide the mouse cursor
	pygame.mouse.set_visible(False)

	#Create a new fleet and center the ship
	create_fleet(ai_settings, screen, aliens, ship)
	ship.center_ship()	



def update_screen(ai_settings, stats, screen, ship, bullets, aliens, play_button, sb):
	#Redraw the screen during each pass through the loop
	screen.fill(ai_settings.bg_color)

	#Draw the screen information
	sb.show_score()

	#Redraw all bullets behind ship and aliens
	for bullet in bullets.sprites():
		bullet.draw_bullet()

	#Draw the ship on the screen
	ship.blitme()	

	#Draw aliens on the screen
	aliens.draw(screen)

	#Draw the play button if the game is active
	if not stats.game_active:
		play_button.draw_button()

	#Make the most recently drawn screen visible
	pygame.display.flip()		

def update_bullets(ai_settings, sb, screen, ship, bullets, aliens, stats):
	"""Update position of bullets and get rid of old bullet"""
	#Update bullet position
	bullets.update()

	#Get rid of bullets that have disappeared
	if ship.moving_left or ship.moving_right:
		for bullet in bullets.copy():
			if bullet.rect.bottom < 0: 
				bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, sb, stats)			

def check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets, sb, stats):
	"""Respond to bullet_alien collision."""
	#Remove any bullets and aliens that have collided
	collisions = pygame.sprite.groupcollide(bullets, aliens, False, True)

	#Score it when a bullet hit an alien
	if collisions:
		for alien in collisions.values():
			stats.score += ai_settings.alien_points * len(aliens)
			sb.prep_score()
		high_score_check(stats, sb)	

	if len(aliens) == 0:
		#If the entire fleet is destoryed, level up the game
		bullets.empty()
		ai_settings.increase_speed()

		#Increase the level
		stats.level += 1
		sb.prep_level()

		create_fleet(ai_settings, screen, aliens, ship)			

def fire_bullets(ai_settings, screen, ship, bullets):
	"""Fire a bullet if limit not reached yet"""
	#Create a new bullet and add it to the bullets group
	if len(bullets) < ai_settings.bullets_allowed:
		new_bullet = Bullet(ai_settings, screen, ship)
		bullets.add(new_bullet)	

def get_number_aliens_x(ai_settings, alien_width):
	"""Determine the number of liens that fit in a row"""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x	

def get_number_rows(ai_settings, alien_height, ship_height):
	"""Determine the number of rows of aliens that fit on the screen"""
	available_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows		

def create_aliens(ai_settings, screen, aliens, alien_number, row_number):
	"""Create an alien and place it in the row"""
	alien = Alien(ai_settings,screen)
	alien_width = alien.rect.width
	alien_height = alien.rect.height
	alien.x = alien_width + 2 * alien_width * alien_number 
	alien.rect.x = alien.x
	alien.rect.y = alien_height + 10 + 2 * alien_height * row_number 
	aliens.add(alien)

def create_fleet(ai_settings, screen, aliens, ship):
	"""Create a full fleet of aliens"""
	#Create an alien
	alien = Alien(ai_settings, screen)
	
	#find the number of aliens in a row
	alien_width = alien.rect.width
	number_aliens_x = get_number_aliens_x(ai_settings, alien_width)

	#find the number of rows of aliens on the screen
	alien_height = alien.rect.height
	ship_height = ship.rect.height
	number_rows = get_number_rows(ai_settings, alien_height, ship_height)

	#Create aliens row by row
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			create_aliens(ai_settings, screen, aliens, alien_number, row_number)		

def update_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Check if he fleet is at an edge, 
		and then update the position of all aliens in the fleet"""
	check_fleet_edges(ai_settings, aliens)
	aliens.update()

	#Look for alien-ship collisions
	if pygame.sprite.spritecollideany(ship, aliens):
		ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)

	#Look for alien hitting the bottom of the screen
	check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets)

				

def check_fleet_edges(ai_settings,aliens):
	"""Respond appropriately if any aliens have reached an edge"""
	for alien in aliens.sprites():
		if alien.check_edge():
			change_fleet_direction(ai_settings, aliens)
			break

def change_fleet_direction(ai_settings, aliens):
	"""Drop the entire fleet and change the fleet direction."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1

def ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Respond to ship being hit by alien"""
	if stats.ships_left > 0:
		#Decrement ship_left
		stats.ships_left -= 1

		#Update scoreboard
		sb.prep_ship()

		#Empty the list of aliens and bullets
		aliens.empty()
		bullets.empty()

		#Create a new fleet and center the ship
		create_fleet(ai_settings, screen, aliens, ship)
		ship.center_ship()

		#Pauses
		sleep(0.5)

	else:
		stats.game_active = False
		#Make the mouse cursor reappear
		pygame.mouse.set_visible(True)	
	

def check_aliens_bottom(ai_settings, stats, sb, screen, ship, aliens, bullets):
	"""Check if any aliens reach the bottom of the screen"""
	screen_rect = screen.get_rect()
	for alien in aliens:
		if alien.rect.bottom >= screen_rect.bottom:
			#Treat this the same as if the ship got hit
			ship_hit(ai_settings, stats, sb, screen, ship, aliens, bullets)
			break

def high_score_check(stats, sb):
	"""Check to see if there's a new high score"""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()	

	

