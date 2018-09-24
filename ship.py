import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        """初始化飞船并设置其初始位置."""
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载飞船图象并获取其外接矩形.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # 每艘飞船初始位置为屏幕底部中央.
        # centerx只存储整数部分
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center.
        #飞船有center属性,外星人没有?
        self.center = float(self.rect.centerx)

        # 移动 flags 取决于 event.type
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """根据flags更新飞船位置."""
        # 更新飞船的 center 值, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center.
        self.rect.centerx = self.center

    def blitme(self):
        """Draw the ship at its current location.
        在指定位置绘制飞船.
        """
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """将飞船置于屏幕底部中央"""
        self.center = self.screen_rect.centerx