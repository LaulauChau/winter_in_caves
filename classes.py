from game import *


# Classe personnage
class Character(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.shoot_cooldown = 0
        self.health = 0.5
        self.max_health = self.health
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # Charge les images pour le personnage
        animation_types = ['idle', 'run', 'jump', 'death']
        for animation in animation_types:
            # Reset liste temporaire
            temp_list = []
            # Compte nombre d'image dans le dossier
            num_of_frames = len(os.listdir(f'img/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'img/{self.char_type}/{animation}/{i}.png').convert_alpha()
                img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.update_animation()
        self.check_alive()
        # update cooldown
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def move(self, move_left, move_right):
        # Reset variable mouvement
        dx = 0
        dy = 0
        # Affecte les variables en fonction de l'action
        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1
        if self.jump is True and self.in_air is False:
            self.vel_y = -11
            self.jump = False
            self.in_air = True
        # Applique la gravité
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        # Verifie collision avec le sol
        if self.rect.bottom + dy > 900:
            dy = 900 - self.rect.bottom
            self.in_air = False
        # Update hitbox
        self.rect.x += dx
        self.rect.y += dy

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 20
            rock = Rock(self.rect.centerx + (0.7 * self.rect.size[0] * self.direction), self.rect.centery, self.direction)
            rock_groupe.add(rock)

    def update_animation(self):
        # Update animation
        ANIMATION_COOLDOWN = 100
        self.image = self.animation_list[self.action][self.frame_index]
        # Verifie temps passe entre chaque update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        # Boucle les animations
        if self.frame_index >= len(self.animation_list[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation_list[self.action]) - 1
            else:
                self.frame_index = 0

    def update_action(self, new_action):
        # Verifie si nouvelle action != action a l'ecran
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)  # 3 = death

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


# Initialise les classes
player = Character('player', 200, 200, 0.5, 5)
enemy = Character('enemy', 400, 800, 0.5, 5)


# Structures pierre (projectile)
class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = rock_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction

    def update(self):
        # bouger la pierre
        self.rect.x += (self.direction * self.speed)
        # verifie si la pierre sort de l'ecran
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()
        # verifie collision avec les personnages
        if pygame.sprite.spritecollide(player, rock_groupe, False):
            if player.alive:
                player.health -= 0.1
                self.kill()
        if pygame.sprite.spritecollide(enemy, rock_groupe, False):
            if enemy.alive:
                enemy.health -= 0.1
                self.kill()

