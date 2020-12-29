import pygame
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.init()
screen_size = (900, 900)
screen = pygame.display.set_mode(screen_size)
FPS = 50


tile_images = {
    'A': load_image('A.png'),
    'P': load_image('P.png'),
    'I': load_image('I.png'),
    'R': load_image('R.png'),
    'T': load_image('T.png')
}
block_images = [load_image('Block.png'), load_image('Wall.png'), load_image('Gun.png'), load_image('Grade.png')
    , load_image('Cristal.png')]
player_image = load_image('Glaider2.png')

tile_width = 30
tile_height = 30


class Board:
    def __init__(self, filename):
        filename = "data/" + filename
        refract = {'A': 1, 'I':-1, 'T':-1, 'P': 0, 'R': 0}
        with open(filename, 'r') as mapFile:
            self.level_map = [line.strip() for line in mapFile]
        self.hg_map = [[refract[x] for x in line] for line in level_map]


class SpriteGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        print(0)
        pass


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(sprite_group)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(hero_group)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.pos = (pos_x, pos_y)

    def move(self, x, y):
        self.pos = (x, y)
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)

    def put_cristal(self):
        pass

    def put_block(self):
        pass

    def delete(self):
        pass


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(blocks_group)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.contact = True
        self.helth = 4
        self.pos = (pos_x, pos_y)
        self.job = 1
        self.update()

    def update(self):
        self.image = block_images[self.job]
        if self.job == 2:
            self.helth = 8
            self.contact = False
        else:
            self.helth = 4


player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
blocks_group = SpriteGroup()
enemy_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["", "",
                  "",
                  ""]

    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):

            Tile(level[y][x], x, y)
    new_player = Player(0, 0)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def move(hero, movement):
    x, y = hero.pos
    if movement == 'up' and y > 0:
        hero.move(x, y - 1)
    elif movement == 'down' and y < max_y:
        hero.move(x, y + 1)
    elif movement == 'left' and x > 0:
        hero.move(x - 1, y)
    elif movement == 'right' and x < max_x:
        hero.move(x + 1, y)


if __name__ == '__main__':
    board = Board('map.map')
    start_screen()
    level_map = load_level('map.map')
    hero, max_x, max_y = generate_level(level_map)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    move(hero, 'up')
                elif event.key == pygame.K_s:
                    move(hero, 'down')
                elif event.key == pygame.K_a:
                    move(hero, 'left')
                elif event.key == pygame.K_d:
                    move(hero, 'right')
                elif event.key == pygame.K_SPACE:
                    hero.delete()
                elif event.key == pygame.K_e:
                    hero.put_block()
                elif event.key == pygame.K_q:
                    hero.put_cristal()
            for enem in
        screen.fill(pygame.Color('black'))
        sprite_group.draw(screen)
        hero_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()