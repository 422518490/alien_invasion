import sys;
import pygame;
from time import sleep;

from bullet import Bullet;
from alien import Alien;

def check_keydown_events(event,ai_setting,screen,ship,bullets):
	"""响应按键"""
	if event.key == pygame.K_RIGHT:
	#向右移动飞船
		ship.moving_right = True;
	elif event.key == pygame.K_LEFT:
		#向左移动飞船
		ship.moving_left = True;
	elif event.key == pygame.K_SPACE:
		#发射子弹
		fire_bullet(ai_setting,screen,ship,bullets);
	elif event.key == pygame.K_q:
		sys.exit();
		
def check_keyup_events(event,ship):
	"""响应松开按键"""
	if event.key == pygame.K_RIGHT:
		#停止向右移动飞船
		ship.moving_right = False;
	elif event.key == pygame.K_LEFT:
		#停止向左移动飞船
		ship.moving_left = False;

def check_events(ai_setting,screen,status,sb,play_button,ship,aliens,bullets):
	#监视键盘和鼠标事件
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit();
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event,ai_setting,screen,ship,bullets);
		elif event.type == pygame.KEYUP:
			check_keyup_events(event,ship);
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x,mouse_y = pygame.mouse.get_pos();
			check_play_button(ai_setting,screen,status,sb,ship,aliens,bullets,play_button,mouse_x,mouse_y);


def check_play_button(ai_setting,screen,status,sb,ship,aliens,bullets,play_button,mouse_x,mouse_y):
	"""在玩家点击play按钮后游戏开始"""
	button_click = play_button.rect.collidepoint(mouse_x,mouse_y);
	if button_click and not status.game_active:
		#重置游戏设置
		ai_setting.initialize_dynamic_settings();
		
		#隐藏光标
		pygame.mouse.set_visible(False);
		
		#重置游戏统计信息
		status.rest_status();
		status.game_active = True;
		
		#清空外星人列表和子弹列表
		aliens.empty();
		bullets.empty();
		
		#重置记分牌图像
		sb.prep_score();
		sb.prep_high_score();
		sb.prep_level();
		sb.prep_ship();
		
		#创建一群新的外星人，并把飞船放到屏幕底端中央
		create_fleet(ai_setting,screen,ship,aliens);
		ship.center_ship();

def update_screen(ai_setting,screen,status,sb,ship,aliens,bullets,play_button):
	"""更新屏幕上的图像，并切换到新屏幕"""
	#每次循环都重绘屏幕
	screen.fill(ai_setting.bg_color);
	
	#在飞船和外星人后面绘制所有子弹
	for bullet in bullets.sprites():
		bullet.draw_bullet();
		
	#绘制飞船
	ship.blitme();
	
	#绘制外星人
	#alien.blitme();
	aliens.draw(screen);
	
	#显示得分
	sb.show_score();
	
	#如果游戏没有运行，则绘制Play按钮
	if not status.game_active:
		play_button.draw_button();
	
	#让屏幕可见
	pygame.display.flip();

def update_bullets(ai_setting,screen,status,sb,ship,aliens,bullets):
	"""更新子弹位置并删除消失的子弹"""
	bullets.update();
		
	#删除已经消失的子弹
	for bullet in bullets.copy():
		if bullet.rect.bottom <= 0:
			bullets.remove(bullet);
	check_bullet_alien_collision(ai_setting,screen,status,sb,ship,aliens,bullets);
	
def check_bullet_alien_collision(ai_setting,screen,status,sb,ship,aliens,bullets):
	#检查是否有子弹击中了外星人，如果有则删除相应的子弹和外星人
	collisions = pygame.sprite.groupcollide(aliens,bullets,True,True); 
	print(len(bullets));
	print("外星人的数量：" + str(len(aliens)));
	if collisions:
		#针对一颗子弹射中多个外星人
		for alienss in collisions.values():
			status.score += ai_setting.alien_points * len(alienss);
			sb.prep_score();
		check_high_score(status,sb);
		
	if len(aliens) == 0 :
		#删除现有的子弹，并新建外星人
		bullets.empty();
		ai_setting.increase_speed();
		create_fleet(ai_setting,screen,ship,aliens);
		#提高等级
		status.level += 1;
		sb.prep_level();

def fire_bullet(ai_setting,screen,ship,bullets):
	"""如果没有到达限制则发射子弹"""
	#判断屏幕上的子弹是否小于指定的数量
	if len(bullets) < ai_setting.bullet_allowed :
		#创建一颗子弹将其加入到bullets中
		new_bullet = Bullet(ai_setting,screen,ship);
		bullets.add(new_bullet);
		
def get_number_aliens_x(ai_setting,alien_width):
	'''计算一行可以容纳多少个外星人'''
	available_space_x = ai_setting.screen_width - 2*alien_width;
	numbers_alien_x = int(available_space_x/(2*alien_width));
	return numbers_alien_x;
	
def get_number_rows(ai_setting,ship_height,alien_height):
	'''计算屏幕可以容纳多少行外星人'''
	availiable_space_y = ai_setting.screen_height - (3*alien_height) - ship_height;
	number_rows = int(availiable_space_y/(2*alien_height));
	return number_rows;
	
def create_alien(ai_setting,screen,ship,aliens,alien_number,row_number):
	'''建一个外星人并把其加入当前行'''
	alien = Alien(ai_setting,screen);
	alien_width = alien.rect.width;
	alien.x = alien_width + 2*alien_width * alien_number;
	alien.rect.x = alien.x;
	alien.rect.y = ship.rect.height + 5 + alien.rect.height + 2*alien.rect.height*row_number;
	aliens.add(alien);

def create_fleet(ai_setting,screen,ship,aliens):
	"""创建外星人群"""
	#创建一个外星人，并计算一行可以容纳多少个外星人
	#外星人间距为外星人宽度
	alien = Alien(ai_setting,screen);
	numbers_alien_x = get_number_aliens_x(ai_setting,alien.rect.width);
	
	number_rows = get_number_rows(ai_setting,ship.rect.height,alien.rect.height);
	
	for number_row in range(number_rows):
		#创建第一行外星人
		for alien_number in range(numbers_alien_x + 1):
			#创建一个外星人并把其加入当前行
			create_alien(ai_setting,screen,ship,aliens,alien_number,number_row);

def update_aliens(ai_setting,status,sb,screen,ship,aliens,bullets):
	'''更新外星人人群中所有外星人的位置'''
	check_fleet_edges(ai_setting,aliens);
	aliens.update();
	
	#检查外星人和飞船之间的碰撞
	if pygame.sprite.spritecollideany(ship,aliens):
		ship_hit(ai_setting,status,sb,screen,ship,aliens,bullets);
	
	#检查是否有外星人到底底部
	check_aliens_bottom(ai_setting,status,sb,screen,ship,aliens,bullets);
	
def check_fleet_edges(ai_setting,aliens):
	'''有外星人到达边缘时采取相应措施'''
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_setting,aliens);
			break;
			
def change_fleet_direction(ai_setting,aliens):
	'''将整个外星人人群下移并改变方向'''
	for alien in aliens.sprites():
		alien.rect.y += ai_setting.fleet_drop_speed;
	ai_setting.fleet_direction *= -1;
	
def ship_hit(ai_setting,status,sb,screen,ship,aliens,bullets):
	"""响应被外星人撞到飞船"""
	if status.ship_left > 0:
		#将ship_left减1
		status.ship_left -= 1;
		
		#更新记分牌
		sb.prep_score();
		sb.prep_ship();
		
		#清空外星人列表和子弹列表
		aliens.empty();
		bullets.empty();
		
		#创建一群新的外星人，并把飞船放到屏幕底端中央
		create_fleet(ai_setting,screen,ship,aliens);
		ship.center_ship();
		
		#暂停
		sleep(0.5);
	else:
		status.game_active = False;
		#让光标可见
		pygame.mouse.set_visible(True);
	
def check_aliens_bottom(ai_setting,status,sb,screen,ship,aliens,bullets):
	"""检查是否有外星人到达屏幕底端"""
	screen_rect = screen.get_rect();
	for alien in aliens.sprites():
		if alien.rect.bottom >= screen_rect.bottom:
			#外星人撞到屏幕底部，飞船也销毁
			ship_hit(ai_setting,status,sb,screen,ship,aliens,bullets);
			break;
			
def check_high_score(status,sb):
	"""检查是否产生了新的最高分"""
	if status.score > status.high_score:
		status.high_score = status.score;
		sb.prep_high_score();
