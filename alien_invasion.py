
import pygame;
from pygame.sprite import Group;

from settings import Setting;
from ship import Ship;
import game_function as gf;
from alien import Alien;
from game_status import GameStatus;
from button import Button;
from score_board import ScoreBoard;

def run_game():
	#初始化游戏并创建一个屏幕对象
	pygame.init();
	
	ai_setting = Setting();
	
	screen = pygame.display.set_mode((ai_setting.screen_width,ai_setting.screen_height));
	pygame.display.set_caption("alien_invasion");
	
	#创建play按钮
	play_button = Button(ai_setting,screen,"Play");
	
	#创建一个用于存储游戏统计信息的实例
	status = GameStatus(ai_setting);
	#创建计分实例
	sb = ScoreBoard(ai_setting,screen,status);
	
	#创建一艘飞船
	ship = Ship(ai_setting,screen);
	#创建一个外星人
	#alien = Alien(ai_setting,screen);
	
	#创建一个用于存放子弹的组
	bullets = Group();
	
	#设置背景色
	#bg_color = (230,230,230);
	
	#创建一个用于存放外星人的组
	aliens = Group();
	#创建外星人群
	gf.create_fleet(ai_setting,screen,ship,aliens);
	
	#开始游戏主循环
	while True:
		
		#监视键盘和鼠标事件
		gf.check_events(ai_setting,screen,status,sb,play_button,ship,aliens,bullets);
		#还有飞船的时候更新
		if status.game_active:
			#更新飞船位置
			ship.update();
			
			
			#更新外星人位置
			gf.update_aliens(ai_setting,status,sb,screen,ship,aliens,bullets);
			
			#更新子弹信息
			gf.update_bullets(ai_setting,screen,status,sb,ship,aliens,bullets);
		
		#刷新屏幕
		gf.update_screen(ai_setting,screen,status,sb,ship,aliens,bullets,play_button);

run_game();
