import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in the fleet."""

    def __init__(self, ai_settings, screen):
        """初始化外星人并设置其初始位置."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像并设置其 rect 属性.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # 初始位置屏幕左上方, x, y 分别是矩形左上角横纵坐标,
        # width 和 height是外星飞船图像矩形的属性
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # 存储外星人的确切位置.
        self.x = float(self.rect.x)

    def blitme(self):
        """在当前位置绘制外星人."""
        # 单个外星人有用, 编组时用draw()
        self.screen.blit(self.image, self.rect)

    def update(self):
        """向左或右移动外星人."""
        self.x += (self.ai_settings.alien_speed_factor * 
                   self.ai_settings.fleet_direction)
        self.rect.x = self.x        

    def check_edges(self):
        """若外星人抵达屏幕(左右)边界, reture True."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True