import pygame;

from pygame.sprite import Sprite;

class Alien(Sprite):
	
	def __init__(self,ai_setting,screen):
		super().__init__();
		self.ai_setting = ai_setting;
		self.screen = screen;
		
		#加载外星人图片，并设置rect属性
		self.image = pygame.image.load("images\smallfei.png");
		self.rect = self.image.get_rect();
		
		#每个外星人初始都在屏幕左上角附近
		self.rect.x = self.rect.width;
		self.rect.y = self.rect.height;
		
		#存储外星人的准确位置
		self.x = float(self.rect.x);
		
		
	
	def blitme(self):
		"""在指定位置绘制外星人"""
		self.screen.blit(self.image,self.rect);
	
	def update(self):
		self.x += (self.ai_setting.alien_speed_factor*self.ai_setting.fleet_direction);
		self.rect.x = self.x;
	
	def check_edges(self):
		'''如果外星人位于屏幕边缘，则返回True'''
		screen_rect = self.screen.get_rect();
		if self.rect.right >= screen_rect.right:
			return True;
		elif self.rect.left <= 0:
			return True;
