from classes import *


# Remplis le fond d'ecran
def draw_background():
    screen.fill(BACKGROUND)
    width = sky.get_width()
    for x in range(8):
        # screen.blit(background, ((x * width) - scroll, 0))
        screen.blit(sky, ((x * width) - bg_scroll * 0.5, 0))
        screen.blit(rocks, ((x * width) - bg_scroll * 0.55, 0))
        screen.blit(clouds_1, ((x * width) - bg_scroll * 0.60, 0))
        screen.blit(clouds_2, ((x * width) - bg_scroll * 0.65, 0))
        screen.blit(ground_1, ((x * width) - bg_scroll * 0.70, 0))
        screen.blit(ground_2, ((x * width) - bg_scroll * 0.75, 0))
        screen.blit(ground_3, ((x * width) - bg_scroll * 0.8, 0))


# Boucle de jeu
run = True
while run:
    clock.tick(FPS)

    draw_background()
    world.draw()
    health_bar.draw(player.health)
    player.update()
    player.draw()

    for enemy in enemy_group:
        enemy.ai()
        enemy.update()
        enemy.draw()

    rock_groupe.update()
    rock_groupe.draw(screen)
    projectile_groupe.update()
    projectile_groupe.draw(screen)
    water_group.update()
    water_group.draw(screen)
    exit_group.update()
    exit_group.draw(screen)

    # Update action joueur
    if player.alive:
        if shoot:
            player.shoot()
        elif projectile and projectile_thrown is False:
            projectile = Projectile(player.rect.centerx + (0.75 * player.rect.size[0] * player.direction), player.rect.top, player.direction)
            projectile_groupe.add(projectile)
            projectile_thrown = True
        if player.in_air:
            player.update_action(2)  # 2 = jump
        elif moving_left or moving_right:
            player.update_action(1)  # 1 = run
        else:
            player.update_action(0)  # 0 = idle

        screen_scroll = player.move(moving_left, moving_right)
        print(screen_scroll)
        bg_scroll -= screen_scroll

    for event in pygame.event.get():
        # Quitter le jeu
        if event.type == pygame.QUIT:
            run = False
        # Clavier
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_z and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_a:
                projectile = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_a:
                projectile = False
                projectile_thrown = False

    pygame.display.update()

pygame.quit()
