class GameStats():
    """跟踪游戏的统计数据信息"""

    def __init__(self, ai_settings):
        """初始化统计信息"""
        self.ai_settings = ai_settings
        self.reset_stats()

        # 刚启动游戏时处于非活动状态
        self.game_active = False

        # 最高分不被重置
        self.high_score = 0

    def reset_stats(self):
        """初始化在游戏运行期间可能发生变化的统计数据信息"""
        # 重新分配给玩家规定数目的飞船
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1