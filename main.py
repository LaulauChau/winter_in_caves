from classes import *


# Remplis le fond d'ecran
def draw_background():
    screen.fill(BACKGROUND)
    pygame.draw.line(screen, RED, (0, 900), (SCREEN_WIDTH, 900))


# Boucle de jeu
run = True
while run:
    clock.tick(FPS)

    draw_background()

    player.update()
    player.draw()

    enemy.update()
    enemy.draw()

    rock_groupe.update()
    rock_groupe.draw(screen)

    # Update action joueur
    if player.alive:
        if shoot:
            player.shoot()
        if player.in_air:
            player.update_action(2)  # 2 = jump
        elif moving_left or moving_right:
            player.update_action(1)  # 1 = run
        else:
            player.update_action(0)  # 0 = idle
        player.move(moving_left, moving_right)

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
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_SPACE:
                shoot = False

    pygame.display.update()

pygame.quit()
