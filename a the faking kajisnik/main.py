import pygame
import time as t

clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((870, 273))
pygame.display.set_caption('a the faking kajisnik')
icon = pygame.image.load('img/icon.jpg')
pygame.display.set_icon(icon)

kajisnik = pygame.image.load('img/kajisnik_1.png')
kajisnik = pygame.transform.scale(kajisnik, (300, 300))

pig = pygame.image.load('img/pig.png')
pig = pygame.transform.scale(pig, (100, 100))
pig_x = 900
pig_list_in_game = []

walk = [
    pygame.transform.scale(pygame.image.load('img/kajisnik_1.png'), (300, 300)),
    pygame.transform.scale(pygame.image.load('img/kajisnik_2.png'), (300, 300)),
    pygame.transform.scale(pygame.image.load('img/kajisnik_3.png'), (300, 300))
]


player_x = 0
player_y = 0
is_jump = False
jump_count = 8
player_anim_count = 0


bg_1 = pygame.image.load('img/background_pole.jpg')
bg_x = 0

player_speed = 12

gameplay = True

label = pygame.font.Font('font/kajisnik_font.otf', 60)
lose_label = label.render('Тебя сожрали....', False, 'red')
restart_label = label.render('Попытаться ещё раз....', False, 'green')
restart_label_rect = restart_label.get_rect(topleft=(100, 200))

run_game = True
bg_sound = pygame.mixer.Sound('sound/background_music_1.mp3')
bg_sound.set_volume(0.04)
ms_play = bg_sound.play(-1)

pig_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pig_timer, 3000)

bullet = pygame.image.load('img/poop.png')
bullet = pygame.transform.scale(bullet, (30, 30))
bullets = []


sound_played = False

while run_game:
    screen.blit(bg_1, (bg_x, 0))

    player_rect = walk[0].get_rect(topleft=(player_x, player_y))

    if gameplay:

        if pig_list_in_game:
            for (i, el) in enumerate (pig_list_in_game):
                screen.blit(pig, el)
                el.x -= 10

                if el.x < -10:
                    pig_list_in_game.pop(i)

                if player_rect.colliderect(el):
                    gameplay = False

        keys = pygame.key.get_pressed()


        if keys[pygame.K_a] and player_x > 0:
            player_x -= player_speed
            anim_rect = walk[player_anim_count].get_rect(center=(player_x + kajisnik.get_width() // 2, player_y + kajisnik.get_height() // 2))
            screen.blit(walk[player_anim_count], anim_rect)
            if player_anim_count == 2:
                player_anim_count = 0
            else:
                player_anim_count += 1
        elif keys[pygame.K_d] and player_x < 600:
            player_x += player_speed
            anim_rect = walk[player_anim_count].get_rect(center=(player_x + kajisnik.get_width() // 2, player_y + kajisnik.get_height() // 2))
            screen.blit(walk[player_anim_count], anim_rect)
            if player_anim_count == 2:
                player_anim_count = 0
            else:
                player_anim_count += 1
        else:
            anim_rect = kajisnik.get_rect(center=(player_x + kajisnik.get_width() // 2, player_y + kajisnik.get_height() // 2))
            screen.blit(kajisnik, anim_rect)


        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_count >= -8:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 8

                
    else:
        screen.fill('blue')
        screen.blit(lose_label, (200, 120))
        screen.blit(restart_label, restart_label_rect)
        if not sound_played:
            screem = pygame.mixer.Sound('sound/pig.wav')
            screem.set_volume(0.2)
            play_screem = screem.play()
            sound_played = True
            sound_played = False
            bullets.clear()

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
                gameplay = True
                player_x =  0
                pig_list_in_game.clear()


    if keys[pygame.K_r]:
        bullets.append(bullet.get_rect(topleft=(player_x + 100, player_y + 200)))
        poop_sound_fx = pygame.mixer.Sound('sound/poop.wav')
        poop_sound_fx.set_volume(0.3)
        poop_sound_fx.play()

    if bullets:
        for el in bullets:
            screen.blit(bullet, el)
            el.x += 40

            if el.x > 2000:
                bullets.pop()

            if pig_list_in_game:
                for (index, svin) in enumerate(pig_list_in_game):
                    if el.colliderect(svin):
                        pig_list_in_game.pop(index)
                        bullets.pop(index)
                        pig_dead_sound_fx = pygame.mixer.Sound('sound/pig_dead_sound.wav')
                        pig_dead_sound_fx.set_volume(0.1)
                        pig_dead_sound_fx.play()
  


    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
            pygame.quit()

        if event.type == pig_timer:
            pig_list_in_game.append(pig.get_rect(topleft=(900, 160)))

    clock.tick(12)
