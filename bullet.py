import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship."""

    def __init__(self, ai_settings, screen, ship):
        """在飞船当前位置创建一个bullet object."""
        super().__init__()
        self.screen = screen

        # 在(0, 0)处创建一个 bullet rect,然后将其放在正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width,
                                    ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # 将子弹的位置存储为小数值
        self.y = float(self.rect.y)

        self.blt_color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """向上移动子弹."""
        # 更新子弹的小数值位置坐标.
        self.y -= self.speed_factor
        # 更新 rect 的位置.
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        # 注意此处用的pygame.draw.rect(), 不是blit()函数
        pygame.draw.rect(self.screen, self.blt_color, self.rect)