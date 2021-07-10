import requests
import jsonpickle
# *this is never used because the function is shared with the mobs, the mobs specify when the thing hits whereas the player has separate conditions. this is a mess btw.
# import numpy as np
import random
import pygame
import math
import time
import os
from pygame.locals import *
headers = {'Content-type': 'application/json'}
pygame.init()
arrows = []
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()
class player(object):
    def __init__(self,ID,X,Y,H):
        self.ID=ID
        self.X=X
        self.Y=Y
        self.H =H

with open("ip.txt", "r") as ip:
    ipadress=ip.read()

r = requests.get(f'http://{ipadress}:5000/start')
me=jsonpickle.decode(r.text)

def img(imgname):
    return pygame.image.load(imgname).convert_alpha()


fontBG = pygame.font.Font('freesansbold.ttf', 50)
font = pygame.font.Font('freesansbold.ttf', 25)
funt = pygame.font.Font('freesansbold.ttf', 30)
fpont = pygame.font.Font('freesansbold.ttf', 20)
fint = pygame.font.Font('freesansbold.ttf', 150)
flont = pygame.font.Font('freesansbold.ttf', 80)
flint = pygame.font.Font('freesansbold.ttf', 45)
folnt = pygame.font.Font('freesansbold.ttf', 40)
icon = img('man.png')
pygame.display.set_icon(icon)
mobs = []
PYSPD = 0
timedstuffs = []
PXSPD = 0
tiles = []
grases = [img('gras1.png'), img('gras2.png'), img('gras3.png'), img('gras4.png'), img('gras5.png')]
terrain = []


def blit_text(text, pos, font, max_width, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 1, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            screen.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


############          player          ############

Px = 0
Py = 0
PARMR = 0
PPARMR = 0
PELEMENT = [0, 0]
PED = [0, 0, 0]
PSPECIAL = []
PSPECIALO = []
PATC = [1, 1]
Patcsped = [10, 10]
PRange = [30, 30]
PSPE = 11
PEQ = []
gold = 0
############                          ############

#### elements: air water stone fire. [number of element, amount]

# position,img,armor,armor piercing,element,speed,
# name, identification?,health,attack,specials
enearrow = []
news = pygame.transform.smoothscale(img('dudenews.png'), (w, h))
allyarrow = []
mosh = img('mosh.png')
draconian = img('draconian.png')
dopusatc = [img('dopusattack.png'), img('dopusattack.png'), img('dopus.png')]
mobtile=img('buff.png')
def shoot(e, arow, shouldIshoot):
    global XX
    # Speed,attack,pierce,sametarget,IMG
    if e == 'mouse':
        XX = pygame.mouse.get_pos()
        xS = (w / 2) - (XX[0])
        yS = (h / 2) - (XX[1])
    else:
        xS = (w / 2) - (e.x + e.s[0] / 2 + me.X)
        yS = (h / 2) - (e.y + e.s[1] / 2 + me.Y)
    if xS == 0:
        spdx = arow[1]
        spdy = 0
    else:
        spdx = arow[1] / math.sqrt(yS ** 2 / xS ** 2 + 1)
        if xS < 0:
            spdx *= -1
        spdy = spdx * yS / xS
    # e.EX=spdx
    # e.EY=spdy
    if spdx == 0:
        if spdy < 0:
            final = pygame.transform.rotate(arow[5], -90)
        else:
            final = pygame.transform.rotate(arow[5], 90)
    elif spdx > 0:
        final = pygame.transform.rotate(arow[5], -math.atan(spdy / spdx) * 180 / math.pi)
    else:
        final = pygame.transform.flip(arow[5], False, True)
        final = pygame.transform.rotate(final, 180 - math.atan(spdy / spdx) * 180 / math.pi)

    if arow[4] < 0:
        ally = 1
    else:
        ally = 0

    if ally == 0:
        arrows.append(arrow(e.x + e.s[0] // 2, e.y + e.s[1] // 2, spdx, spdy, arow[2], arow[3], arow[4], 0, final))
    else:
        arrows.append(arrow(w // 2 - Px, h // 2 - Py, -spdx, -spdy, arow[2], arow[3], -arow[4] + 1, 1, final))

def atcdown(t, multiplier):
    multiplier[0].A[0] /= multiplier[1]
    timedstuffs.remove(t)
    t.kill
    del t
screen.fill((50,50,50))
screen.blit(news, ((0, 0)))
screen.blit(pygame.transform.smoothscale(img("loading.png"),(900,100)), ((int(w*0.15), int(h*0.81))))
pygame.display.update()
def slow(e, multiplier, nothin):
    e.EX /= multiplier[1]
    e.EX /= multiplier[1]
    e.EY /= multiplier[1]
    e.S[0] /= multiplier[1]
    timedstuffs.append(timer(spdup, ti + multiplier[2], [e, multiplier[1]], e.ID))
    timedstuffs.sort(key=bythetime)
mobspd=0.8

def spdup(t, multiplier):
    multiplier[0].EX *= multiplier[1]
    multiplier[0].EY *= multiplier[1]
    multiplier[0].S[0] *= multiplier[1]
    timedstuffs.remove(t)
    t.kill
    del t

def hpboost(e, multiplier, nothin):
    e.H[1] = int(e.H[1]*multiplier[1])
    e.H[0] = int(e.H[0]*multiplier[1])
    timedstuffs.append(timer(hplow, ti + multiplier[2], [e, multiplier[1]], e.ID))
    timedstuffs.sort(key=bythetime)

def hplow(t, multiplier):
    multiplier[0].H[0] = int(multiplier[0].H[0]*multiplier[1])
    multiplier[0].H[1] = int(multiplier[0].H[1]*multiplier[1])
    timedstuffs.remove(t)
    t.kill
    del t

bullet = img('bullet.png')
def atcup(e, multiplier, nothin):
    global timedstuffs
    e.A[0] *= multiplier[1]
    timedstuffs.append(timer(atcdown, ti + multiplier[2], [e, multiplier[1]], e.ID))
    timedstuffs.sort(key=bythetime)
armors=[]
chopper=img('chopper.png')
choppercrpd=img('chopperA.png')
zandalar=img('zandalar.png')
lava=img('lava.png')
zandalarcrpd=img('zandalarcrpd.png')
ice=img('icesword.png')
ice2=img('iceswordcrpd.png')
ash=img('ashenblade.png')
ash2=img('ashenbladecrpd.png')
gun=img('gunsaber.png')
gun2=img('gunsabercropped.png')
torso=img('torsoarmor.png')
torso2=img('torsoarmorcrpd.png')
demon=img('demonplate.png')
deflect=img('projectiledeflector.png')
life=img('lifegown.png')
def weaponsRANDOM(gouit, pricemult=0, spellmult=0, bigmult=1):
    global weapons, armors
    if gouit == 0:
        luck = random.randint(1, 30)
    else:
        luck = gouit
    if luck < 6:
        quality = 'Trash'
    elif luck < 11:
        quality = 'Inferior'
    elif luck < 16:
        quality = 'Decent'
    elif luck <= 21:
        quality = 'Great'
    elif luck < 26:
        quality = 'Giant'
        bigmult+=0.5
    elif luck < 30:
        quality = 'LEGENDARY'
        luck += 20
    elif luck == 30:
        quality = 'MYTHIC'
        luck += 30

        #X, Y, I, A,speed, SPE, cost

    weapons = [[-50, 40, [chopper, choppercrpd], 6 + luck // 1.5,0, [], 100 + luck*3,
                [quality + ' Chopper', 'quite a basic sword, decently long though, costs:' + str(100 + luck*3)]]
        , [-50, 40, [zandalar,zandalarcrpd], 3 + luck // 2.5,-2-luck//15, [], 80 + luck**2,
           [quality + ' Zandalari meatcleaver', 'short and weak, but fast costs:' + str(80 + luck**2)]]
        , [-50, 40, [ice, ice2], 30 + luck // 2,0-luck//15,
           [[1, 2], 0, 0, 100, slow, ['*line 1', 1.07 + luck / 80, 65 + luck/1.5]], 250 + luck*luck*2,
           [quality + ' Frost-Slicer',
            'freeze amount and duration is relient on quality. can be very powerful against meele foes. costs:' + str(
                250 + luck*luck*2)]]
        , [-50, 40, [ash, ash2], 75 + luck*20, 0 - luck // 20,
            # Speed,attack,pierce,sametarget,IMG
           [[1,2], 0, 0, 100, shoot, [0, 7, 5+luck*1.5*bigmult,100,-1,pygame.transform.smoothscale(lava, (int(500 * bigmult), int(250 * bigmult)))]], (10000 + luck*luck*80)*bigmult,
           [quality + ' Godslayer',
            'throws lava at enemies hit, immensly expensive. costs:' + str(
                int((5000 + luck*luck*80)*bigmult))]]
        , [-50, 40, [gun, gun2], luck // 10,4-luck//10,
           [[2], 1, 1, 0, shoot, [0, 25, luck * 0.5+luck**2*0.05, 1, -1, pygame.transform.smoothscale(bullet, (int(30 * bigmult), int(15 * bigmult)))]], 50 * luck+luck**2, [quality + ' Gun',
                                                                                  'guns can be utter failiures, or strong, but it will reflect on the price costs:' + str(
                                                                                      50 * luck+luck**2)]]]

          #I, Armor, PArmor, helf, SPE, cost

    armors =[[[torso, torso2], 5 + luck // 3, 2 + luck // 8, int(100+luck*luck/5*(bigmult*3-2)), [], 400+bigmult*2000 + luck*luck//2,
                [quality + ' Torsoarmor', 'quite a basic armorpiece, still much better than nothing though, costs:' + str(400+bigmult*1500 + luck*luck//2)]],
    [[demon, demon], int((35 + luck*1.5)*(bigmult*3-2)),4 + luck // 7,int(50+luck*luck/10*(bigmult*3-2)), [], 600+bigmult*2000 + int(luck*luck*1.5),
                [quality + 'Demonplate', 'has a lot of armor, not so much health though, costs:' + str(600+bigmult*2000 + int(luck*luck*1.5))]],
    [[deflect, deflect], (7 + int(luck*0.3))*(bigmult*3-2),(10 + luck*2)*(bigmult*3-2),int(50+luck*luck/10*(bigmult*3-2)), [], 600+bigmult*1500 + int(luck*luck*1.5),
                [quality + 'The Deflector', 'has some armor, not much health, but protects from projectiles (and special sources of damage) costs:' + str(600+bigmult*1500 + int(luck*luck*1.5))]],
    [[life, life], -45 - int(luck*1.5)-400*(bigmult*2-2),-70 - int(luck*1.5)-400*(bigmult*2-2),int(600+luck*luck*1.8+ 10000*(bigmult*2-2)), [], 600 +bigmult*2000 + int(luck*luck*1.5),
                [quality + 'Lifegown', 'has a lot of helf, not so healthy though, considering the negative armor, costs:' + str(600+bigmult*2000 + int(luck*luck*1.5))]]]

    if bigmult !=1:
        for e in weapons:
            soiz = e[2][0].get_size()
            e[2][0] = pygame.transform.smoothscale(e[2][0], (int(soiz[0] * bigmult), int(soiz[1] * bigmult)))
        for e in armors:
            soiz = e[0][0].get_size()
            e[0][0] = pygame.transform.smoothscale(e[0][0], (int(soiz[0] * bigmult), int(soiz[1] * bigmult)))
weaponsRANDOM(0)
dragonatc=[img('draconianatc.png'),img('draconian.png')]
dragon=img('draconian.png')
dopusIMG=img('dopus.png')
orcIMG=img('orc.png')
orcatc=[img('orcatc.png'),img('orc.png')]
fireball=img('fireball.png')
dopii=img('dope.png')
grasatacbig = [pygame.transform.smoothscale(img('grasatc1.png'),(400,400)), pygame.transform.smoothscale(img('grasatc2.png'),(400,400)), pygame.transform.smoothscale(img('grasatc2.png'),(400,400))]
grasatac = [img('grasatc1.png'), img('grasatc2.png'), img('grasatc2.png')]
dope=pygame.transform.smoothscale(dopii,(50,50))
dopeatc=[pygame.transform.smoothscale(dopii,(75,75)),pygame.transform.smoothscale(dopii,(100,100)),pygame.transform.smoothscale(dopii,(125,125)),
         pygame.transform.smoothscale(dopii,(150,150)),pygame.transform.smoothscale(dopii,(200,200)),pygame.transform.smoothscale(dopii,(275,275)),
         pygame.transform.smoothscale(dopii,(375,375)),pygame.transform.smoothscale(dopii,(500,500)),pygame.transform.smoothscale(dopii,(650,650)),
         pygame.transform.smoothscale(dopii,(850,850)),pygame.transform.smoothscale(dopii,(1000,1000)),pygame.transform.smoothscale(dopii,(1200,1200)),
         pygame.transform.smoothscale(dopii,(1600,1600)),pygame.transform.smoothscale(dopii,(1900,1900)),pygame.transform.smoothscale(dopii,(3000,3000)),
         pygame.transform.smoothscale(dopii,(5000,5000)),pygame.transform.smoothscale(dopii,(15000,15000))]
ampla=[4,4 ,1,1, 5,1, 0.2,0.1, 8,2, 4,3]
ampli=[1,1,1,1,1,1,1,1,1,1,1,1,1,1,]
def genmob(mobnumber, position=[700,700],power=[1,0]):
    global ampli,ampla
    weaponsRANDOM(0)
    if power[1]==1:
        ample=[e*power[0] for e in ampla]
    elif power[0]==1:
        ample = ampli
    else:
        ample = [e*power[0] for e in ampli]
    if mobnumber==1:
        MOB=mob(position[0], position[1], [grases[random.randint(0, 4)], grasatac], random.randint(3, 5), 'grass',
                        [atcup, [[1, 2, 3], 3, 140], shoot, [[4], 2, 10*ample[1], -1, 3, mosh]], random.randint(1, 170)*ample[0],
                        [15*ample[1], 15*ample[1]],140, weapons[0])
    elif mobnumber == 2:
        MOB=mob(position[0], position[1], [pygame.transform.smoothscale(grases[random.randint(0, 4)],(400,400)), grasatacbig], 5.5, 'grass',
                        [atcup, [[1, 2, 3], 4, 140], shoot, [[4], 5.6, 30*ample[3], -1, 3, pygame.transform.smoothscale(mosh,(942,565))]], random.randint(600, 1000)*ample[2],
                        [15*ample[3], 15*ample[3]],140, weapons[4])
    elif mobnumber == 3:
        MOB=mob(position[0], position[1], [dopusIMG, dopusatc, [60, 0, 239, 287]], random.randint(6, 8), 'dopus',
                        [atcup, [[3], 180, 120], slow, [[3], 3, 120]], 50*ample[4], [2*ample[5], 2*ample[5]],120, weapons[1])
    elif mobnumber == 4:
        MOB=mob(position[0], position[1], [dragon, dragonatc], random.randint(4, 5), 'fire lizard',
                        [atcup, [[2], 150, 150], shoot, [[3], 20, 200*ample[6], 60, 2, fireball]], 5000*ample[6], [30*ample[7], 30*ample[7]],150, weapons[3])
    elif mobnumber == 5:
        MOB=mob(position[0], position[1], [dope, dopeatc], random.randint(7, 10), 'dope',
                        [atcup, [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21], 4, 10000], slow, [[2], 150, 15000],
                         hpboost, [[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21], 3, 10000]], 15*ample[8], [2*ample[9], 2*ample[9]],120, weapons[2])
    elif mobnumber == 6:
        MOB=mob(position[0], position[1], [orcIMG, orcatc, [-20, 0, 300, 300]], random.randint(3, 4), 'orc',
                        [atcup, [[2], 2, 500], slow, [[2], 0.5, 50]], 250*ample[10], [30*ample[11], 30*ample[11]],50, weapons[4])
    return MOB
class moob(pygame.sprite.Sprite):
    def __init__(self,X,Y,I,ID,Enemies,difficulty):
        self.ID=ID
        self.X=X
        self.Y=Y
        self.I = I
        self.s = self.I.get_size()
        self.enemies = []
        self.e=Enemies
        self.d = difficulty
    def enter(self):
        for e in range(self.e):
            mawb=genmob(random.randint(1,6), [2000,2000], [self.d/100,0])
            mawb.X=random.randint(-2000,2000)
            mawb.Y = random.randint(-2000, 2000)
            self.enemies.append(mawb)
ranged=[]

class shop(object):
    def __init__(self,ID,X,Y):
        self.ID =ID
        self.X=X
        self.Y=Y

class arrow(pygame.sprite.Sprite):
    def __init__(self, X, Y, speedx, speedy, dmg, pierce, sametarget, friendly, I):
        super(arrow, self).__init__()
        if friendly == 0:
            enearrow.append(self)
        else:
            allyarrow.append(self)
        self.X = X
        self.Y = Y
        self.I = I
        self.x = X
        self.y = Y
        self.SX = speedx
        self.SY = speedy
        self.dmg = dmg
        self.P = pierce
        self.ST = [5, sametarget]
        self.s = self.I.get_size()

    def F(self):
        functionlist[self.f](self, self.power)


class timer(pygame.sprite.Sprite):
    def __init__(self, F, T, power, ID):
        self.T = T
        self.ID = ID
        self.f = F
        self.power = power

    def F(self):
        self.f(self, self.power)

class mob(pygame.sprite.Sprite):
    def __init__(self, X, Y, I, S, N, SPE, H, A,atcspd, Loot, id=0, nevaatc=0):
        super(mob, self).__init__()
        self.fliped=1
        self.atcspd = atcspd
        self.X = X
        self.attacking = nevaatc
        self.Y = Y
        self.x = X
        self.y = Y
        self.i = I[0]
        self.I = self.i
        self.atcs = I[1]
        self.S = [S, S]
        self.A = A
        if id==0:
            self.ID = random.randint(10, 100000000)
        else:
            self.ID = id
        self.SPE = SPE
        self.H = [H, H]
        self.N = N
        self.EX = 0
        self.loot = random.choice([(self.H[1]*3), Loot])
        self.EY = 0
        self.tired = [1, 200]
        self.s = self.I.get_size()
        if len(I) > 2:
            self.trueX = I[2][0]
            self.trueY = I[2][1]
            self.trueS = [I[2][2], I[2][3]]
        else:
            self.trueX = 0
            self.trueY = 0
            self.trueS = 0


class text(pygame.sprite.Sprite):
    def __init__(self, X, Y, I):
        self.X = X
        self.Y = Y
        self.I = I
        self.s = self.I.get_size()


class button(pygame.sprite.Sprite):
    def __init__(self, X, Y, I, F, FunctionInput):
        self.X = X
        self.Y = Y
        self.F = F
        self.Fin = FunctionInput
        self.i = I
        self.s = self.i.get_size()
        self.I = pygame.transform.smoothscale(self.i, (int(self.s[0] * 1.1), int(self.s[1] * 1.1)))
        self.S = self.I.get_size()


class tile(pygame.sprite.Sprite):
    def __init__(self, X, Y, I,ID=-1):
        self.ID=ID
        self.X = X
        self.Y = Y
        self.I = I
        self.s = self.I.get_size()


class item(pygame.sprite.Sprite):
    def __init__(self, X, Y, I):
        self.X = X
        self.Y = Y
        self.i = I
        self.I = I
        self.s = self.I.get_size()


items = []
class Armor(pygame.sprite.Sprite):
    def __init__(self, I, Armor, PArmor, helf, SPE, cost,name):
        self.name=name
        self.cost = cost
        self.I = I[0]
        self.Icropped = I[1]
        self.A = Armor
        self.PA = PArmor
        self.H = helf
        self.SPE = SPE
        self.s = self.I.get_size()
        sizo = self.Icropped.get_size()
        if sizo[0] * 1.5 > (sizo[1]) * 1.2:
            ES = 120
            EY = int((sizo[1] / sizo[0]) * 120)
        else:
            EY = 150
            ES = int((sizo[0] / sizo[1]) * 150)
        ImgOfArmor = pygame.transform.smoothscale(self.Icropped, (ES, EY))
        merged = img('ItemHolder.png')
        sizo = ImgOfArmor.get_size()
        merged.blit(ImgOfArmor, (int(66-sizo[0] // 2), 3))
        multiplier = 0.5
        multiplier2 = 0.1
        gah = 0
        for e in items:
            multiplier += 0.075
            gah += 1
            if gah % 6 == 0:
                multiplier = 0.5
                multiplier2 += 0.18
        sizo = merged.get_size()
        items.append(self)
        self.item = [int(w * multiplier - 4), int(h * multiplier2 - 3), merged, 0, sizo[0], sizo[1]]
        self.saveo = [e for e in self.item]

class Weapon(pygame.sprite.Sprite):
    def __init__(self, X, Y, I, A,speed, SPE, cost,name):
        self.name=name
        self.cost = cost
        multiplier = 0.5
        multiplier2 = 0.1
        gah = 0
        for e in items:
            multiplier += 0.075
            gah += 1
            if gah % 6 == 0:
                multiplier = 0.5
                multiplier2 += 0.18
        self.i = pygame.transform.rotate(I[0], 15)
        self.I = self.i
        self.speed = speed
        self.SPE = [e for e in SPE]
        self.Icropped = pygame.transform.rotate(I[1], 15)
        items.append(self)
        self.X = [X, X, X]
        self.Y = [Y, Y]
        self.A = A
        self.s = self.I.get_size()
        self.R = self.s[1]
        sizoo = self.Icropped.get_size()
        if sizoo[0] * 1.5 > (sizoo[1]) * 1.2:
            ES = 120
            EY = int((sizoo[1] / sizoo[0]) * 120)
        else:
            EY = 150
            ES = int((sizoo[0] / sizoo[1]) * 150)
        ImgOfWeapon = pygame.transform.smoothscale(self.Icropped, (ES, EY))
        sizoo = ImgOfWeapon.get_size()
        merged = img('ItemHolder.png')
        merged.blit(ImgOfWeapon, (int(64 - sizoo[0] // 2), 3))
        sizoo = merged.get_size()
        self.item = [int(w * multiplier - 4), int(h * multiplier2 - 3), merged, 0, sizoo[0], sizoo[1]]
        self.saveo = [e for e in self.item]


def bythetime(e):
    return e.T

ActiveWeapon = []
playerIMG = img('man2.png')
PlayerSize = playerIMG.get_size()
playerIMGcrpd = img('mancropped.png')
PlayerSizecrpd = playerIMGcrpd.get_size()
ti = 0
speech = pygame.transform.smoothscale(img('speech.png'), (int(w * .4), int(h * .3)))
shoptile = img('shop.png')


def draw00(showp):
    XX = pygame.mouse.get_pos()
    for e in buttons:
        if XX[0] + e.s[0] // 2 > e.X > XX[0] - e.s[0] // 2:
            if XX[1] + e.s[1] // 2 > e.Y > XX[1] - e.s[1] // 2:
                screen.blit(e.I, (e.X - e.S[0] // 2, e.Y - e.S[1] // 2))
                if showp == 1:
                    screen.blit(speech, (w * 0.5, h * 0.05))
                    itemname = flint.render(e.Fin[2][0], True, (255, 0, 0))
                    screen.blit((itemname), (w * 0.52, h * 0.059))
                    blit_text(e.Fin[2][1], [w * 0.52, h * 0.1], font, w * 0.9)
            else:
                screen.blit(e.i, (e.X - e.s[0] // 2, e.Y - e.s[1] // 2))
        else:
            screen.blit(e.i, (e.X - e.s[0] // 2, e.Y - e.s[1] // 2))


def draw0():
    for e in arrows:
        screen.blit(e.I, (e.x + me.X - e.s[0] // 2, e.y + me.Y - e.s[1] // 2))

buttons = []
countdown=int(time.time())+10000
def count(counttime):
    global countdown
    countdown=counttime[0]
def shopreplace(Replacement):
    #[the id of the replaced shop, the replacement shop]
    global shops
    for e in shops:
        if e.ID==Replacement[0]:
            shops.remove(e)
            break
    shops.append(tile(Replacement[1].X, Replacement[1].Y, shoptile, Replacement[1].ID))
def draw2():
    global PXSPD, PYSPD, h, w,moving
    for e in tiles:
        if e.X<=-400-me.X:
            tiles.append(tile(e.X+2400,e.Y, grases[random.randint(0, 4)]))
            tiles.remove(e)
        elif e.X>w-me.X+200:
            tiles.append(tile(e.X-2400,e.Y, grases[random.randint(0, 4)]))
            tiles.remove(e)
    for e in tiles:
        if e.Y<=-me.Y-400:
            tiles.append(tile(e.X,e.Y+1600, grases[random.randint(0, 4)]))
            tiles.remove(e)
        elif e.Y>-me.Y+h+200:
            tiles.append(tile(e.X,e.Y-1600, grases[random.randint(0, 4)]))
            tiles.remove(e)
    for e in tiles:
        screen.blit(e.I, (e.X + me.X, e.Y + me.Y))
    for e in shops:
        screen.blit(e.I, (e.X + me.X, e.Y + me.Y))
        if w // 2 + e.s[0] > e.X + me.X + e.s[0] > w // 2:
            if h // 2 + e.s[1] > e.Y + me.Y + e.s[1] > h // 2:
                PXSPD = 0
                PYSPD = 0
                moving = 0
                r = requests.post('http://'+ipadress+':5000/ShopUpdate', headers=headers, data=jsonpickle.encode([e.ID,me.ID]))
                shoops = jsonpickle.decode(r.text)
                shops.append(tile(shoops.X, shoops.Y, shoptile, shoops.ID))
                shops.remove(e)
                e.kill
                shoppin()
    for e in moobs:
        screen.blit(e.I, (e.X + me.X, e.Y + me.Y))
        if w // 2 + e.s[0] > e.X + me.X + e.s[0] > w // 2:
            if h // 2 + e.s[1] > e.Y + me.Y + e.s[1] > h // 2:
                PXSPD = 0
                PYSPD = 0
                mobbin(e)
    for e in mobs:
        screen.blit(e.I, (e.x + me.X, e.y + me.Y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(e.x + me.X - 10, e.y + me.Y - 20, e.s[0], 10))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(e.x + me.X - 10, e.y + me.Y - 20, e.s[0]*e.H[0]/e.H[1], 10))


arenaIMG = img('arena.png')


def draw1():
    global Py, Px, chosen
    screen.blit(arenaIMG, ((w - ArenaSize[0]) // 2 + Px, (h - ArenaSize[1]) // 2 + Py))
    for e in chosen:
        if e.X < (w - ArenaSize[0] - e.s[0]) // 2:
            e.X = (w - ArenaSize[0] - e.s[0]) // 2 + 1
            e.EX *= -1
        elif e.X > (w + ArenaSize[0] - e.s[0]) // 2:
            e.X = (w + ArenaSize[0] - e.s[0]) // 2 - 1
            e.EX *= -1
        if e.Y < (h - ArenaSize[1] - e.s[1]) // 2:
            e.y = (h - ArenaSize[1] - e.s[1]) // 2 + 1
            e.EY *= -1
        elif e.Y > (h + ArenaSize[1] - e.s[1]) // 2:
            e.Y = (h + ArenaSize[1] - e.s[1]) // 2 - 1
            e.EY *= -1

        screen.blit(e.I, (e.x + me.X, e.y + me.Y))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(e.x + me.X - 10, e.y + me.Y - 20, e.s[0], 10))
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(e.x + me.X - 10, e.y + me.Y - 20, e.s[0]*e.H[0]/e.H[1], 10))

def draw7():
    global Py, Px, chosen
    screen.blit(arenaIMG, ((w - ArenaSize[0]) // 2 + Px, (h - ArenaSize[1]) // 2 + Py))
    # for e in chosen:
    #     if e.X < (w - ArenaSize[0] - e.s[0]) // 2:
    #         e.X = (w - ArenaSize[0] - e.s[0]) // 2 + 1
    #         e.EX *= -1
    #     elif e.X > (w + ArenaSize[0] - e.s[0]) // 2:
    #         e.X = (w + ArenaSize[0] - e.s[0]) // 2 - 1
    #         e.EX *= -1
    #     if e.Y < (h - ArenaSize[1] - e.s[1]) // 2:
    #         e.y = (h - ArenaSize[1] - e.s[1]) // 2 + 1
    #         e.EY *= -1
    #     elif e.Y > (h + ArenaSize[1] - e.s[1]) // 2:
    #         e.Y = (h + ArenaSize[1] - e.s[1]) // 2 - 1
    #         e.EY *= -1
    #
    #     screen.blit(e.I, (e.x + me.X, e.y + me.Y))
    #     pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(e.x + me.X - 10, e.y + me.Y - 20, e.s[0], 10))
    #     pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(e.x + me.X - 10, e.y + me.Y - 20, e.s[0]*e.H[0]/e.H[1], 10))


def arrowmov():
    for e in arrows:
        e.X += e.SX
        e.Y += e.SY
        e.x = int(e.X)
        e.y = int(e.Y)
mobspd=0.8
def playerdown():
    global me,enearrow,allyarrow,arrows,moving,mobspd,arena,chosen
    if arena==1:
        winfight(0)
        chosen=[]
    holo = 1000
    mobspd=0.8
    arrows=[]
    moving=0
    enearrow=[]
    allyarrow=[]
    for e in mobs:
        e.H[0]=e.H[1]
    while holo > 0:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    holo -=20
                if event.mod & pygame.KMOD_ALT:
                    if event.key == pygame.K_F4:
                        raise SystemExit
        screen.fill((255, 0, 0))
        distacoo=font.render("press f to pay respects to yourself and respawn faster", True, (0,0,0))
        screen.blit(distacoo, (300, h//1.7))
        dista = flont.render("YOU DEAD, RESPAWN IN " + str(int(holo)), True, (0, 0, 0))
        screen.blit((dista), (10, h//2))
        pygame.display.update()
        holo -= 0.5
    me.H[0] = me.H[1]+10000000000
def arrowkill():
    global me, arrows, allyarrow, enearrow, mobs
    for e in arrows:
        if not borderY[0]-500 < e.Y + me.Y < borderY[1]+500:
            arrows.remove(e)
            if e in allyarrow:
                allyarrow.remove(e)
            else:
                enearrow.remove(e)
            e.kill
        elif not borderX[0]-500 < e.X + Px < borderX[1]+500:
            arrows.remove(e)
            if e in allyarrow:
                allyarrow.remove(e)
            else:
                enearrow.remove(e)
            e.kill
    for e in enearrow:
        if e.ST[0] < 1:
            if e.X + Px - e.s[0] // 2 < w // 2 < e.X + Px + e.s[0] // 2:
                if e.Y + Py - e.s[1] // 2 < h // 2 < e.Y + Py + e.s[1] // 2:
                    if e.dmg>PPARMR:
                        me.H[0] -= (e.dmg-PPARMR)/(8+max(PPARMR,0)/10)*8
                        if me.H[0]<0:
                            playerdown()
                    e.P -= 1
                    if e.P == 0:
                        arrows.remove(e)
                        enearrow.remove(e)
                        e.kill
                    else:
                        e.ST[0] = e.ST[1]
        else:
            e.ST[0] -= 1
    for e in allyarrow:
        if e.ST[0] == 0:
            if arena == 1:
                dudes = chosen
            else:
                dudes = mobs
            for b in dudes:
                if b.trueS==0:
                    trues=b.s
                else:
                    trues = b.trueS
                if distanceM(e.X, e.Y, b.X + b.trueX + trues[0] // 2, b.Y + b.trueY + trues[1] // 2,
                             (trues[1] + trues[0] + e.s[0] + e.s[1]) / 4):
                    b.H[0] -= e.dmg
                    if b.H[0] < 0:
                        gar = [c for c in timedstuffs]
                        for a in gar:
                            if b.ID == a.ID:
                                timedstuffs.remove(a)
                        gar = []
                        mobs.remove(b)
                        if arena == 1:
                            chosen.remove(b)
                            if chosen == []:
                                winfight()
                        else:
                            lootem(b)
                        b.kill
                    e.P -= 1
                    if e.P == 0:
                        arrows.remove(e)
                        allyarrow.remove(e)
                        e.kill
                    else:
                        e.ST[0] = e.ST[1]
            dudes = []
        else:
            e.ST[0] -= 1


cooldown = 0


def mobmov():
    global me
    for e in mobs:
        if (not e.H[0] == e.H[1]) or e in chosen:
            rota = distanceC(e.X + Px + e.s[0] // 2, e.Y + e.s[1] // 2 + Py, w // 2, h // 2)
            if rota < 1500 or arena==1:
                if e.attacking == 0:
                    if rota < e.s[0] // 4+e.s[1] // 4:
                        e.attacking = 1
                        timedstuffs.append(timer(MobAttack, ti + 10, [e, 1], e.ID))
                        timedstuffs.sort(key=bythetime)
                xSo = (w / 2) - (e.x + e.s[0] / 2 + me.X)
                ySo = (h / 2) - (e.y + e.s[1] / 2 + me.Y)
                if xSo == 0:
                    spdx = e.S[0]
                    spdy = 0
                else:
                    spdx = e.S[0] / math.sqrt(ySo ** 2 / xSo ** 2 + 1)
                    if xSo < 0:
                        spdx *= -1
                    spdy = spdx * ySo / xSo
                e.EX = spdx
                e.EY = spdy
                if e.EX > 0:
                    if e.fliped == 0:
                        e.fliped = 1
                        e.I = pygame.transform.flip(e.I, True, False)
                elif e.fliped == 1:
                    e.I = pygame.transform.flip(e.I, True, False)
                    e.fliped = 0
            elif not arena == 1:
                e.H[0] = e.H[1]
        else:
            e.tired[0] -= 1
            if e.tired[0] == 0:
                e.tired[0] = e.tired[1]
                e.EX = (random.uniform(-e.S[0], e.S[0]))/2
                e.EY = (random.uniform(-e.S[0], e.S[0]))/2
                if e.EX > 0:
                    if e.fliped == 0:
                        e.fliped = 1
                        e.I = pygame.transform.flip(e.I, True, False)
                elif e.fliped == 1:
                    e.I = pygame.transform.flip(e.I, True, False)
                    e.fliped = 0
        e.X += e.EX*min((time.time() - start_time)*70,5)*2*mobspd
        e.Y += e.EY*min((time.time() - start_time)*70,5)*2*mobspd
        e.x = int(e.X)
        e.y = int(e.Y)

arena = 0
chosen = []
money = 0
loot = []

def distanceC(eneX, eneY, bulX, bulY):
    distance = math.sqrt((math.pow(eneX - bulX, 2)) + (math.pow(eneY - bulY, 2)))
    return distance


def distanceM(eneX, eneY, bulX, bulY, o):
    distance = math.sqrt((math.pow(eneX - bulX, 2)) + (math.pow(eneY - bulY, 2)))
    # distancoo=font.render(str(distance), True, (0,0,0))
    # screen.blit((distancoo), (10, 60))
    if distance < o:
        return True

def winfight(lootit=0):
    global me, arena, Px, Py, loot, money, borderX, borderY, borderXX, borderYY
    arena = 0
    me.Y = PY1
    me.X = PX1
    Py = PY1
    Px = PX1
    borderX = [0, w]
    borderY = [0, h]
    borderXX = [-20000, 20000]
    borderYY = [-20000, 20000]
    if lootit==1:
        for e in loot:
            if isinstance(e, list):
                if isinstance(e[0], int):
                    ActiveWeapon.append(Weapon(e[0], e[1], e[2], e[3], e[4], e[5], e[6],e[7]))
                else:
                    unActivearmor.append(Armor(e[0], e[1], e[2], e[3], e[4],e[5],e[6]))
            else:
                money += e
    loot = []
    me.H[0] = me.H[1]


def lootem(ene):
    global loot, money
    loot.append(ene.loot)
    for e in loot:
        if isinstance(e, list):
            if isinstance(e[0], int):
                ActiveWeapon.append(Weapon(e[0], e[1], e[2], e[3], e[4], e[5],e[6],e[7]))
            else:
                unActivearmor.append(Armor(e[0], e[1], e[2], e[3], e[4],e[5],e[6]))
        else:
            money += e
    loot = []
def equippedArmr(armor):
    global PATC, Activearmor, Activearmor, PlayerSize, PSPECIAL,Patcsped,me,PASPE,PARMR,PPARMR
    armor.item[2] = pygame.transform.smoothscale(armor.item[2],
                                                  (int(armor.item[4] * 1.25), int(armor.item[5] * 1.25)))
    PARMR+=armor.A
    PPARMR += armor.PA
    me.H[0]+=armor.H
    me.H[1] += armor.H
    armor.item[3] = -1
    if not armor.SPE == []:
        PASPE.append(hand)
    armor.item[0] = int(w * 0.025)
    armor.item[1] = int(h * 0.345)
    Activearmor.append(armor)
    unActivearmor.remove(armor)
PASPE=[]
unActivearmor=[]
Activearmor=[]

def unequippedArmr(bo):
    global me, unActivearmor,Activearmor,PASPE, PARMR,PPARMR
    unActivearmor.append(bo)
    Activearmor.remove(bo)
    me.H[0]-=bo.H
    me.H[1] -= bo.H
    PARMR -= bo.A
    PPARMR -= bo.PA
    if not bo.SPE == []:
        if bo.SPE in PASPE:
            PASPE.remove(bo.SPE)
        else:
            print('for sum reason the special of ' + str(e) + 'is not in PASPE')
    bo.item = [e for e in bo.saveo]

def unequippedweapon(bo, hand):
    global PATC,Patcsped
    ActiveWeapon.append(bo)
    PATC[hand] -= bo.A
    Patcsped[hand*-1+1] -= bo.speed
    if not bo.SPE == []:
        if bo.SPE in PSPECIAL:
            PSPECIAL.remove(bo.SPE)
        else:
            print('for sum reason the special of ' + str(e) + 'is not in PSPE')
    PRange[hand] -= bo.R // 2
    bo.item = [e for e in bo.saveo]
    ActiveWeaponer.remove(bo)


def equippedweapon(weapon, hand):
    global PATC, ActiveWeapon, ActiveWeaponer, PlayerSize, PSPECIAL,Patcsped
    PATC[hand] += weapon.A
    PRange[hand] += weapon.R // 2
    weapon.item[2] = pygame.transform.smoothscale(weapon.item[2],
                                                  (int(weapon.item[4] * 1.25), int(weapon.item[5] * 1.25)))
    Patcsped[hand*-1+1] += weapon.speed
    weapon.item[3] = -1
    if not weapon.SPE == []:
        weapon.SPE[2] = hand
        PSPECIAL.append(weapon.SPE)
    if hand == 0:
        weapon.hand = 2
        weapon.I = pygame.transform.flip(weapon.i, True, False)
        weapon.X = [int(-weapon.X[2]), int(-weapon.X[2]), weapon.X[2]]
        weapon.item[0] = int(w * 0.232)
        weapon.item[1] = int(h * 0.73)
    else:
        weapon.I = weapon.i
        weapon.hand = 1
        weapon.X = [weapon.X[2], weapon.X[2], weapon.X[2]]
        weapon.item[0] = int(w * 0.125)
        weapon.item[1] = int(h * 0.73)
    ActiveWeaponer.append(weapon)
    ActiveWeapon.remove(weapon)


breakme = 0
ActiveWeaponer = []
EquipMen = pygame.transform.smoothscale(img('EquipMen.png'), (w, h))
bl = 0
holding = 0
biggafish = img("man.png")
stot=img("weaponstater.png")

def menu():
    global breakme, ActiveWeapon, ActiveWeaponer, PATC, holding,unActivearmor
    allposdown=0
    blobl=3
    while True:
        XX = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    allposdown+=blobl
                elif event.button == 5:
                    allposdown -= blobl
                elif event.button == 1:
                    if holding == 0:
                        for e in items:
                            if e.item[0]<w*0.45:
                                positiongrab=0
                            else:
                                positiongrab = allposdown
                            if distanceM(e.item[0] + e.item[4] / 2, e.item[1]+positiongrab + e.item[5] / 2, XX[0], XX[1], 80):
                                if e.item[3] < 0:
                                    e.item[3] -= 1
                                    e.item[3] *= -1
                                else:
                                    e.item[3] = 1
                                holding = 1
                                break
                    else:
                        holding = 0
                        for e in items:
                            if e.item[3] > 0:
                                if XX[0] > w * 0.4:
                                    if e in Activearmor:
                                        unequippedArmr(e)
                                    elif e in ActiveWeaponer:
                                        if e.hand == 2:
                                            e.hand = 0
                                        unequippedweapon(e, e.hand)
                                    e.item[3] = 0
                                    break
                                elif XX[0] < w * 0.2:
                                    if e in unActivearmor or e in Activearmor:
                                        for b in Activearmor:
                                            unequippedArmr(b)
                                        equippedArmr(e)
                                    else:
                                        if e in ActiveWeaponer:
                                            if e.hand == 1:
                                                e.item[3] = 0
                                                break
                                            else:
                                                unequippedweapon(e, 0)
                                        for b in ActiveWeaponer:
                                            if b.hand == 1:
                                                unequippedweapon(b, 1)
                                        equippedweapon(e, 1)
                                        break
                                    break
                                else:
                                    if e in unActivearmor or e in Activearmor:
                                        for b in Activearmor:
                                            unequippedArmr(b)
                                        equippedArmr(e)
                                    else:
                                        if e in ActiveWeaponer:
                                            if e.hand == 2:
                                                e.item[3] = 0
                                                break
                                            else:
                                                unequippedweapon(e, 1)
                                        for b in ActiveWeaponer:
                                            if b.hand == 2:
                                                unequippedweapon(b, 0)
                                        equippedweapon(e, 0)
                                    break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    breakme = 1
                if event.mod & pygame.KMOD_ALT:
                    if event.key == pygame.K_F4:
                        raise SystemExit
                if event.key == pygame.K_KP_PLUS:
                    blobl+=100
                if event.key == pygame.K_KP_MINUS:
                    blobl-=100
        screen.fill((182, 182, 182))
        if breakme == 1:
            for e in items:
                if e.item[3] == 1:
                    e.item[3] = 0
                    holding = 0
                    break
            breakme = 0
            break
        for g in items:
            if g.item[3] < 1:
                if g.item[0]>w*0.45:
                    screen.blit(g.item[2], ((g.item[0], g.item[1]+allposdown)))
        if holding==0:
            for g in items:
                if g.item[3] < 1:
                    if g.item[0] > w * 0.45:
                        if distanceC(g.item[0] + g.item[4] // 2, g.item[1] + allposdown + g.item[5] // 2, XX[0],XX[1]) < g.item[4] // 2:
                            screen.blit(stot, (1100+15, g.item[1]+15 + allposdown))
                            stats = funt.render(str(g.name[0]), True, (0, 0, 0))
                            screen.blit(stats, (1100 + 10 + 15, g.item[1] + 15 + allposdown + 50))
                            blit_text(g.name[1], [1100 + 10 + 15, g.item[1] + 15 + allposdown + 200], font, w * 0.85)
                            if g in unActivearmor:
                                stats = font.render('health: ' + str(int(g.H)), True, (0, 0, 0))
                                screen.blit(stats, (1100+15 +10, g.item[1]+15 + allposdown +125))
                                stats = font.render('armour: ' + str(int(g.A)), True, (0, 0, 0))
                                screen.blit(stats, (1100+15 + +10, g.item[1]+15 + allposdown +150))
                                stats = font.render('spell armour: ' + str(int(g.PA)), True, (0, 0, 0))
                                screen.blit(stats, (1100+15 + +10, g.item[1]+15 + allposdown +175))
                            else:
                                stats = font.render('attack: ' + str(int(g.A)), True, (0, 0, 0))
                                screen.blit(stats, (1100+10+15, g.item[1]+15 + allposdown +125))

        screen.blit(EquipMen, (0, 0))
        screen.blit(biggafish, (int(w * 0.15), int(h * 0.03)))
        for g in items:
            if g.item[3] < 1:
                if g.item[0]<w*0.45:
                    screen.blit(g.item[2], ((g.item[0], g.item[1])))
            else:
                screen.blit(g.item[2], ((XX[0] - g.item[4] // 2, XX[1] - g.item[5] // 2)))

        draw00(0)
        stats = font.render('attack: ' + str(int(PATC[1])) + ',' + str(int(PATC[0])), True, (0, 0, 0))
        screen.blit(stats, ((15, 800)))
        stats = font.render('health: ' + str(int(me.H[0])) + '/' + str(int(me.H[1])), True, (0, 0, 0))
        screen.blit(stats, ((15, 825)))
        stats = font.render('money: ' +str(int(money)), True, (0, 0, 0))
        screen.blit(stats, ((15, 850)))
        stats = fpont.render('physical armour: ' +str(int(PARMR)), True, (0, 0, 0))
        screen.blit(stats, ((15, 875)))
        stats = fpont.render('spell armour: ' +str(int(PPARMR)), True, (0, 0, 0))
        screen.blit(stats, ((15, 895)))
        pygame.display.update()

def getarmor(theitem):
    theitem = theitem[0]
    unActivearmor.append(Armor(theitem[0], theitem[1], theitem[2], theitem[3], theitem[4],theitem[5],theitem[6]))
def getweapon(theitem):
    theitem = theitem[0]
    ActiveWeapon.append(Weapon(theitem[0], theitem[1], theitem[2], theitem[3], theitem[4], theitem[5],theitem[6],theitem[7]))

book = img('book.png')
beefbook = img('sandwich.png')
moobIMG=pygame.transform.smoothscale(img('moobIMG.png'), (w, h))
fioght = img('fight.png')
killrog=0
def mobbin(mooob):
    global breakme, buttons,moobs,killrog,Py
    breakme = 0
    buttons.append(button(int(w * .5), int(h * 0.88), fioght, 0,
                          [0]))
    while True:
        XX = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for e in buttons:
                    if XX[0] + e.s[0] // 2 > e.X > XX[0] - e.s[0] // 2:
                        if XX[1] + e.s[1] // 2 > e.Y > XX[1] - e.s[1] // 2:
                            killrog=1
                            buttons.remove(e)
                            e.kill
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    breakme = 1
                if event.mod & pygame.KMOD_ALT:
                    if event.key == pygame.K_F4:
                        raise SystemExit
        if breakme == 1:
            Py-=200
            breakme = 0
            buttons = []
            break
        screen.fill((0, 0, 0))
        screen.blit(moobIMG, ((0, 0)))
        draw00(0)
        if killrog==1:
            mooob.enter()
            for e in mooob.enemies:
                mobs.append(e)
            loot.append(mooob.d*5)
            fight(mooob.enemies)
            r = requests.post('http://' + ipadress + ':5000/MoobUpdate', headers=headers,
                              data=jsonpickle.encode([mooob.ID, me.ID]))
            shoops = jsonpickle.decode(r.text)
            moobs.append(moob(shoops.X, shoops.Y, mobtile, shoops.ID, shoops.enemies,shoops.difficulty))
            moobs.remove(mooob)
            mooob.kill
            killrog=0
            buttons = []
            break

        pygame.display.update()

def shoppin():
    global breakme, ActiveWeapon, ActiveWeaponer, PATC, holding, buttons, money, weapons
    breakme = 0
    bok=random.randint(0,100)
    if bok==100:
        buttons.append(button(int(w * .78), int(h * 0.78), beefbook, SANDWICH,
                              [500, [1, 0, 0, 2, 0], ['Shopkeeper\'s sandwich', 'my sandwich? fine it is yours for 500 gold']]))
    else:
        buttons.append(button(int(w * .78), int(h * 0.78), book, atcP,
                              [10, [1, 0, 0, 2, 0], ['Book of war', '+1 atttack!, how amazing']]))
    for e in range(3):
        weaponsRANDOM(0)
        purchase = weapons[random.randint(0, len(weapons) - 1)]
        buttons.append(button(int(w * 0.15 * e + w * 0.3), int(h * 0.78), purchase[2][1], getweapon,
                              [purchase[6], [purchase], purchase[7]]))
    weaponsRANDOM(0)
    purchase = armors[random.randint(0, len(armors) - 1)]
    buttons.append(button(int(w * 0.37), int(h * 0.258), purchase[0][1], getarmor,
                          [purchase[5], [purchase], purchase[6]]))
    while True:
        XX = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for e in buttons:
                    if XX[0] + e.s[0] // 2 > e.X > XX[0] - e.s[0] // 2:
                        if XX[1] + e.s[1] // 2 > e.Y > XX[1] - e.s[1] // 2:
                            if money > e.Fin[0] - 1:
                                money -= e.Fin[0]
                                e.F(e.Fin[1])
                                buttons.remove(e)
                                e.kill
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    breakme = 1
                if event.mod & pygame.KMOD_ALT:
                    if event.key == pygame.K_F4:
                        raise SystemExit
        if breakme == 1:
            breakme = 0
            buttons = []
            break
        screen.fill((0, 0, 0))
        screen.blit(shopIMG, ((0, 0)))
        stats = font.render('Money: ' + str(money), True, (220, 170, 0))
        screen.blit(stats, ((15, 1005)))
        draw00(1)
        pygame.display.update()


shopIMG = pygame.transform.smoothscale(img('shopkeeper.png'), (w, h))
def fight(ene):
    global loot, PX1, PY1, chosen, arena, ArenaSize, me, Px, Py, borderX, borderY, borderXX, borderYY, mobs, PSPE, PXSPD, PYSPD
    for e in ene:
        loot.append(e.loot)
        chosen.append(e)
    PXSPD = 0
    PYSPD = 0
    PX1 = me.X
    PY1 = me.Y
    me.X = 0
    me.Y = 0
    Px = 0
    Py = 0
    for e in mobs:
        e.H[0] = e.H[1]
    arena = 1
    ArenaSize = arenaIMG.get_size()
    borderXX = [-(ArenaSize[0] - PlayerSize[0]) // 2 - w // 2, (ArenaSize[0] - PlayerSize[0]) // 2 - w // 2]
    borderYY = [-(ArenaSize[1] - PlayerSize[1]) // 2 - h // 2, (ArenaSize[1] - PlayerSize[1]) // 2 - h // 2]



color = [0, 0, 0]
texts = []
borderX = [0, w]
borderY = [0, h]
newsii = ['Man dies to supervillan, but manages to survive, because seriously who ever died to supervillans?',
          'Some fat-ass woman ate ' + str(random.randint(10000000,
                                                         1000000000)) + ' megatonnes of icecream. Dont worry, yo momma still holds the record...',
          'Today nothing happened... This event of nothingness killed 1000 people because of pure shock.',
          'The news reporter is an idiot. He also cant see this.',
          'have you seen the cant and didnt? thats because I cant be bothered.',
          'Art critics shocked after discovering that the famous red dot actually contains no symbolism whatsoever.',
          'Profiter Velen got loads of stonks by selling draenei to the burning legion.',
          'Grass can be very dangerous.', 'The following message is a lie in at least one way:',
          'the boulderfist ogre guarantees a win because of stats', 'avoid death, unlike all the enemy mobs...',
          'I eat people, says the man-eater we interviewed. How surprising.',
          'Are you ugly? Makeup cant save you? Buy our face-ripper with a 75percent dicount and get your money stolen for free!',
          'In the end, death claims us all. So claims the undead, soon-to-be tripledead, doubledead lady.',
          'POKEMON says you should enslave all the pokemon. Our reporter says: uhhhh...',
          'Newton says: gravity mon... it exists.',
          'The melon is squishing grapes... you shoudnt have let yo momma get out the house.',
          'Breaking news! scientists have discoverded how telepo- HEY! stop looking at that cat video for a damn second, this is- nevermind',
          'Illidan got squashed by sargeras and is now getting eaten by an imp.',
          'Ha, that idiot says he is an attack helicopter!            Oh no, he IS an attack helicopter! RUN!',
          'Wait a second whilst we kick this gnome', ':)',
          'John Johnson has stolen from Innocent Mc.Notsuspicious, who was carrying a bomb, and got proclaimed a saint.',
          'Sum dude convinced a whole city to go kill themselves. How? charisma hat.',
          'Physicists have concluded that nothing makes sense and went bankrupt.',
          'does the reporter ever move? ... I mean I dont think so...',
          'this is an escort the text to the end quest so you betteer alt-F4. H  e  l  l  o  w    a  d  v  e  n  t  u  r  e  r    p  l  e  a  s  e    s  a  v- ok, I think hes gone',
          'Have you ever seen anyone insult the magnificent Dudelandia.py? Of course not, its too good!           ...if you have please give their adress to murder-dude, he lives on 21 W. Pacific St.Dude, TX 77904.',
          'the lotto numbers are  ' + str([random.randint(1, 9), random.randint(1, 9), random.randint(1, 9),
                                           random.randint(1,
                                                          9)]) + ' if you have these numbers then please go to 21 W. Pacific St.Dude, TX 77904.',
          'We made newspapers in the past, but the printers...ugh', '!enod llew',
          'The reporter is not wearing pants, which is of course, normal.',
          'Why do robbers use a sack for the money? and why the blindfold with holes? It immediatly identifies you as a robber and seems so fiddly...   I just use a vaccum cleaner and shrek mask.',
          'the police arrested an acorn, still better than when they arrested my sandwich last tuesday I guess...',
          'There is a dude for every need, even pointlessly killing everything that can be killed, Oh wait, thats you',
          'Justice dude killed himself, what does that mean?',
          'Ages ago The Overdude forged this world, melting these grasslands on the top of The great abbys, granting us the gift of space and unlimited material...',
          'Spears that are pointless are utterly pointless.']
newses = [e for e in newsii]
vvv = 0
destnd = ([color[0], random.choice([0, 150, 255])], [color[1], random.choice([0, 150, 255])],
          [color[2], random.choice([0, 150, 255])])
headlines = random.randint(0, (len(newses) - 1))
texts.append(text(1300, 895, fontBG.render(newses[headlines], True, (0, 0, 0))))
newses.remove(newses[headlines])
for d in texts:
    vvv = d.X + 25 + d.s[0]
headlines = random.randint(0, (len(newses) - 1))
texts.append(text(150 + vvv, 895, fontBG.render(newses[headlines], True, (0, 0, 0))))
newses.remove(newses[headlines])
for d in texts:
    vvv = d.X + 25 + d.s[0]
headlines = random.randint(0, (len(newses) - 1))
texts.append(text(150 + vvv, 895, fontBG.render(newses[headlines], True, (0, 0, 0))))
newses.remove(newses[headlines])
playbutton = pygame.transform.smoothscale(img('playbutton.png'), (int(w / 4.5), int(h / 4.5)))


def breaker(f):
    global breakme
    breakme = 1


buttons.append(button(w * 0.82, h * 0.8, playbutton, breaker, []))
vvv = 0
ggggg = 0
r = requests.get('http://'+ipadress+':5000/shoppos')
shoops = jsonpickle.decode(r.text)
shops=[]
for e in shoops:
    shops.append(tile(e.X,e.Y,shoptile,e.ID))

r = requests.get('http://'+ipadress+':5000/mobbos')
mooobs = jsonpickle.decode(r.text)
moobs=[]
for e in mooobs:
    moobs.append(moob(e.X,e.Y,mobtile,e.ID,e.enemies,e.difficulty))

while True:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            XX = pygame.mouse.get_pos()
            for e in buttons:
                if XX[0] + e.s[0] // 2 > e.X > XX[0] - e.s[0] // 2:
                    if XX[1] + e.s[1] // 2 > e.Y > XX[1] - e.s[1] // 2:
                        e.F(e.Fin)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                breakme = 1
            if event.mod & pygame.KMOD_ALT:
                if event.key == pygame.K_F4:
                    raise SystemExit
    screen.fill((int(color[0]), int(color[1]), int(color[2])))
    if breakme == 1:
        breakme = 0
        break
    goy = 0
    for e in destnd:
        if e[0] < e[1]:
            e[0] += 0.5
        elif e[0] > e[1]:
            e[0] -= 0.5
        else:
            e[1] = random.choice([0, 150, 255])
        color[goy] = e[0]
        goy += 1
    for e in texts:
        screen.blit(e.I, ((e.X, e.Y)))
        e.X -= 0.7

    for e in texts:
        if e.X < 50 - e.s[0]:
            texts.remove(e)
            e.kill
            del e
            for d in texts:
                vvv = d.X + 25 + d.s[0]
            if newses == []:
                newses = [e for e in newsii]
            headlines = random.randint(0, (len(newses) - 1))
            texts.append(text(150 + vvv, 895, fontBG.render(newses[headlines], True, (0, 0, 0))))
            newses.remove(newses[headlines])
            vvv = 0
    screen.blit(news, ((0, 0)))
    draw00(0)
    pygame.display.update()
buttons = []
for e in range(8):
    for I in range(13):
        tiles.append(tile(-400 + 200 * I, -400 + 200 * e, grases[random.randint(0, 4)]))

borderXX = [-20000, 20000]
borderYY = [-20000, 20000]
texts = []
atttacksIMG = [img("R1.png"), img("R2.png"), img("L1.png"), img("L2.png"), img("man2.png")]
###########################################################################
nows = 0
def heal(nobodycares,amount,nomatter):
    global me
    # [health to [0],health to [1]]
    me.H[1]+=amount[1]
    me.H[0] += amount[0]
sandw=img("sand.png")
def SANDWICH(nomatter):
    global me, ActiveWeapon
    # X, Y, I, A,speed, SPE, cost
    #[0, 25, luck * 0.5 + luck ** 2 * 0.05, 1, -1,
     #pygame.transform.smoothscale(bullet, (int(30 * bigmult), int(15 * bigmult)))]]
    ActiveWeapon.append(Weapon(-50, 40, [sandw,beefbook], 1, 0, [[2], 1, 1, 0, heal, [100,1]], 500,"Sandwich"))
def atcP(multipliar):
    # multipliar(amount,way),timee,hand,first
    global PATC
    if multipliar[3] < 2:
        if multipliar[1] == 1:
            PATC[multipliar[3]] += multipliar[0]
            multnew = -multipliar[0]
        else:
            PATC[multipliar[3]] *= multipliar[0]
            multnew = 1 / multipliar[0]
    elif multipliar[1] == 0:
        PATC[0] += multipliar[0]
        PATC[1] += multipliar[0]
        multnew = -multipliar[0]
    else:
        PATC[0] *= multipliar[0]
        PATC[1] *= multipliar[0]
        multnew = 1 / multipliar[0]
    if multipliar[4] == 1:
        timedstuffs.append(timer(atcP, multnew, ti + multipliar[2], multipliar[3], 0))
        timedstuffs.sort(key=bythetime)



mobs.append(mob(700, 600, [img('man2.png'), []], 0, 'man', [], 100, [1, 1], 150, weapons[2]))
weaponsRANDOM(0)


def MobAttack(t, f):
    # t=time sprite, f=[the mob,the faze], mabe usable t.power[0]=the mob also... but unchanged by changes in the original...probably
    rolll = len(f[0].atcs)
    t.T += f[0].atcspd
    timedstuffs.sort(key=bythetime)
    f[1] += 1
    if rolll > f[1] - 2:
        f[0].I = f[0].atcs[f[1] - 2]
        f[0].fliped = 1
        pastfart = f[0].s
        f[0].s = f[0].I.get_size()
        f[0].X -= (f[0].s[0] - pastfart[0]) // 2
        f[0].Y -= (f[0].s[1] - pastfart[1]) // 2
        if distanceM(f[0].X + Px + f[0].s[0] // 2, f[0].Y + f[0].s[1] // 2 + Py, w // 2, h // 2,
                     (PlayerSizecrpd[1] + PlayerSizecrpd[0]) / 4 + (f[0].s[0] + f[0].s[1]) / 4):
            if f[0].A[0]>PARMR:
                me.H[0] -= (f[0].A[0]-PARMR)/(8+max(PARMR,0)/10)*8
                if me.H[0]<1:
                    playerdown()
        for e in range((len(f[0].SPE)) // 2):
            if f[1] in f[0].SPE[e * 2 - 1][0]:
                f[0].SPE[e * 2 - 2](f[0], f[0].SPE[e * 2 - 1], f[1])
    elif rolll < f[1] - 2:
        f[0].attacking = 0
        timedstuffs.remove(t)
        t.kill
        del t
    else:
        f[0].I = f[0].i
        if (f[0].X + f[0].s[0] // 2 + Px > w // 2):
            f[0].I = pygame.transform.flip(f[0].I, True, False)
        pastfart = f[0].s
        f[0].s = f[0].I.get_size()
        f[0].X -= (f[0].s[0] - pastfart[0]) // 2
        f[0].Y -= (f[0].s[1] - pastfart[1]) // 2
dpressed = 0
apressed = 0
# def flipmob(self,uuu):
#     global timedstuffs
#     for e in mobs:
#         if e.EX>0:
#             if e.fliped==0:
#                 e.fliped=1
#                 e.I = pygame.transform.flip(e.I, True, False)
#         elif e.fliped==1:
#             e.I = pygame.transform.flip(e.i, True, False)
#             e.fliped =0
#     self.T+=200
#     timedstuffs.sort(key=bythetime)
#timedstuffs.append(timer(flipmob, ti, [0, False], 0))
def atcright(a, f):
    global playerIMG, arena, ActiveWeaponer, ActiveWeapon, cooldown,timedstuffs
    a.power[0] += 1
    if a.power[0] == 3:
        for c in ActiveWeaponer:
            c.X[0] = c.X[1]
            c.Y[0] = c.Y[1]
            c.I = c.i
            if c.hand == 2:
                c.I = pygame.transform.flip(c.I, True, False)
            c.s = c.I.get_size()
        if dpressed == 1:
            timedstuffs.append(timer(atcright, ti, [0, False], 0))
            timedstuffs.sort(key=bythetime)
            cooldown = Patcsped[1] * 2+1
        elif apressed == 1:
            timedstuffs.append(timer(atcright, ti, [0, True], 0))
            timedstuffs.sort(key=bythetime)
            cooldown = Patcsped[0] * 2+1
        playerIMG = atttacksIMG[4]
        timedstuffs.remove(a)
        a.kill
        del a
    else:
        if a.power[1] == 0:
            playerIMG = atttacksIMG[1 + a.power[0]]
            for c in ActiveWeaponer:
                if c.hand == 2:
                    if a.power[0] == 2:
                        c.Y[0] += 55
                    else:
                        c.X[0] += 45
                        c.Y[0] -= 150
                    c.I = pygame.transform.rotate(c.i, 35 * a.power[0])
                    c.I = pygame.transform.flip(c.I, True, False)
                    c.s = c.I.get_size()
        else:
            playerIMG = atttacksIMG[a.power[0] - 1]
            for c in ActiveWeaponer:
                if c.hand == 1:
                    if a.power[0] == 2:
                        c.Y[0] += 55
                    else:
                        c.X[0] -= 45
                        c.Y[0] -= 150
                    c.I = pygame.transform.rotate(c.i, 35 * a.power[0])
                    c.s = c.I.get_size()
        if arena == 1:
            participants = chosen
            uuu = 1
        else:
            participants = mobs
            uuu = 2
        for b in range(len(PSPECIAL)):
            if not PSPECIAL[b][1] == 0:
                if a.power[0] in PSPECIAL[b][0]:
                    if a.power[1] == PSPECIAL[b][2]:
                        PSPECIAL[b][4]('mouse', PSPECIAL[b][5], a.power[0])
        for e in participants:
            if not (e.X + e.s[0] // 2 + Px > w // 2) == a.power[1]:
                e.x + me.X, e.y + me.Y
                firsthit = 0
                if e.trueS==0:
                    truess=e.s
                else:
                    truess = e.trueS
                if distanceM(e.X + e.trueX + Px + truess[0] // 2, e.Y + e.trueY + truess[1] // 2 + Py, w // 2, h // 2,
                             (truess[0] + truess[1]) // 4 + PRange[a.power[1]]):
                    firsthit += 1
                    if arena==3:
                        e.A[0]+=PATC[a.power[1]]
                    else:
                        e.H[0] -= PATC[a.power[1]]
                    for b in range(len(PSPECIAL)):
                        if not PSPECIAL[b][1] == 1:
                            if PSPECIAL[b][3] > firsthit:
                                if a.power[0] in PSPECIAL[b][0]:
                                    if a.power[1] == PSPECIAL[b][2]:
                                        PSPECIAL[b][4](e, PSPECIAL[b][5], a.power[0])
                            # the zero means its not a condition, player specials[which special?](mob,the specials specific variables, the faze of the attack)
                    if e.H[0] < 1:
                        gar = [c for c in timedstuffs]
                        for b in gar:
                            if e.ID == b.ID:
                                timedstuffs.remove(b)
                        gar = []
                        if uuu == 1:
                            chosen.remove(e)
                            if chosen == []:
                                winfight()
                        else:
                            lootem(e)
                        mobs.remove(e)
        a.T += Patcsped[a.power[1] * -1 + 1]
        timedstuffs.sort(key=bythetime)
    participants = []


###########################################################################
functionlist = [atcright, MobAttack, atcdown, spdup]
running = True
moving=0
posofmousa = [10000000, 10000000]
def moobreplace(Replacement):
    #[the id of the replaced moob, the replacement moob]
    global moobs
    for e in moobs:
        if e.ID==Replacement[0]:
            moobs.remove(e)
            break
    moobs.append(moob(Replacement[1].X,Replacement[1].Y,mobtile,Replacement[1].ID,Replacement[1].enemies,Replacement[1].difficulty))
def enewin():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.mod & pygame.KMOD_ALT:
                    if event.key == pygame.K_F4:
                        raise SystemExit
        screen.fill((200,0,0))
        dista=flont.render(str("ENEMIES HAVE DESTROYED YOU!"), True, (0,0,0))
        screen.blit((dista), (50, h//2))
        pygame.display.update()
timeout=0
helth=0
#for e in range(200):
    #lootem(genmob(random.randint(1,6)))
# weaponsRANDOM(0)
# for e in range(100):
#     getarmor([armors[random.randint(0,len(armors)-1)]])
#weaponsRANDOM(30)
#for e in range(10):
    #getarmor([armors[ random.randint(0,len(armors)-1) ]])
def Murderkill(lols):
    global loot, PX1, PY1, chosen, arena, ArenaSize, me, Px, Py, borderX, borderY, borderXX, borderYY, PXSPD, PYSPD,arena,mobs
    PXSPD =0
    PYSPD = 0
    mobs=[]
    chosen=[]
    ArenaSize = arenaIMG.get_size()
    me.X = random.randint(-(ArenaSize[0] - PlayerSize[0]) // 2 - w // 2,(ArenaSize[0] - PlayerSize[0]) // 2 - w // 2)
    me.Y = random.randint(-(ArenaSize[1] - PlayerSize[1]) // 2 - h // 2, (ArenaSize[1] - PlayerSize[1]) // 2 - h // 2)
    me.H[0]=me.H[1]
    Px = random.randint(-(ArenaSize[0] - PlayerSize[0]) // 2 - w // 2,(ArenaSize[0] - PlayerSize[0]) // 2 - w // 2)
    Py = random.randint(-(ArenaSize[1] - PlayerSize[1]) // 2 - h // 2, (ArenaSize[1] - PlayerSize[1]) // 2 - h // 2)
    borderXX = [-(ArenaSize[0] - PlayerSize[0]) // 2 - w // 2, (ArenaSize[0] - PlayerSize[0]) // 2 - w // 2]
    borderYY = [-(ArenaSize[1] - PlayerSize[1]) // 2 - h // 2, (ArenaSize[1] - PlayerSize[1]) // 2 - h // 2]
    arena=3
    for e in lols[0]:
        if not e.ID==me.ID:
            mobs.append(mob(700, 700, [playerIMGcrpd, playerIMGcrpd], 0, 'Player',
                            [], 10000, [0,0],50, weapons[4],e.ID,1))
to=0
players=[]
def enedead(didIwin):
    global mobs
    if didIwin[0]==1:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.mod & pygame.KMOD_ALT:
                        if event.key == pygame.K_F4:
                            raise SystemExit
            screen.fill((0, 186, 0))
            dista = flont.render(str("YOU HAVE DEFEATEN THEM ALL!"), True, (0, 0, 0))
            screen.blit((dista), (50, h // 2))
            pygame.display.update()
    else:
        for e in mobs:
            if e.ID == didIwin[1]:
                mobs.remove(e)
timeouter=1
updatelist=[shopreplace,moobreplace,count,Murderkill,enedead]
while running:
    XX = pygame.mouse.get_pos()
    start_time = time.time()
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            moving = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                moving=1
                xS = (XX[0]) - (w / 2)
                yS = (XX[1]) - (h / 2)
                posofmousa = [XX[0] - me.X, XX[1] - me.Y]
            else:
                xS = (w / 2) - (XX[0])
                yS = (h / 2) - (XX[1])
            if xS == 0:
                PXSPD = PSPE
                PYSPD = 0
            else:
                PXSPD = PSPE / math.sqrt(yS ** 2 / xS ** 2 + 1)
                if xS < 0:
                    PXSPD *= -1
                PYSPD = PXSPD * yS / xS
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_ESCAPE:
                menu()
            if event.mod & pygame.KMOD_ALT:
                if event.key == pygame.K_F4:
                    raise SystemExit

            # if event.key == pygame.K_p:
            #     mobs.append(genmob(1))
            #     mobs.append(genmob(2))
            #     mobs.append(genmob(3))
            #     mobs.append(genmob(5))
            #     mobs.append(genmob(4))
            #     mobs.append(genmob(6))
            #     weaponsRANDOM(0)

            # if event.key == pygame.K_t:
            #     mobs.append(genmob(3))
            #     weaponsRANDOM(0)
            if event.key == pygame.K_a:
                apressed = 1
                if cooldown < 1:
                    timedstuffs.append(timer(atcright, ti, [0, True], 0))
                    timedstuffs.sort(key=bythetime)
                    cooldown = Patcsped[0] * 2+1
            # if event.key == pygame.K_k:

            if event.key == pygame.K_d:
                dpressed = 1
                if cooldown < 1:
                    timedstuffs.append(timer(atcright, ti, [0, False], 0))
                    timedstuffs.sort(key=bythetime)
                    cooldown = Patcsped[1] * 2

            # if event.key == pygame.K_i:

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                apressed = 0
            if event.key == pygame.K_d:
                dpressed = 0
            # if event.key == pygame.K_w:
            #   if PYSPD <0:
        #         PYSPD = 0
        #  if event.key == pygame.K_s:
        #    if PYSPD >0:
        #       PYSPD = 0
    screen.fill((200, 0, 0))
    if me.H[0]>me.H[1]:
        me.H[0]-=min(17000000,me.H[0]-me.H[1])
    if arena == 1:
        if to % 300 == 0:
            mobspd+=0.01
        borderX = [(w - ArenaSize[0]) // 2 + Px, (w - ArenaSize[0]) // 2 + Px + ArenaSize[0]]
        borderY = [(h - ArenaSize[1]) // 2 + Py, (h - ArenaSize[1]) // 2 + Py + ArenaSize[1]]
        draw1()
    elif arena==3:
        if int(time.time())>timeouter:
            timeouter = int(time.time())
            timeout+=5
        borderX = [(w - ArenaSize[0]) // 2 + Px, (w - ArenaSize[0]) // 2 + Px + ArenaSize[0]]
        borderY = [(h - ArenaSize[1]) // 2 + Py, (h - ArenaSize[1]) // 2 + Py + ArenaSize[1]]
        draw7()
        for e in players:
            if e.ID != me.ID:
                screen.blit(playerIMG, (e.X + me.X + 895, e.Y + me.Y + 465))
                for b in mobs:
                    if b.ID==e.ID:
                        b.x = int(e.X)+ 895
                        b.y = int(e.Y)+ 465
                        b.X = b.x
                        b.Y = b.y
                        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(b.x + me.X, b.y + me.Y - 20, PlayerSizecrpd[1], 10))
                        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(b.x + me.X, b.y + me.Y - 20, PlayerSizecrpd[1]*e.H[0]/e.H[1], 10))
                        b.helfloss=b.H[1]-b.H[0]
                        b.H[0]=b.H[1]
        r = requests.post('http://'+ipadress+':5000/Dmgdone', headers=headers, data=jsonpickle.encode([[[e.helfloss,e.A[0],e.ID] for e in mobs],me.ID]))
        heh = jsonpickle.decode(r.text)
        heh[0]*=timeout
        heh[1]*= timeout
        if heh[1] > max(0,PARMR):
            me.H[0] -= (heh[1] - PARMR) / (8 + max(PARMR, 0)) / 10
        if heh[0] > max(0,PPARMR):
            me.H[0] -= (heh[0] - PPARMR) / (8 + max(PPARMR, 0)) / 10
        if me.H[0]<0:
            r = requests.post('http://'+ipadress+':5000/playerdeath', headers=headers,
                              data=jsonpickle.encode(me.ID))
            enewin()
        for e in mobs:
            e.A[0]=0
            e.helfloss=0
    else:
        if to % 300 == 0:
            for e in mobs:
                if not borderY[0] - 1500 < e.Y + me.Y < borderY[1] + 1500:
                    mobs.remove(e)
                    e.kill
                elif not borderX[0] - 1500 < e.X + Px < borderX[1] + 1500:
                    mobs.remove(e)
                    e.kill
            for _ in range(10):
                poser=random.randint(1,4)
                if poser==1:
                    xposs=random.randint(-200,w+100)
                    yposs = -1000
                elif poser==2:
                    xposs=random.randint(-200,w+100)
                    yposs = h+200
                elif poser==3:
                    xposs = -1000
                    yposs = random.randint(-100, h + 200)
                else:
                    xposs = w+200
                    yposs = random.randint(-100, h + 100)
                mobs.append(genmob(random.randint(1,6),[xposs-me.X,yposs-me.Y]))
        draw2()
        for e in players:
            if e.ID != me.ID:
                screen.blit(playerIMG, (e.X + me.X + 895, e.Y + me.Y + 465))
        # for e in mobs:
        #     if distanceM(e.X + me.X + e.s[0] // 2, e.Y + me.Y + e.s[1] // 2, w // 2, h // 2, 100):
        #         fight([e])
    r = requests.post('http://' + ipadress + ':5000/PlayerUpdate', headers=headers, data=jsonpickle.encode(me))
    decoded=jsonpickle.decode(r.text)
    newupdates=decoded[1]
    for e in newupdates:
        updatelist[e[0]](e[1])
    players = decoded[0]

    screen.blit(playerIMG, ((w - PlayerSize[0]) // 2, (h - PlayerSize[1]) // 2))
    pygame.draw.rect(screen, (0, 0, 0),
                     pygame.Rect((w - PlayerSizecrpd[0]) // 2 - 50, (h - PlayerSizecrpd[1]) // 2 - 15, PlayerSizecrpd[1], 10))
    pygame.draw.rect(screen, (0, 150, 0),
                     pygame.Rect((w - PlayerSizecrpd[0]) // 2 - 50, (h - PlayerSizecrpd[1]) // 2 - 15, PlayerSizecrpd[1]*me.H[0]/me.H[1], 10))
    for e in ActiveWeaponer:
        screen.blit(e.I, (int(((w + e.X[0]) / 2) - e.s[0] / 2), int(((h + e.Y[0]) / 2) - e.s[1] / 2)))
    for e in Activearmor:
        screen.blit(e.I,(w//2-e.s[0]//2,h//2-e.s[1] // 2))
    draw0()
    draw00(0)

    ############           ############           ############           ############
    #######  player  #############  player  #############  player  #############  player  ######
    ############           ############           ############           ############
    if moving==1:
        xS = (XX[0]) - (w / 2)
        yS = (XX[1]) - (h / 2)
        posofmousa = [XX[0] - me.X, XX[1] - me.Y]
        if xS == 0:
            PXSPD = PSPE
            PYSPD = 0
        else:
            PXSPD = PSPE / math.sqrt(yS ** 2 / xS ** 2 + 1)
            if xS < 0:
                PXSPD *= -1
            PYSPD = PXSPD * yS / xS
    Px -= PXSPD*min((time.time() - start_time)*70,5)
    Py -= PYSPD*min((time.time() - start_time)*70,5)
    if distanceM(posofmousa[0] + me.X, posofmousa[1] + me.Y, w // 2, h // 2, 10):
        posofmousa = [1000000, 1000000]
        PXSPD = 0
        PYSPD = 0
    if not borderXX[0] + w // 2 <= Px <= borderXX[1] + w // 2:
        if Px < borderXX[0] + w // 2:
            Px = borderXX[0] + w // 2
        else:
            Px = borderXX[1] + w // 2
    if not borderYY[0] + h // 2 <= Py <= borderYY[1] + h // 2:
        if Py < borderYY[0] + h // 2:
            Py = borderYY[0] + h // 2
        else:
            Py = borderYY[1] + h // 2
    me.X = int(Px)
    me.Y = int(Py)
    ############           ############           ############           ############
    #######  player  #############  player  #############  player  #############  player  ######
    ############           ############           ############           ############

    ############           ############           ############           ############
    #######    MOB   #############    MOB   #############   MOB    #############    MOB   ######
    ############           ############           ############           ############

    arrowmov()
    arrowkill()
    mobmov()
    ############           ############           ############           ############
    #######    MOB   #############    MOB   #############   MOB    #############    MOB   ######
    ############           ############           ############           ############
    fps = font.render("FPS: " + str(time.time() - start_time), True, (0, 0, 0))
    screen.blit(fps, (10, 20))
    fps = font.render("TimeTillDeath: " + str(countdown+240 - int(start_time)), True, (0, 0, 0))
    screen.blit(fps, (10, 50))
    if (countdown+240 - int(start_time))<1:
        countdown=1000000000000
        r = requests.post('http://'+ipadress+':5000/Murderfight', headers=headers, data=jsonpickle.encode([]))
    if cooldown > 0:
        cooldown -= 1
    for e in timedstuffs:
        if e.T < ti:
            e.F()
        else:
            break

    pygame.display.update()
    ti += (time.time() - start_time)*50
    to += 1
