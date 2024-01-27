import datetime
import os
import platform
import random
import sys
import time

import pygame
import pygame.mixer
import pygame_gui
from pygame_gui.elements import UIButton

pygame.init()
pygame.mixer.init()

background_music = pygame.mixer.Sound(os.path.join('data', "4-9-18 idk.mp3 2019.mp3"))
background_music.play(loops=-1)

FPS = 30

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
bombs_group = pygame.sprite.Group()
booms_group = pygame.sprite.Group()
walls_group = pygame.sprite.Group()


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {'wall': load_image('img.png'), 'empty': load_image('img_1.png')}
player_image = load_image('hero.png')
enemy_image = load_image('enemy.png')
bomb_image = load_image('bomb.png')
wall_image = load_image('img.png')
boom_image = load_image('boom.png')
enemy_dead_image = load_image('dead.png')
walls = []

tile_width = tile_height = 100


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                walls_group.add(Wall(x, y))
                walls.append(Wall(x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                if 0 <= x < len(level[y]) and 0 <= y < len(level):
                    Tile('empty', x, y)
                    new_enemy = Enemy(x, y, new_player)
                    enemies_group.add(new_enemy)
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def levels_screen():
    level = "map1.txt"
    SCREEN_WIDTH, SCREEN_HEIGHT = (18 + 1) * tile_width, (19 + 1) * tile_width
    fon = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))

    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    level_1_button = UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 150), (300, 100)),
        text='Level 1',
        manager=manager)

    level_2_button = UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (300, 100)),
                              text='Level 2',
                              manager=manager)

    level_3_button = UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150), (300, 100)),
        text='Level 3',
        manager=manager)

    back_button = UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                           text='Back',
                           manager=manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            manager.process_events(event)

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == level_1_button:
                    level = "map1.txt"
                    return level
                elif event.ui_element == level_2_button:
                    level = "map2.txt"
                    return level
                elif event.ui_element == level_3_button:
                    level = "map3.txt"
                    return level
                elif event.ui_element == back_button:
                    return level

        manager.update(1 / FPS)
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        manager.draw_ui(screen)
        pygame.display.flip()


def results_screen():
    SCREEN_WIDTH, SCREEN_HEIGHT = (18 + 1) * tile_width, (19 + 1) * tile_height
    screen.fill(pygame.Color("gray"))

    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))


    file = open(file="results.txt", mode="r")
    results = file.read()
    file.close()

    font = pygame.font.SysFont("Arial", 30)
    text = font.render(results, True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()

    back_button = UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100), (300, 100)),
                           text='Back',
                           manager=manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            manager.process_events(event)

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    return

        manager.update(1 / FPS)
        manager.draw_ui(screen)
        pygame.display.flip()


def start_screen():
    SCREEN_WIDTH, SCREEN_HEIGHT = (18 + 1) * tile_width, (19 + 1) * tile_height
    level = "map1.txt"
    fon = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))

    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    start_button = UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100), (300, 100)),
                            text='Start Game',
                            manager=manager)

    levels_button = UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (300, 100)),
                             text='Levels',
                             manager=manager)

    results_button = UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100), (300, 100)),
        text='Results',
        manager=manager)

    exit_button = UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 200), (300, 100)),
                           text='Exit Game',
                           manager=manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            manager.process_events(event)

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return level
                elif event.ui_element == levels_button:
                    level = levels_screen()
                elif event.ui_element == results_button:
                    level = results_screen()
                elif event.ui_element == exit_button:
                    terminate()

        manager.update(1 / FPS)
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        manager.draw_ui(screen)
        pygame.display.flip()


def menu_screen():
    global level
    SCREEN_WIDTH, SCREEN_HEIGHT = (18 + 1) * tile_width, (19 + 1) * tile_height
    fon = pygame.transform.scale(load_image('fon.jpg'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(fon, (0, 0))

    manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))

    start_button = UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100), (300, 100)),
                            text='Return game',
                            manager=manager)

    levels_button = UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2), (300, 100)),
                             text='Return to Main Screen',
                             manager=manager)

    exit_button = UIButton(relative_rect=pygame.Rect((SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 100), (300, 100)),
                           text='Exit Game',
                           manager=manager)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            manager.process_events(event)

            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == start_button:
                    return
                elif event.ui_element == levels_button:
                    level = start_screen()
                    return level
                elif event.ui_element == exit_button:
                    terminate()

        manager.update(1 / FPS)
        screen.fill((0, 0, 0))
        screen.blit(fon, (0, 0))
        manager.draw_ui(screen)
        pygame.display.flip()


def draw_health_bar(player, screen):
    health_bar_width = 500
    health_bar_height = 20
    health_ratio = player.life / 100

    health_bar_x = SCREEN_WIDTH - health_bar_width - 10
    health_bar_y = SCREEN_HEIGHT - health_bar_height - 10

    health_bar_background_color = pygame.Color("gray")
    health_bar_foreground_color = pygame.Color("blue")

    pygame.draw.rect(screen, health_bar_background_color,
                     pygame.Rect(health_bar_x, health_bar_y, health_bar_width, health_bar_height))
    pygame.draw.rect(screen, health_bar_foreground_color,
                     pygame.Rect(health_bar_x, health_bar_y, health_bar_width * health_ratio, health_bar_height))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)


class Boom(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(booms_group, all_sprites)
        self.image = boom_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.duration = 2 * FPS
        self.frame = 0

    def update(self):
        self.duration -= 1
        if self.duration <= 0:
            self.kill()
        else:
            self.frame = (self.frame + 1) % 4
            self.image = pygame.transform.scale(boom_image, (60, 60))
            self.image.set_alpha(255 * (self.duration / (2 * FPS)))


class Bomb(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction):
        super().__init__(bombs_group, all_sprites)
        self.image = bomb_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.direction = direction
        self.speed = 7

    def move(self):
        dx, dy = self.direction
        self.rect.y += dy * self.speed
        self.collide(0, dy)

        self.rect.x += dx * self.speed
        self.collide(dx, 0)

    def collide(self, dx, dy):

        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                booms_group.add(Boom(self.rect.x // tile_width, self.rect.y // tile_height))
                self.kill()
                bomb_sound = pygame.mixer.Sound(
                    os.path.join("data", "Nuclear Bomb Explosion Sound Effect. (256  kbps).mp3"))
                bomb_sound.set_volume(0.3)
                bomb_sound.play(loops=0)
                return

        for enemy in enemies_group:
            current_time = pygame.time.get_ticks()
            if pygame.sprite.collide_rect(self, enemy):
                enemy.image = enemy_dead_image
                enemy.dead_time = current_time
                dead_sound = pygame.mixer.Sound(os.path.join("data", "lego-yoda-death-sound-effect.mp3"))
                dead_sound.play(loops=0)
                booms_group.add(Boom(self.rect.x // tile_width, self.rect.y // tile_height))
                self.kill()
                bomb_sound = pygame.mixer.Sound(
                    os.path.join("data", "Nuclear Bomb Explosion Sound Effect. (256  kbps).mp3"))
                bomb_sound.set_volume(0.3)
                bomb_sound.play(loops=0)
                return


class Wall(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemies_group, all_sprites)
        self.image = wall_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, player):
        super().__init__(enemies_group, all_sprites)
        self.image = enemy_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.dead_time = 0
        self.target = player
        self.speed = 3
        if level == "map3.txt":
            self.speed = 6
        self.last_enemy_damage_time = 0

    def move_towards_target(self):
        dx, dy = self.target.rect.x - self.rect.x, self.target.rect.y - self.rect.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance > 0:
            dx /= distance
            dy /= distance

        self.rect.x += dx * self.speed
        self.collide(0, dx)

        self.rect.y += dy * self.speed
        self.collide(dy, 0)

    def collide(self, dy, dx):
        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):
                if dx > 0:
                    self.rect.right = wall.rect.left
                if dx < 0:
                    self.rect.left = wall.rect.right
                if dy > 0:
                    self.rect.bottom = wall.rect.top
                if dy < 0:
                    self.rect.top = wall.rect.bottom
                return True

        for player in player_group:
            if pygame.sprite.collide_rect(self, player):
                if dx > 0:
                    self.rect.right = player.rect.left

                if dx < 0:
                    self.rect.left = player.rect.right

                if dy > 0:
                    self.rect.bottom = player.rect.top

                if dy < 0:
                    self.rect.top = player.rect.bottom

                current_time = pygame.time.get_ticks()
                if current_time - self.last_enemy_damage_time > 2000:
                    self.last_enemy_damage_time = current_time
                    player.life -= 10
                return True

        return False

    def update(self):
        if self.image == enemy_dead_image:
            current_time = pygame.time.get_ticks()
            if current_time - self.dead_time > 5000:
                for player in player_group:
                    player.killed += 1
                for i in range(2):
                    new_enemy_x = self.rect.x + random.choice([-25, 25])
                    new_enemy_y = self.rect.y + random.choice([-25, 25])
                    new_enemy = Enemy(new_enemy_x // tile_width, new_enemy_y // tile_height, player)
                    enemies_group.add(new_enemy)
                self.kill()

        else:
            self.move_towards_target()


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.life = 100
        self.last_enemy_damage_time = 0
        self.killed = 0

    def shoot_bomb(self):
        dx, dy = 0, 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1
        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1

        mag = (dx ** 2 + dy ** 2) ** 0.5
        if mag > 0:
            dx /= mag
            dy /= mag

        if dx == 0 and dy == 0:
            return

        bombs_group.add(Bomb(self.rect.x // tile_width, self.rect.y // tile_height, (dx, dy)))
        time.sleep(0.2)

    def update(self):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_UP]:
            dy -= 10
        if keys[pygame.K_DOWN]:
            dy += 10
        if keys[pygame.K_LEFT]:
            dx -= 10
        if keys[pygame.K_RIGHT]:
            dx += 10

        self.rect.y += dy
        self.collide(0, dy)

        self.rect.x += dx
        self.collide(dx, 0)

        for enemy in enemies_group:
            if pygame.sprite.collide_rect(self, enemy) and enemy.image != enemy_dead_image:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_enemy_damage_time > 2000:
                    self.last_enemy_damage_time = current_time
                    self.life -= 10

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.shoot_bomb()

    def collide(self, dx, dy):
        for wall in walls:
            if pygame.sprite.collide_rect(self, wall):

                if dx > 0:
                    self.rect.right = wall.rect.left

                if dx < 0:
                    self.rect.left = wall.rect.right

                if dy > 0:
                    self.rect.bottom = wall.rect.top

                if dy < 0:
                    self.rect.top = wall.rect.bottom

        for enemy in enemies_group:
            if pygame.sprite.collide_rect(self, enemy):
                if dx > 0:
                    self.rect.right = enemy.rect.left

                if dx < 0:
                    self.rect.left = enemy.rect.right

                if dy > 0:
                    self.rect.bottom = enemy.rect.top

                if dy < 0:
                    self.rect.top = enemy.rect.bottom


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - SCREEN_WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - SCREEN_HEIGHT // 2)


SCREEN_WIDTH, SCREEN_HEIGHT = (18 + 1) * tile_width, (19 + 1) * tile_width
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
camera = Camera()

level = start_screen()
running = True
player, map_x, map_y = generate_level(load_level(level))

manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
menu_button = UIButton(relative_rect=pygame.Rect((10, 10), (100, 50)),
                       text='Menu',
                       manager=manager)

while running:
    dt = clock.tick(FPS) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            terminate()
        manager.process_events(event)

        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == menu_button:
                menu_screen()

    player_group.update()
    enemies_group.update()
    bombs_group.update()
    booms_group.update()
    for bomb in bombs_group:
        bomb.move()
        if bomb.direction == (0, -1):
            for wall in walls:
                if pygame.sprite.collide_rect(bomb, wall):
                    booms_group.add(Boom(bomb.rect.x // tile_width, bomb.rect.y // tile_height))
                    bomb.kill()
                    break
    manager.update(dt)
    screen.fill(pygame.Color("black"))
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)

    all_sprites.draw(screen)
    player_group.draw(screen)
    booms_group.draw(screen)
    walls_group.draw(screen)
    enemies_group.draw(screen)
    draw_health_bar(player, screen)
    manager.draw_ui(screen)
    pygame.display.flip()

    if player.life <= 0:
        file = open(file="results.txt", mode="a+")
        file.write(f"{platform.node()} - {player.killed} {datetime.datetime.now().time()}" + "\n")
        file.close()
        screen.fill(pygame.Color("gray"))
        message = f"You killed {player.killed} enemies!"
        font = pygame.font.SysFont("Arial", 30)
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()

        time.sleep(5)
        all_sprites.empty()
        enemies_group.empty()
        player_group.empty()
        walls_group.empty()

        level = start_screen()
        walls = []
        player, map_x, map_y = generate_level(load_level(level))
        continue

pygame.quit()