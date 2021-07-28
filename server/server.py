from flask import Flask, request
import jsonpickle
import time
import random
import pygame
import math
countdown=-1
class tile(pygame.sprite.Sprite):
    def __init__(self, X, Y, I):
        self.X = X
        self.Y = Y
        self.I = I
        self.s = [100,100]
playersID=0
moobs=[]
moobID=0

def distanceC(eneX, eneY, bulX, bulY):
    distance = math.sqrt((math.pow(eneX - bulX, 2)) + (math.pow(eneY - bulY, 2)))
    return distance
class moob(object):
    def __init__(self):
        global moobID
        moobID+=1
        self.ID=moobID
        self.X=-20000 + 200 * random.randint(0, 200)
        self.Y=-20000 + 200 * random.randint(0, 200)
        self.difficulty=int((distanceC(self.X,self.Y,0,0))//500)
        self.difficulty=self.difficulty*self.difficulty/50
        if self.difficulty<0.5:
            self.difficulty=0.5
        self.enemies = min(10,max(int(self.difficulty*0.3),2))
class player(object):
    def __init__(self):
        global playersID
        self.updates=[]
        playersID+=1
        self.ID=playersID
        self.X=0
        self.Y=0
        self.dead=0
        self.spell = 0
        self.physical = 0
        self.H = [500, 500]
players=[]
shops=[]
shopID = 0
class shop(object):
    def __init__(self):
        global shopID
        shopID+=1
        self.ID=shopID
        self.X=-20000 + 200 * random.randint(1, 199)
        self.Y=-20000 + 200 * random.randint(1, 199)
        self.type=random.randint(0,2)
for e in range(1000):
    shops.append(shop())

for e in range(500):
    moobs.append(moob())


class timer(object):
    def __init__(self,ID):
        self.T="hu ha"
        self.ID=ID

app = Flask(__name__)

f=1
updates=[]
@app.route('/Murderfight', methods = ['POST'])
def Murderfight():
    global updates
    update = jsonpickle.decode(request.get_data())
    for b in players:
        if b.dead == 0:
            b.updates.append([3,[players]])
            b.dead = 1
    return jsonpickle.encode(players)

@app.route('/Dmgdone', methods = ['POST'])
def Dmgdone():
    global players
    update = jsonpickle.decode(request.get_data())
    pla=update[0]
    playrID=update[1]
    for e in pla:
        for b in players:
            if b.ID==e[2]:
                b.spell+=e[0]
                b.physical+=e[1]
                break
    for e in players:
        if e.ID==playrID:
            phys=e.physical
            spol=e.spell
            e.physical=0
            e.spell=0
            return jsonpickle.encode([spol,phys])
            break
buttons=[]
@app.route('/Auction', methods = ['POST'])
def auction():
    global shops,updates,buttons
    buttons=[]
    buttons.append([0.5, 0.67, 1, 1,
                    [1, [50, 0, 0, 2, 0]
                        , ["The bible of facesmacking",
                           "a permanent 50 attack boost. costs:"]], random.randint(1, 100000)])
    for e in range(6):
        if 0.15 * e + 0.1>0.5:
            e+=0.3
        buttons.append([0.15 * e + 0.1, 0.78, 0, 0,
                              [1, [250, 250]
                                  , ["HEALTH POTION",
                                     "a permanent 250 hp health boost. costs:"]],random.randint(1,100000)])
    update = jsonpickle.decode(request.get_data())
    for b in players:
        b.updates.append([5,[buttons]])
    return jsonpickle.encode(1)

@app.route('/AuctionEnd', methods = ['POST'])
def auctionpend():
    update = jsonpickle.decode(request.get_data())
    for b in players:
        aitems=[]
        for e in buttons:
            if b.ID==e[1]:
                aitems.append(e[1])
        b.updates.append([7, aitems])
@app.route('/AuctionPrice', methods = ['POST'])
def auctionpUpdate():
    global updates,buttons,players
    update = jsonpickle.decode(request.get_data())
    for e in buttons:
        if e[5] == update[0][0]:
            if e[4][0]<update[0][1]:
                for b in players:
                    if not b.ID == update[1]:
                        b.updates.append([6, update])
                    e[1]=update[1]
                    e[4][0]=update[0][1]
                return jsonpickle.encode(1)
            else:
                print("i",e[4][0],update[0][1])
        else:
            print(e[5], update[0][0])
    return jsonpickle.encode(0)
@app.route('/ShopUpdate', methods = ['POST'])
def ShopUpdate():
    global shops,updates
    update = jsonpickle.decode(request.get_data())
    for e in shops:
        if e.ID==update[0]:
            newshop=shop()
            for b in players:
                if not b.ID==update[1]:
                    b.updates.append([0,[e.ID,newshop]])
            shops.append(newshop)
            shops.remove(e)
            return jsonpickle.encode(newshop)
            break

@app.route('/playerdeath', methods = ['POST'])
def playerdeath():
    global players,updates
    update = jsonpickle.decode(request.get_data())
    if len(players) == 2:
        for e in players:
            e.updates.append([4, [1, update]])
    else:
        for e in players:
            if e.ID==update:
                players.remove(e)
            else:
                e.updates.append([4, [0,update]])
    return jsonpickle.encode(0)
@app.route('/MoobUpdate', methods = ['POST'])
def MoobUpdate():
    global moobs,updates
    update = jsonpickle.decode(request.get_data())
    for e in moobs:
        if e.ID==update[0]:
            newshop=moob()
            for b in players:
                if not b.ID==update[1]:
                    b.updates.append([1,[e.ID,newshop]])
            moobs.append(newshop)
            moobs.remove(e)
            return jsonpickle.encode(newshop)
            break

@app.route('/PlayerUpdate', methods = ['POST'])
def PlayerUpdate():
    global players,updattes
    update = jsonpickle.decode(request.get_data())
    for e in players:
        if e.ID==update.ID:
            e.X=-update.X
            e.Y=-update.Y
            e.H=update.H
            updattes=e.updates
            e.updates=[]
            break
    return jsonpickle.encode([players,updattes])

@app.route('/MyUpdates', methods = ['POST'])
def giveupdate():
    global players
    update = jsonpickle.decode(request.get_data())
    for e in players:
        if e.ID==update:
            dododoo=[e for e in e.updates]
            e.updates = []
            return jsonpickle.encode(dododoo)
            break
    print('clientnotfounderror')
    return jsonpickle.encode([])
@app.route('/players', methods = ['GET'])
def playerget():
    global players
    return jsonpickle.encode(players)
@app.route('/game/<name>', methods = ['GET', 'POST'])
def game_endpoint(name):
    global f
    if request.method == 'POST':
        data = jsonpickle.decode(request.get_data())
        data.ID+=1
        return jsonpickle.encode(data)
    else:
        f+=1
        return f"Hello, {name} {f}!"

@app.route('/start')
def startdfhd():
    global players,countdown
    newplayer=player()
    players.append(newplayer)
    if len(players)==2:
        countdown=int(time.time())
        for e in players:
            e.updates.append([2,[countdown]])
    elif countdown>0:
        newplayer.updates.append([2, [countdown]])
    return jsonpickle.encode(newplayer)

@app.route('/shoppos')
def shopposer():
    global shops
    return jsonpickle.encode(shops)
@app.route('/mobbos')
def mobboser():
    global moobs
    return jsonpickle.encode(moobs)
@app.route('/time')
def time_endpoint():
    return "%f" % time.time()


app.run('0.0.0.0', 5000, True)