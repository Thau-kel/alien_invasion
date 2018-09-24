import sys
from time import sleep

import pygame

from alien import Alien
from bullet import Bullet


def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """响应按下键盘的事件."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    """未达限制数量则发射子弹."""
    # 创建一颗新子弹并将其加入子弹编组, add() 方法.
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)    

def check_keyup_events(event, ship):
    """响应按键松开的事件."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets):
    """响应按键以及鼠标事件."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # 获取鼠标光标位置坐标, 这几个语句块顺序有问题???
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
            ship, aliens, bullets, mouse_x, mouse_y)            

def check_play_button(
        ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets, mouse_x, mouse_y):
    # 当玩家点击 PLAY 按钮时开始一局新游戏
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    # 两个条件(按钮被点击, 游戏处于非活动状态)均满足时才开始新游戏
    if button_clicked and not stats.game_active:
        # 重置 游戏设置
        ai_settings.initialize_dynamic_settings()
        
        # 隐藏鼠标光标
        pygame.mouse.set_visible(False)

        # 重置 游戏统计数据
        stats.reset_stats()
        stats.game_active = True

        # 重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # 清空外星人和子弹
        aliens.empty()
        bullets.empty()

        # 新建一支舰队并使飞船重新居中
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, 
        play_button):
    """Update images on the screen and flip to the new screen. 
    更新屏幕上的图像, 并切换到新屏幕.
    """
    # 每次循环都重绘屏幕.
    screen.fill(ai_settings.bg_color)

    # 在飞船及外星人之后重绘所有子弹???
    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)

    # 显示得分信息
    sb.show_score()

    # 若游戏处于非活动状态, 则绘制 Play按钮
    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
        """更新子弹的位置并删除已越屏幕上边界的子弹."""
        bullets.update()

        # 删除已消失的子弹, for语句对副本进行操作
        for bullet in bullets.copy():
            if bullet.rect.bottom <= 0:
                bullets.remove(bullet)

        check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, 
                                      aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, 
                                   ship, aliens, bullets):    
    """响应子弹和外星人之间的碰撞"""
    # 删除发生碰撞的子弹和外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # 一支舰队被全灭后, 就提升一个等级
        bullets.empty()
        ai_settings.increase_speed()

        # 提升等级
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)

def get_number_alien_x(ai_settings, alien_width):
    """计算一行能容纳的外星人的数量"""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """计算屏幕能容纳的外星人行数."""
    available_space_y = (ai_settings.screen_height
                         - 3 * alien_height
                         - ship_height)
    number_rows = int(available_space_y /  (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    # 创建一个外星人并将其放在当前行. 按顺序计算坐标???
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """创建一支外星人舰队."""
    # 创建一个外星人并计算一行可容纳外星人的数量, 注意实参的传递
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alien_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
                                  alien.rect.height)

    # 创建外星人舰队
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                         row_number)

def check_fleet_edges(ai_settings, aliens):
    """响应任何外星人触及屏幕(左右)边界的事件."""
    for alien in aliens.sprites():
        if alien.check_edges():   
            change_fleet_direction(ai_settings, aliens)     
            break     

def change_fleet_direction(ai_settings,aliens):
    """让整个舰队下降并改变其水平运动方向(左右)."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens,
                        bullets):
    """检查是否有外星人到达屏幕底部边界"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # 和飞船被撞一样反应
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """检查舰队是否达到某个边界, 若然, 则更新舰队所有外星人的位置."""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()        

    # 检查外星人与飞船的碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)

    # 检查是否有外星人到达屏幕底端
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """响应飞船与外星人之间的碰撞"""
    if stats.ships_left > 0:
        # 减少可用飞船的数量
        stats.ships_left -= 1

        # 更新记分牌
        sb.prep_ships()

        # 清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        # 创建一支新舰队并将飞船重置于屏幕底部中央
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # 暂停
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_high_score(stats, sb):
    """检查是否有新最高分纪录出现"""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()