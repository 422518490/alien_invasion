class GameStatus():
	"""跟踪游戏的统计信息"""
	
	def __init__(self,ai_setting):
		"""初始化统计信息"""
		self.ai_setting = ai_setting;
		self.rest_status();
		#游戏结束
		self.game_active = False;
		#在任何情况下都不重置最高分
		self.high_score = 0;
		
	def rest_status(self):
		"""初始化在游戏运行期间可能变化的统计信息"""
		self.ship_left = self.ai_setting.ship_limit;
		#游戏计分
		self.score = 0;
		#玩家等级
		self.level = 1;
