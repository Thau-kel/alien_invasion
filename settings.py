class Settings:
    """一个存储游戏所有设置的类."""

    def __init__(self):
        """初始化游戏的静态设置."""
        # 屏幕设置
        self.screen_width = 900
        self.screen_height = 600
        self.bg_color = (255, 255, 255)

        # 飞船设置, 数量
        self.ship_limit = 3        

        # 子弹设置
        self.bullet_width = 500
        self.bullet_height = 15
        self.bullet_color = 0, 0, 255
        self.bullets_allowed = 3

        # 舰队下降速度
        self.fleet_drop_speed = 10

        # 以多大的加速度加速游戏
        self.speedup_scale = 1.1
        # 外星人点数增长速度
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而发生变化的设置"""
        self.ship_speed_factor = 1
        self.bullet_speed_factor = 3
        # 外星人左右移动速度
        self.alien_speed_factor = 1
        # 舰队方向 1 向右, -1 向左.
        self.fleet_direction = 1

        # 计分
        self.alien_points = 50

    def increase_speed(self):
        """提高速度的设置和外星人点数"""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)