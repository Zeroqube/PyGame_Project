import pygame
import os
import sys
import random

def load_image(name, colorkey=None):
    fullname = os.path.join('Picturs', name)
    fullname = os.path.join('data', fullname)

    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


pygame.init()
screen_size = (720, 600)
screen = pygame.display.set_mode(screen_size)
FPS = 30
HP = load_image('HP.png')
bulet_image = load_image('Bulet.png')
tile_images = {
    'A': load_image('A.png'),
    'P': load_image('P.png'),
    'I': load_image('I.png'),
    'R': load_image('R.png'),
    'T': load_image('T.png')
}
block_images = [load_image('Block.png'), load_image('Cristal.png'), load_image('Wall.png'), load_image('Gun.png'),
                load_image('Grade.png')]
player_image = load_image('Glaider3.png')

tile_width = 30
tile_height = 30


class Enemy_1(pygame.sprite.Sprite):
    def __init__(self, x, y, helth):
        self.helth = helth
        self.pos = (x, y)
        super().__init__(enemy_group)
        self.image = load_image('Enemy1.png')
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)
        if -2 < board.pos[0] - self.pos[0] < 2 and -2 < board.pos[1] - self.pos[1] < 2:
            self.suicide()

    def act(self):
        self.move(board.enemy_map[self.pos[1]][self.pos[0]])
        if -2 < board.pos[0] - self.pos[0] < 2 and -2 < board.pos[1] - self.pos[1] < 2:
            self.suicide()

    def move(self, side):
        if side == 's':
            self.move(self.find())
        if side == 'u':
            if board.map[self.pos[0]][self.pos[1] - 1] != 0:
                board.map[self.pos[0]][self.pos[1] - 1].die()
            board.map[self.pos[0]][self.pos[1] - 1] = Enemy_1(self.pos[0], self.pos[1] - 1, self.helth)
            self.kill()
        if side == 'd':
            if board.map[self.pos[0]][self.pos[1] + 1] != 0:
                board.map[self.pos[0]][self.pos[1] + 1].die()
            board.map[self.pos[0]][self.pos[1] + 1] = Enemy_1(self.pos[0], self.pos[1] + 1, self.helth)
            self.kill()
        if side == 'l':
            if board.map[self.pos[0] - 1][self.pos[1]] != 0:
                board.map[self.pos[0] - 1][self.pos[1]].die()
            board.map[self.pos[0] - 1][self.pos[1]] = Enemy_1(self.pos[0] - 1, self.pos[1], self.helth)
            self.kill()
        if side == 'r':
            if board.map[self.pos[0] + 1][self.pos[1]] != 0:
                board.map[self.pos[0] + 1][self.pos[1]].die()
            board.map[self.pos[0] + 1][self.pos[1]] = Enemy_1(self.pos[0] + 1, self.pos[1], self.helth)
            self.kill()

    def suicide(self):
        board.helth -= 1
        board.win_score += 10
        self.kill()

    def kill(self):
        super().kill()
        board.map[self.pos[0]][self.pos[1]] = 0

    def find(self):
        for x in range(-1, 2):
            for y in range(-1, 2):
                try:
                    side = board.enemy_map[self.pos[1] + x][self.pos[0] + y]
                except Exception:
                    side = '0'
                if side != '0':
                    return side

resurs_image = load_image('Resurse.png')


class Resurs(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.pos = (x, y)
        super().__init__(sprite_group)
        self.image = resurs_image
        self.rect = self.image.get_rect().move(
            tile_width * x, tile_height * y)

    def kill(self):
        super().kill()
        board.score += 1
        board.map[self.pos[0]][self.pos[1]] = 0

    def die(self):
        super().kill()
        board.map[self.pos[0]][self.pos[1]] = 0


class Produser:
    def __init__(self, x, y):
        self.pos = (x, y)

    def produse(self):
        for pos in ((-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)):
            if not board.map[self.pos[0] + pos[0]][self.pos[1] + pos[1]]:
                board.map[self.pos[0] + pos[0]][self.pos[1] + pos[1]] = Resurs(self.pos[0] + pos[0], self.pos[1] + pos[1])
                break


class Board:
    def __init__(self, filename):
        self.pos = (-1, -1)
        self.score = 20
        self.helth = 50
        self.win_score = 100
        self.produsers = []
        filename1 = "data/levels/" + filename + '/' + filename + '.map'
        refract = {'A': 1, 'I':-1, 'T':-1, 'P': 0, 'R': 0}
        with open(filename1, 'r') as mapFile:
            self.level_map = [line.strip() for line in mapFile]
        self.hg_map = [[refract[x] for x in line] for line in self.level_map]
        filename2 = "data/levels/" + filename + '/' + 'enemy.map'
        with open(filename2, 'r') as mapFile:
            self.enemy_map = [line.strip() for line in mapFile]
        for y in range(len(self.level_map)):
            for x in range(len(self.level_map[y])):
                print(x, y, self.level_map[y][x])
                if self.level_map[y][x] == 'I':
                    self.produsers.append(Produser(x, y))
                elif self.level_map[y][x] == 'T':
                    self.pos = (x, y)

        self.map = [[0] * len(self.level_map) for i in range(len(self.level_map[0]))]

    def produce(self):
        for producer in self.produsers:
            producer.produse()

    def rebuild(self, x, y):
        hg = self.hg_map[y][x]
        for cur_sprite in blocks_group.sprites():
            p_x, p_y = cur_sprite.pos
            if hg == self.hg_map[p_y][p_x]:
                cur_sprite.nule()
        for structure in range(1, 9):
            for cur_sprite in blocks_group.sprites():
                p_x, p_y = cur_sprite.pos
                if hg == self.hg_map[p_y][p_x]:
                    cur_sprite.compare(structure)

    def act(self):
        for cur_sprite in blocks_group.sprites():
            cur_sprite.act()
        for cur_sprite in bulets_group.sprites():
            t = clock.tick()
            cur_sprite.move(t)
        for cur_sprite in enemy_group.sprites():
            cur_sprite.act()


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
        x, y = self.pos
        if not board.map[x][y] and board.hg_map[y][x] != -1 and board.score > 8:
            board.map[x][y] = Block(x, y, 1)

    def put_block(self):
        x, y = self.pos
        if not board.map[x][y] and board.hg_map[y][x] != -1 and board.score > 0:
            board.map[x][y] = Block(x, y, 0)

    def delete(self):
        x, y = self.pos
        if board.map[x][y] != 0:
            board.map[x][y].kill()


class Bulet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, v_x, v_y, damege, rang):
        super(Bulet, self).__init__(bulets_group)
        self.pos = (pos_x * tile_height, pos_y * tile_width)
        self.st = self.pos
        self.range = rang
        self.velosity = (v_x, v_y)
        self.damege = damege
        self.image = bulet_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)

    def move(self, t):
        self.pos = (self.pos[0] + self.velosity[0] * t, self.pos[1] + self.velosity[1] * t)
        self.rect = self.image.get_rect().move(self.pos[0], self.pos[1])
        if ((self.pos[0] - self.st[0]) ** 2 + (self.pos[1] - self.st[1]) ** 2) ** 0.5 > self.range:
            self.kill()

    def attac(self):
        if type(board.map[self.pos[0] // tile_height][self.pos[1] // tile_height]).__name__ == 'Enemy_1':
            board.map[self.pos[0] // tile_height][self.pos[1] // tile_height].helth -= self.damege
            self.kill()


class Block(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, cry):
        super().__init__(blocks_group)
        self.image = block_images[cry]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.helth = 4
        self.pos = (pos_x, pos_y)
        self.job = cry

        self.used = False
        self.using = False
        self.chids = []
        self.mode = 0
        self.type = 0

        self.user = self.pos
        if self.job == 1:
            board.score -= 9
        else:
            board.score -= 1

        board.rebuild(*self.pos)

    def nule(self):
        self.used = False
        self.using = False
        self.chids = []
        self.mode = 0
        self.type = 0

    def kill(self):
        super().kill()
        if self.used:
            board.rebuild(*self.pos)

        if self.job == 1:
            board.score += 9
        else:
            board.score += 1
        board.map[self.pos[0]][self.pos[1]] = 0

    def die(self):
        super().kill()
        if self.used:
            board.rebuild()
        board.map[self.pos[0]][self.pos[1]] = 0

    def act(self):
        if self.using:
            if self.type == 1:
                self.collect()
            elif self.type == 2:
                self.shoot()

    def collect(self):
        flag = False
        for i in range(-5, 6):
            for j in range(-5, 6):
                if type(board.map[self.pos[0] + i][self.pos[1] + j]).__name__ == 'Resurs':
                    board.map[self.pos[0] + i][self.pos[1] + j].kill()
                    flag = True
                    break
            if flag:
                break

    def compare(self, structure):
        for i in range(8):
            #for block in blueprint[structure][i]:
            pass


    def shoot(self):
        pass



player = None
running = True
clock = pygame.time.Clock()
sprite_group = SpriteGroup()
hero_group = SpriteGroup()
blocks_group = SpriteGroup()
enemy_group = SpriteGroup()
bulets_group = SpriteGroup()


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Приветствуем пилот глайдера!",
                  "Твоя задача собрать достаточное количество ресурсов, что-бы покинуть планету",
                  "К нашей территории подступают враги, не дай им уничтожить станцию",
                  "Мы не сможем покинуть планету пока станция повреждена",
                  "Придётся накопить на 10 единиц ресурсов больше, за каждую поломку",
                  "Удачи пилот!"]

    fon = pygame.transform.scale(load_image('fon.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 26)
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
    filename = "data/levels/" + filename + '/' + filename + '.map'
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
    new_player = Player(10, 10)
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
    c = 0
    board = Board('1')
    start_screen()
    level_map = load_level('1')
    hero, max_x, max_y = generate_level(level_map)
    flag_q = False
    flag_e = False
    flag_space = False
    board.map[19][7] = Enemy_1(19, 7, 5)
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
                    flag_space = True
                elif event.key == pygame.K_e:
                    flag_e = True
                elif event.key == pygame.K_q:
                    flag_q = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    flag_space = False
                elif event.key == pygame.K_e:
                    flag_e = False
                elif event.key == pygame.K_q:
                    flag_q = False
            if flag_space:
                hero.delete()
            elif flag_e:
                hero.put_block()
            elif flag_q:
                hero.put_cristal()
        c += 1
        if c % (FPS * 2) == 0:
            board.produce()
            board.act()

        screen.fill(pygame.Color('black'))
        sprite_group.draw(screen)
        blocks_group.draw(screen)
        enemy_group.draw(screen)
        hero_group.draw(screen)

        f2 = pygame.font.SysFont("serif", 20)
        text2 = f2.render(f"{board.score} / {board.win_score}", True, ("WHITE"))
        screen.blit(text2, (650, 50)), screen.blit(resurs_image, (600, 50))

        # Кол-во хп города
        f3 = pygame.font.SysFont("serif", 20)
        text3 = f3.render(f"{board.helth} / 50", True, ("WHITE"))
        screen.blit(text3, (650, 10)), screen.blit(HP, (600, 0))

        clock.tick(FPS)
        pygame.display.flip()
    pygame.quit()