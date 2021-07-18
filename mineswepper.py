import pygame as pg
import random
from math import floor

loads = {1: "none.png", 2: "flag.png", 3: "q.png", 4: 'mine2.png',
         5: 'miner.png', 6: 'mine.png'}

mines = {0: 'fill.png',
         1: 'm1.png', 2: 'm2.png', 3: 'm3.png', 4: 'm4.png',
         5: 'm5.png', 6: 'm6.png', 7: 'm7.png', 8: 'm8.png',
         9: 'mine.png'}

w = 50
h = 30
ui = 50
size = 32
ww = w * size
wh = h * size + ui
maxs = 2
mins = 0
chance = [0, 0, 0, 9]
shown = True
lose = False

showm = []
minelist = []

black = [0, 0, 0]
white = [255, 255, 255]
minesnum = 0
flags = 0
lives = 1
dlives = 1

pg.font.init()

positions = [[-1, -1], [0, -1], [1, -1], [-1, 0], [1, 0], [-1, 1], [0, 1], [1, 1]]


def ne(alist: list, x: int, y: int, r: int):
    global positions
    c = 0
    for i in positions:
        try:
            if alist[y + i[0]][x + i[1]] == r:
                c += 1
        except IndexError:
            pass
    return c


def mts(text: str = "", x: int = 0, y: int = 0, col=None, fontsize=30):
    if col is None:
        col = [0, 0, 0]
    fontr = pg.font.Font("font.ttf", fontsize)
    screen_text = fontr.render(text, True, col, None)
    window.blit(screen_text, [x, y])


def ngame():
    global showm, minelist, minesnum, flags, lose, lives
    showm, minelist = [], []
    minesnum, flags = 0, 0
    for _ in range(0, h):
        py = []
        for _ in range(0, w):
            py.append(1)
        showm.append(py)

    for _ in range(0, h):
        py = []
        for _ in range(0, w):
            py.append(random.choice(chance))
        minelist.append(py)
    for y in minelist:
        for x in y:
            if x == 9:
                minesnum += 1
    flags = minesnum
    lose = False
    lives = dlives
    show()


def win():
    xp = 0
    yp = 0
    wn = True
    for y in minelist:
        for x in y:
            if x == 9:
                if showm[yp][xp] != 2:
                    wn = False
            xp += 1
        yp += 1
        xp = 0
    if wn:
        return True
    else:
        return False


def draw():
    global minelist
    xp = 0
    yp = 0
    for y in minelist:
        for x in y:
            c = ne(minelist, xp, yp, 9)
            if x != 9:

                minelist[yp][xp] = c
                pic = pg.image.load(mines[c])
                pic = pg.transform.scale(pic, (size, size))
                window.blit(pic, pg.rect.Rect(xp * size, yp * size, size, size))
            if x == 9:
                pic = pg.image.load(mines[9])
                pic = pg.transform.scale(pic, (size, size))
                window.blit(pic, pg.rect.Rect(xp * size, yp * size, size, size))
            xp += 1
        yp += 1
        xp = 0


def show():
    global flags
    window.fill(white)
    draw()
    flags = minesnum
    fl = 0
    if shown:
        xp = 0
        yp = 0
        for y in showm:
            for x in y:
                if x > 0:
                    pic = pg.image.load(loads[x])
                    pic = pg.transform.scale(pic, (size, size))
                    window.blit(pic, pg.rect.Rect(xp * size, yp * size, size, size))
                xp += 1
                if x == 2:
                    fl += 1
            xp = 0
            yp += 1
    flags = flags - fl


def click():
    mx = floor(pg.mouse.get_pos()[0] / size)
    my = floor(pg.mouse.get_pos()[1] / size)
    if not (pg.mouse.get_pos()[1] > wh - ui or pg.mouse.get_pos()[0] > ww):
        if showm[my][mx] != 9:
            showm[my][mx] = 0
            m = []
            for _ in range(0, h):
                py = []
                for _ in range(0, w):
                    py.append(0)
                m.append(py)
            m[my][mx] = 1
            for _ in range(0, max([w, h])):
                yp = 0
                xp = 0
                for y in m:
                    for x in y:
                        if x == 1:
                            le = False
                            ri = False
                            up = False
                            do = False
                            if xp - 1 != -1:
                                if mins <= minelist[yp][xp - 1] <= maxs:
                                    m[yp][xp - 1] = 1
                                    le = True
                            if yp + 1 != h:
                                if mins <= minelist[yp + 1][xp] <= maxs:
                                    m[yp + 1][xp] = 1
                                    do = True
                            if xp + 1 != w:
                                if mins <= minelist[yp][xp + 1] <= maxs:
                                    m[yp][xp + 1] = 1
                                    ri = True
                            if yp - 1 != -1:
                                if mins <= minelist[yp - 1][xp] <= maxs:
                                    m[yp - 1][xp] = 1
                                    up = True
                            if xp - 1 != -1 and yp - 1 != -1:
                                if (mins <= minelist[yp - 1][xp - 1] <= maxs) and (le or up):
                                    minelist[yp - 1][xp - 1] = 1
                            if xp + 1 != w and yp + 1 != h:
                                if (mins <= minelist[yp + 1][xp + 1] <= maxs) and (do or ri):
                                    minelist[yp + 1][xp + 1] = 1
                            if xp - 1 != -1 and yp + 1 != h:
                                if (mins <= minelist[yp + 1][xp - 1] <= maxs) and (le or do):
                                    minelist[yp + 1][xp - 1] = 1
                            if xp + 1 != w and yp - 1 != -1:
                                if (mins <= minelist[yp - 1][xp + 1] <= maxs) and (ri or up):
                                    minelist[yp - 1][xp + 1] = 1
                        xp += 1
                    yp += 1
                    xp = 0
            xp = 0
            yp = 0
            for y in m:
                for x in y:
                    if x == 1:
                        showm[yp][xp] = 0
                    xp += 1
                yp += 1
                xp = 0
        if minelist[my][mx] == 9:
            global lives
            lives -= 1
            if lives == 0:
                global lose
                xp = 0
                yp = 0
                lose = True
                for y in minelist:
                    for x in y:
                        if x == 9 and showm[yp][xp] != 2:
                            showm[yp][xp] = 6
                        if x == 9 and showm[yp][xp] == 2:
                            showm[yp][xp] = 4
                        xp += 1
                    yp += 1
                    xp = 0
                showm[my][mx] = 5
    show()


def flagp():
    mx = floor(pg.mouse.get_pos()[0] / size)
    my = floor(pg.mouse.get_pos()[1] / size)
    if showm[my][mx] == 1:
        showm[my][mx] = 2
    elif showm[my][mx] == 2:
        showm[my][mx] = 3
    elif showm[my][mx] == 3:
        showm[my][mx] = 1
    show()


pg.init()
window = pg.display.set_mode([ww, wh])
pg.display.set_caption('mineswepper')
ngame()
game = True
show()
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            exit()
        if e.type == pg.KEYDOWN:
            if e.key == pg.K_r:
                ngame()
            if e.key == pg.K_e:
                if shown:
                    shown = False
                else:
                    shown = True
                show()
            if e.key == pg.K_ESCAPE:
                exit()

        if e.type == pg.MOUSEBUTTONDOWN:
            if not lose:
                if pg.mouse.get_pressed(3)[0]:
                    click()
                if pg.mouse.get_pressed(3)[2]:
                    flagp()
                win()

    mts("Mines   " + str(minesnum), 0, wh - ui, fontsize=20)
    mts("Flags remain   " + str(flags), 0, int(wh - (ui / 2)), fontsize=20)
    mts("Lives   " + str(lives), int(ww / 2), int(wh - (ui / 2)), fontsize=20)
    if win():
        mts("You   win!", int(ww / 2), wh - ui, [255, 0, 0], 50)
    elif lose:
        mts("You   Lose!", int(ww / 2), wh - ui, [255, 0, 0], 50)
    pg.display.flip()
    pg.display.update()
pg.quit()
