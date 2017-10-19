import pygame;
from pygame.sprite import Sprite;

class Ship(Sprite):
	
	def __init__(self,ai_setting,screen):
		
		"""初始化飞船及其位置"""
		super(Ship,self).__init__();
		
		self.screen = screen;
		
		self.ai_setting = ai_setting;
		
		#加载飞船图形并获取其外接矩形
		self.image = pygame.image.load("images/small.png");
		self.rect = self.image.get_rect();
		self.screen_rect = screen.get_rect();
		
		#将每艘新飞船放在屏幕底部中间
		self.rect.centerx = self.screen_rect.centerx;
		self.rect.bottom = self.screen_rect.bottom;
		self.center = float(self.rect.centerx);
		
		#向右移动标识
		self.moving_right = False;
		#向左移动标识
		self.moving_left = False;
		
	def blitme(self):
		"""在指定位置绘制飞船"""
		self.screen.blit(self.image,self.rect);
	
	def update(self):
		"""向右移动"""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_setting.ship_speed_factor;
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_setting.ship_speed_factor;
		
		self.rect.centerx = self.center;
		
	def center_ship(self):
		self.center = self.screen_rect.centerx;
