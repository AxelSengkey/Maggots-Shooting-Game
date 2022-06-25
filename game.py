import pygame
from pygame.locals import *
import math
from random import randint

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

exitcode = 0
exitcode_gameover = 0
exitcode_win = 1

# font
font_clock = pygame.font.Font("resources/font/Wilderness_0.ttf", 24)
font_score = pygame.font.Font("resources/font/Wilderness_0.ttf", 20)
font_fscore = pygame.font.Font("resources/font/Wilderness_0.ttf", 28)

# image asset
background = pygame.image.load("resources/images/grass.png")
people = pygame.image.load("resources/images/people.png")
sword_img = pygame.image.load("resources/images/sword.png")
enemy_img = pygame.image.load("resources/images/maggot_single.png")
health_bar = pygame.image.load("resources/images/healthbar.png")
health = pygame.image.load("resources/images/health.png")
gameover = pygame.image.load("resources/images/gameover.png")
win = pygame.image.load("resources/images/youwin.png")

# music asset
pygame.mixer.init()
hit_people_sound = pygame.mixer.Sound(
    "resources/audio/mixkit-chewing-something-crunchy-2244.wav")
hit_enemy_sound = pygame.mixer.Sound(
    "resources/audio/mixkit-cartoon-blood-and-gore-hit-726.wav")
sword_sound = pygame.mixer.Sound(
    "resources/audio/zapsplat_foley_cane_whoosh_through_air_whip_001_11671.mp3")
hit_people_sound.set_volume(0.7)
hit_enemy_sound.set_volume(0.2)
sword_sound.set_volume(0.3)

pygame.mixer.music.load("resources/audio/shock-16378.mp3")
pygame.mixer.music.play(-1, 0.0)
pygame.mixer.music.set_volume(0.1)

set_index = 0
frame_set_start = 0
frame_set_end = 2

dwell = 10  # number frames to spend on each image

# to strip the player image to frames
def strip_from_sheet():
    sheet = pygame.image.load('resources/images/summoner.png')

    r = sheet.get_rect()
    rows = 1
    columns = 3
    img_width = r.w/columns
    img_height = r.h/rows

    frames = []
    for row in range(rows):
        for col in range(columns):
            rect = pygame.Rect(col*img_width, row*img_height,
                               img_width, img_height)
            frames.append(sheet.subsurface(rect))

    return frames


frames = strip_from_sheet()

# player
class Player:
    def __init__(self, x, y):
        self.playerposx = x
        self.playerposy = y
        self.top = False
        self.bottom = False
        self.left = False
        self.right = False
        self.mousepos = [0, 0]
        self.angle = 0
        self.playerpos_rot = [0, 0]
        self.attack = False
        self.swd_no = 0
        self.index = 0
        self.rect = frames[self.index].get_rect()
        self.dwell_countdown = dwell
    # change the image frame continously
    def advanceImage(self):
        self.dwell_countdown -= 1
        if self.dwell_countdown < 0:
            self.dwell_countdown = dwell
            self.index = (self.index+1) % (frame_set_end+1)

    def show(self):
        self.mousepos = pygame.mouse.get_pos()
        self.angle = math.atan2(
            self.mousepos[1] - self.playerposy, self.mousepos[0] - self.playerposx)
        angle_deg = self.angle * 57.29  # 180/pi
        player_rot = pygame.transform.rotate(
            frames[self.index], 360 - angle_deg)
        self.playerpos_rot = [self.playerposx - player_rot.get_rect(
        ).width / 2, self.playerposy - player_rot.get_rect().height / 2]
        screen.blit(player_rot, self.playerpos_rot)

        if self.top and self.right and self.playerposy >= 0 and self.playerposx <= width-64:
            self.playerposy -= 1
            self.playerposx += 1
        elif self.top and self.left and self.playerposy >= 0 and self.playerposx >= 100:
            self.playerposy -= 1
            self.playerposx -= 1
        elif self.bottom and self.right and self.playerposy <= height-46 and self.playerposx <= width-64:
            self.playerposy += 1
            self.playerposx += 1
        elif self.bottom and self.left and self.playerposy <= height-46 and self.playerposx >= 100:
            self.playerposy += 1
            self.playerposx -= 1
        elif self.top and self.playerposy >= 0:
            self.playerposy -= 3
        elif self.bottom and self.playerposy <= height-46:
            self.playerposy += 3
        elif self.left and self.playerposx >= 100:
            self.playerposx -= 3
        elif self.right and self.playerposx <= width-64:
            self.playerposx += 3

    def show_sword(self, swords):
        if self.attack == True:
            swords.append([self.angle, self.playerpos_rot[0] + 32, self.playerpos_rot[1] + 23])
            self.attack = False

        for sword in swords:
            # sword movement velocity (to change the x,y position)
            velx = math.cos(sword[0]) * 5
            vely = math.sin(sword[0]) * 5
            sword[1] += velx
            sword[2] += vely
            if sword[1] < -50 or sword[1] > width or sword[2] < -50 or sword[2] > height:
                swords.pop(0)
            sword_rot = pygame.transform.rotate(
                sword_img, 360 - sword[0] * 57.29)
            screen.blit(sword_rot, (sword[1], sword[2]))


font = pygame.font.SysFont('colonna', 35)
menu_sound = pygame.mixer.Sound("resources/audio/Sword4.ogg")
menu_sound.set_volume(0.2)

MENU = (255, 244, 230)
MENU_ACTIVE = (232, 235, 94)

click = False


def main_menu():
    while True:

        screen.fill((0, 0, 0))
        background = pygame.image.load("resources/images/bg_mainmenu.png")
        screen.blit(background, (0, 0))
        title = pygame.image.load("resources/images/title.png")
        title_rect = title.get_rect(center=(width/2, height/2-60))
        screen.blit(title, title_rect)

        mx, my = pygame.mouse.get_pos()

        start = font.render("Start", True, MENU)
        quit = font.render("Quit", True, MENU)
        start_rect = start.get_rect(center=(width/2, height/2+80))
        quit_rect = quit.get_rect(center=(width/2, height/2+130))
        screen.blit(start, start_rect)
        screen.blit(quit, quit_rect)
        if start_rect.collidepoint(mx, my):
            start = font.render("Start", True, MENU_ACTIVE)
            screen.blit(start, start_rect)
            if click:
                menu_sound.play()
                game()
        if quit_rect.collidepoint(mx, my):
            quit = font.render("Quit", True, MENU_ACTIVE)
            screen.blit(quit, quit_rect)
            if click:
                pygame.quit()
                exit(0)

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()


def game():

    running = True

    playerpos = [150, 200]
    swords = []
    enemy_timer = 200
    enemies = []
    score = 0
    health_p = 190
    countdown = 30000

    me = Player(playerpos[0], playerpos[1])

    while running:
        screen.fill((0, 0, 0))

        for x in range(int(width/background.get_width()+1)):
            for y in range(int(height/background.get_width()+1)):
                screen.blit(background, (x*100, y*100))

        screen.blit(people, (0, 0))

        me.advanceImage()
        me.show()
        me.show_sword(swords)

        enemy_timer -= 1
        if enemy_timer == 0:
            enemies.append([width, randint(60, height-60)])
            enemy_timer = randint(1, 200)

        enemy_idx = 0
        for enemy in enemies:
            enemy[0] -= 3
            if enemy[0] < -65:
                enemies.pop(enemy_idx)

            # enemy collide with the people
            enemy_rect = pygame.Rect(enemy_img.get_rect())
            enemy_rect.top = enemy[1]
            enemy_rect.left = enemy[0]
            if enemy_rect.left < 50:
                enemies.pop(enemy_idx)
                health_p -= 20  # damage point
                hit_people_sound.play()
                print("AAAA!!! OH, NO!")

            sword_idx = 0
            for sword in swords:
                sword_rect = pygame.Rect(sword_img.get_rect())
                sword_rect.top = sword[2]
                sword_rect.left = sword[1]
                # enemy collide with sword
                if enemy_rect.colliderect(sword_rect):
                    score += 1
                    enemies.pop(enemy_idx)
                    swords.pop(sword_idx)
                    hit_enemy_sound.play()
                    print("JLEB!")
                    print("Score: {}".format(score))
                sword_idx += 1
            enemy_idx += 1

            screen.blit(enemy_img, enemy)

        # show the score
        score_text = "Kills: {}".format(score)
        score_show = font_score.render(score_text, True, (255, 255, 255))
        scoretext_rect = score_show.get_rect()
        scoretext_rect.topright = [500, 10]
        screen.blit(score_show, scoretext_rect)

        # show the health bar
        screen.blit(health_bar, (5, 8))
        for hp in range(health_p):
            screen.blit(health, (hp+58, 13))

        # show the countdown time
        minutes = int((countdown - pygame.time.get_ticks())/60000)
        seconds = int((countdown - pygame.time.get_ticks())/1000 % 60)
        time_text = "{:02}:{:02}".format(minutes, seconds)
        clock = font_clock.render(time_text, True, (255, 255, 255))
        text_rect = clock.get_rect()
        text_rect.topright = [630, 8]
        screen.blit(clock, text_rect)

        pygame.display.flip()

        for event in pygame.event.get():
            # exit
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

            # mousebuttondown to summon sword
            if event.type == pygame.MOUSEBUTTONDOWN:
                me.attack = True
                sword_sound.play()

            # keydown keyup
            if event.type == pygame.KEYDOWN:
                if event.key == K_w:
                    me.top = True
                elif event.key == K_s:
                    me.bottom = True
                elif event.key == K_a:
                    me.left = True
                elif event.key == K_d:
                    me.right = True

            if event.type == pygame.KEYUP:
                if event.key == K_w:
                    me.top = False
                elif event.key == K_s:
                    me.bottom = False
                elif event.key == K_a:
                    me.left = False
                elif event.key == K_d:
                    me.right = False

        # win lose
        if pygame.time.get_ticks() > countdown:
            running = False
            exitcode = exitcode_win
        if health_p <= 0:
            running = False
            exitcode = exitcode_gameover

    # GAME LOOP END

    # show win lose
    if exitcode == exitcode_gameover:
        screen.blit(gameover, (0, 0))
    else:
        screen.blit(win, (0, 0))

    # show the final score
    finalscoretext = font_fscore.render(
        "Score: {}".format(score), True, (255, 255, 255))
    finalscoretext_rect = finalscoretext.get_rect(center=(width/2, height/2-75))
    screen.blit(finalscoretext, finalscoretext_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
        pygame.display.flip()


main_menu()

# guide from the internet:
# https://www.petanikode.com/pygame-untuk-pemula/
