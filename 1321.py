import os
import random
import pygame
import sys
pygame.init()
pygame.font.init()

FPS = 50
WIDTH = 500
HEIGHT = 500
STEP = 10
TILE_WIDTH = TILE_HEIGHT = 50
GRAVITY = 10



screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
box_group = pygame.sprite.Group()
money_group = pygame.sprite.Group()
box_black_group = pygame.sprite.Group()
nps_group = pygame.sprite.Group()
star_group = pygame.sprite.Group()
screen_rect = (0, 0, WIDTH, HEIGHT)



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image

def terminate():
    pygame.quit()
    sys.exit()

def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("freesansbold.ttf", 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
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
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


a = [['' for i in range(100)] for j in range(100)]

print(a)
for i in range(100):
    for j in range(100):
        chance = random.randint(0, 100)
        if chance < 20:
            a[i][j] = '#'
        else:
            a[i][j] = '.'

for i in range(100):
    a[0][i] = '$'
    a[99][i] = '$'
    a[i][0] = '$'
    a[i][99] = '$'

i = 0
while i < 50:
    chance2 = random.randint(0, 100)
    if chance2 < 50:
        x, y = random.randint(2, 97), random.randint(2, 97)
        while a[x][y] == '#' and a[x][y] != '@' and a[x][y] != '$' and a[x][y] != '?':
            x, y = random.randint(2, 97), random.randint(2, 97)
        a[x][y] = '*'
        i += 1



print(a)
x, y = random.randint(0, 100), random.randint(0, 100)
while a[x][y] == '#':
    x, y = random.randint(0, 100), random.randint(0, 100)
a[x][y] = '@'
cash_m = []

def generate_level(level):
    new_player = None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
                Tile('npc', x + 1, y + 1)
            elif level[y][x] == '*':
                Tile('empty', x, y)
                cash_m.append(Tile('cash', x, y))
            elif level[y][x] == '$':
                Tile('box_black', x, y)
            elif level[y][x] == '?':
                Tile('empty', x, y)
                Tile('npc', x, y)


    return new_player

def cvest_nps():
    chotchik = 0
    proverochra_na_petyxa = False

    if pygame.sprite.spritecollideany(player, nps_group):
        intro_text = ["КВЕСТ ПОЛУЧЕН", "------",
                        "СОБЕРИТЕ 50 МОНЕТ И ВАМ",
                        "ОТКРОЕТСЯ ТАЙНА МИРОЗДАНИЯ"]
        if pygame.sprite.spritecollideany(player, money_group) != None:
            chotchik += 1
            if chotchik == 50:
                proverochra_na_petyxa = True


        font = pygame.font.Font(None, 100)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)




tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'player': load_image('mario.png'),
    'cash': load_image('money.png'),
    'box_black': load_image('box_black.png'),
    'npc': load_image('npc.png'),
    'star': load_image('star.png')
}

class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        if tile_type == 'wall':
            super().__init__(tiles_group, box_group, all_sprites)
        elif tile_type == 'cash':
            super().__init__(money_group, all_sprites)
        elif tile_type == 'box_black':
            super().__init__(box_black_group, all_sprites, tiles_group)
        elif tile_type == 'npc':
            super().__init__(nps_group, all_sprites)
        elif tile_type == 'star':
            super().__init__(star_group, all_sprites)
        else:
            super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x,
                                               TILE_HEIGHT * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = tile_images['player']
        self.rect = self.image.get_rect().move(TILE_WIDTH * pos_x + 15,
                                               TILE_HEIGHT * pos_y + 5)

class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj): # перемещение любого спрайта
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target): # следит за персонажем
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


start_screen()

player = generate_level(a)
camera = Camera()

pressed_left = pressed_right = pressed_up = pressed_down = False
running = True
screen1 = pygame.transform.scale(load_image('grass.png'), (WIDTH, HEIGHT))
screen.blit(screen1, (0, 0))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:  # check for key presses
            if event.key == pygame.K_LEFT:  # left arrow turns left
                pressed_left = True
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                pressed_right = True
            elif event.key == pygame.K_UP:  # up arrow goes up
                pressed_up = True
            elif event.key == pygame.K_DOWN:  # down arrow goes down
                pressed_down = True
        elif event.type == pygame.KEYUP:  # check for key releases
            if event.key == pygame.K_LEFT:  # left arrow turns left
                pressed_left = False
            elif event.key == pygame.K_RIGHT:  # right arrow turns right
                pressed_right = False
            elif event.key == pygame.K_UP:  # up arrow goes up
                pressed_up = False
            elif event.key == pygame.K_DOWN:  # down arrow goes down
                pressed_down = False
    print(money_group.sprites())
    # In your game loop, check for key states:
    for i in range(len(cash_m)):
        f = random.randint(1, 150)
        d1, d2 = 0, 0
        if 1 < f < 25 and pygame.sprite.spritecollideany(cash_m[i], box_black_group) == None:
            cash_m[i].rect.x += 15
            d1 = 15
        if 26 < f < 50 and pygame.sprite.spritecollideany(cash_m[i], box_black_group) == None:
            cash_m[i].rect.x -= 15
            d1 = -15
        if 51 < f < 75 and pygame.sprite.spritecollideany(cash_m[i], box_black_group) == None:
            cash_m[i].rect.y += 15
            d2 = 15
        if 76 < f < 100 and pygame.sprite.spritecollideany(cash_m[i], box_black_group) == None:
            cash_m[i].rect.y -= 15
            d2 = -15
        if pygame.sprite.spritecollideany(cash_m[i], box_black_group) != None:
            if d1 == 0:
                cash_m[i].rect.y += d2 * -1
            else:
                cash_m[i].rect.x += d1 * -1
    if pressed_left:
        player.rect.x -= STEP
        if pygame.sprite.spritecollideany(player, box_group) != None or \
                pygame.sprite.spritecollideany(player, box_black_group) != None:
            player.rect.x += STEP
        elif pygame.sprite.spritecollideany(player, money_group) != None:
            pygame.sprite.spritecollideany(player, money_group).kill()
    if pressed_right:
        player.rect.x += STEP
        if pygame.sprite.spritecollideany(player, box_group) != None or \
                pygame.sprite.spritecollideany(player, box_black_group) != None:
            player.rect.x -= STEP
        elif pygame.sprite.spritecollideany(player, money_group) != None:
            pygame.sprite.spritecollideany(player, money_group).kill()
    if pressed_up:
        player.rect.y -= STEP
        if pygame.sprite.spritecollideany(player, box_group) != None or \
                pygame.sprite.spritecollideany(player, box_black_group) != None:
            player.rect.y += STEP
        elif pygame.sprite.spritecollideany(player, money_group) != None:
            pygame.sprite.spritecollideany(player, money_group).kill()
    if pressed_down:
        player.rect.y += STEP
        if pygame.sprite.spritecollideany(player, box_group) != None or \
                pygame.sprite.spritecollideany(player, box_black_group) != None:
            player.rect.y -= STEP
        elif pygame.sprite.spritecollideany(player, money_group) != None:
            pygame.sprite.spritecollideany(player, money_group).kill()

    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)


    tiles_group.draw(screen)
    player_group.draw(screen)
    money_group.draw(screen)
    box_black_group.draw(screen)
    nps_group.draw(screen)
    star_group.draw(screen)
    cvest_nps()
    pygame.display.flip()
    clock.tick(FPS)
terminate()
