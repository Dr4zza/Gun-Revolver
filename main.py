import pygame
from sys import exit
import player
import random
import particlepy

bullets = []
enemy_bullets = []
enemies = []
bulletleft = 100
ammo = []
t = 0
t2 = 0
t3 = 0
t4 = 0
enemy_spawn = 80
bullet_rate = 70
reload_spawn = 100

while True:
#   the part of the code that allows you to quit the game
    if player.game_active == True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
            elif player.player_health == -15:
                player.game_active = False
                bulletleft = 100
                player.player_health = 10
                bullets = []
                enemy_bullets = []
                enemies = []
                ammo = []
                player.player_rect.center = (200,300)
            
            elif bulletleft == 0:
                player.game_active = False
                bulletleft = 100
                player.player_health = 10
                bullets = []
                enemy_bullets = []
                enemies = []
                ammo = []
                player.player_rect.center = (200,300)

            if event.type == pygame.MOUSEBUTTONDOWN:
                if player.gun_inactive == False:
                    if bulletleft > 0:
                        pos = (player.player_rect.centerx,player.player_rect.centery)
                        bullets.append(player.Bullet(*pos))
                        bulletleft -= 1
                    player.shot = True
                if player.player_rect.collidepoint(event.pos):
                    player.moving = True

                
            elif event.type == pygame.MOUSEBUTTONUP:
                if player.player_rect.collidepoint(event.pos):
                    player.moving = False

                elif not player.player_rect.collidepoint(event.pos):
                    player.moving = False

            elif event.type == pygame.MOUSEMOTION and player.moving:
                player.player_gravity = 0
                player.player_rect.move_ip(event.rel)
            
        for bullet in bullets[:]:
            player.Bullet.update(bullet)
            angle = player.gun.gunrotate()
            if angle < 360 and angle > 180:
                player.player_gravity = 0
            else:
                player.player_gravity = 1
            direction = player.Bullet.update(bullet)

            player.player_rect.x += (direction[0]*-1)*5.5
            player.player_gravity -= direction[1]*10
            player.Player.playergravity()
            player.screen.blit(player.player_surf,player.player_rect)

            if not player.screen.get_rect().collidepoint(bullet.pos):
                bullets.remove(bullet)
            elif bullet.pos[1] > 550:
                bullets.remove(bullet)

        dt = player.clock.tick()
        t += dt
        t2 += dt
        t3 += dt
        t4 += dt

        text_surface = player.text_font.render(str(bulletleft) ,False, "Green")
        score_surface = player.text_font.render(str(player.score), False, "Black")
        rotated_bullet = pygame.transform.rotate(player.bullet_surf, 90)

        player.gun_rect.x = player.player_rect.x - 100
        player.gun_rect.y = player.player_rect.y    

        player.screen.blit(player.sky_surface,(0,0))
        player.screen.blit(player.ground_surface,(0,550))
        player.screen.blit(player.player_surf, player.player_rect)

        if len(str(bulletleft)) == 1:
            player.screen.blit(text_surface, (970,4))
            player.screen.blit(rotated_bullet, (947,4))
        elif len(str(bulletleft)) == 2:
            player.screen.blit(text_surface, (963,4))
            player.screen.blit(rotated_bullet, (940,4))
        elif len(str(bulletleft)) == 3:
            player.screen.blit(text_surface, (950,4))
            player.screen.blit(rotated_bullet, (927,4))

        player.screen.blit(score_surface,(500,4))

        if player.score >= 250:
            reload_spawn = 50
            enemy_spawn = 65
            bullet_rate = 55

        if t > reload_spawn:
            postion = (random.randrange(1,1000), random.randrange(1,570))
            ammo.append(postion)
            t = 0

        if t3 > enemy_spawn:
            if len(enemies) < 10:
                pos3 = (random.randrange(10,991), 560)
                enemies.append(player.Enemy(*pos3))
                t3 = 0 
                
        if t2 > bullet_rate and len(enemies) != 0:
            for enemy in enemies:
                pos2 = (enemy.rect.centerx, enemy.rect.centery)
                enemy_bullets.append(player.EnemyBullet(*pos2))
                t2 = 0

        if t4 > 45:
            player.score += 1
            t4 = 0

        for bullet2 in enemy_bullets[:]:
            player.EnemyBullet.update(bullet2)
            if player.player_rect.collidepoint(bullet2.pos):
                if player.player_health > -15:
                    player.player_health -= 1
                enemy_bullets.remove(bullet2)

        for bullet2 in enemy_bullets:
            player.EnemyBullet.draw(bullet2, player.screen)

        for enemy in enemies[:]:
            player.Enemy.update(enemy)
            for bullet in bullets:
                if enemy.rect.colliderect(bullet.rect):
                    bullets.remove(bullet)
                    enemy.life -= 1

        for enemy in enemies:
            if enemy.life == 0 and len(enemies) > 0:
                enemies.remove(enemy)
                player.score += 10
            player.Enemy.draw(enemy, player.screen)
            player.Enemy.gunrotate_enemy(enemy)

        for ammos in ammo[:]:
            reload_rect = player.reload_surf.get_rect(center = ammos)
            if player.player_rect.colliderect(reload_rect):
                bulletleft += 5
                ammo.remove(ammos)

        for ammos in ammo:
            player.screen.blit(player.reload_surf, ammos)
            if len(ammo) != 1:
                ammo.remove(ammos)

        for bullet in bullets:
            player.Bullet.draw(bullet,player.screen)

        player.Player.playergravity()
        player.Player.playerfriction()
        player.Player.healthbar()
        player.gun.gunrotate()
        player.Enemy.data()
        pygame.display.update()
        player.clock.tick(60)

    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit()
                exit()
        
        Menu = player.menu()
        pygame.display.update()
        player.clock.tick(60)