import pygame
import sys

score = 0
health = 100
pygame.init()
screen = pygame.display.set_mode([1080, 650])
running = True
B = pygame.image.load('Block.png')
C = pygame.image.load('Resurse.png')
HP = pygame.image.load('Cristal.png')
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill('BLACK')

# Схема стены
    screen.blit(B, (0, 0)), screen.blit(B, (30, 0)), screen.blit(B, (0, 30)), screen.blit(B, (30, 30))

# Схема сборщика
    screen.blit(B, (0, 90)), screen.blit(B, (30, 90)), screen.blit(B, (90, 90)), screen.blit(B, (120, 90))
    screen.blit(B, (0, 120)), screen.blit(C, (60, 120)), screen.blit(B, (120, 120))
    screen.blit(B, (0, 150)), screen.blit(B, (30, 150)), screen.blit(B, (90, 150)), screen.blit(B, (120, 150))

# Схема базовой пушки
    screen.blit(B, (0, 210)), screen.blit(B, (30, 210)), screen.blit(B, (30, 240))
    f1 = pygame.font.SysFont("serif", 22); text1 = f1.render('или', True, ("WHITE")); screen.blit(text1, (70, 225))
    screen.blit(B, (120, 210)), screen.blit(B, (150, 240)), screen.blit(B, (180, 210))

# Схема пушки c большей дальностью стрельбы и силой
    screen.blit(B, (0, 300)), screen.blit(B, (30, 300)), screen.blit(B, (60, 300)),
    screen.blit(B, (60, 330)), screen.blit(B, (60, 360))
    f1 = pygame.font.SysFont("serif", 22); text1 = f1.render('или', True, ("WHITE")); screen.blit(text1, (100, 330))
    screen.blit(B, (150, 300)), screen.blit(B, (180, 330)), screen.blit(B, (210, 360)),
    screen.blit(B, (240, 330)), screen.blit(B, (270, 300))

# Схема пушки c повышенной скорострельностью и силой
    screen.blit(B, (0, 420)), screen.blit(B, (30, 420)), screen.blit(B, (30, 450)), screen.blit(C, (0, 450))

# Схема огнемёта
    screen.blit(B, (300, 0)), screen.blit(B, (300, 30)), screen.blit(B, (270, 30)), screen.blit(C, (300, 60))
    screen.blit(B, (270, 60)), screen.blit(B, (240, 60)),

# Схема зинитки
    screen.blit(B, (450, 0)), screen.blit(B, (510, 0)), screen.blit(C, (480, 30))
    screen.blit(B, (450, 60)), screen.blit(B, (510, 60))

# Схема улучшеной зинитки
    screen.blit(B, (700, 0)), screen.blit(B, (820, 0)), screen.blit(B, (730, 30)), screen.blit(B, (790, 30))
    screen.blit(C, (760, 60))
    screen.blit(B, (730, 90)), screen.blit(B, (790, 90)), screen.blit(B, (700, 120)), screen.blit(B, (820, 120))

# Схема автоматического строителя стен
    screen.blit(B, (400, 180)), screen.blit(B, (430, 180)), screen.blit(C, (460, 180))
    screen.blit(C, (400, 210)), screen.blit(C, (430, 210))
    screen.blit(B, (400, 240)), screen.blit(B, (430, 240)), screen.blit(C, (460, 240))

# Кол-во кристаллов
    f2 = pygame.font.SysFont("serif", 22)
    text2 = f2.render(f"{score} / 100", True, ("WHITE"))
    screen.blit(text2, (100, 550)), screen.blit(C, (50, 550))

# Кол-во хп города
    f3 = pygame.font.SysFont("serif", 22)
    text3 = f3.render(f"{health} / 100", True, ("WHITE"))
    screen.blit(text3, (100, 600)), screen.blit(HP, (40, 590))

    pygame.display.flip()
pygame.quit()