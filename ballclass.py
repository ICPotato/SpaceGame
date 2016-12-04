from tkinter import *
import math
import random

#CONTRIBUTORS:
#Rob C - Development of the Program
#Olive S - Umm moral support

#This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

window = Tk()
window.resizable(0, 0)
window.geometry("600x600")
c = Canvas(window, width=600, height=600)
rand = 2
window.config(cursor="none")
window.title("Player Moving Simulator 2017")
c.pack()

class Entity(object):
        ## use position for bounding boxes, manual drawing
        ## use drawposition for loading sprites in
        def __init__(self):
                self.coords = {'x1': 0, 'y1': 0, 'x2': 0, 'y2': 0}
                self.drawCoords = {'x1': 0, 'y1': 0}
                self.sprite = PhotoImage()
        def getSprite(self):
                return self.sprite
        def setSprite(self, pic):
                self.sprite = pic
        def getPosition(self):
                return self.coords
        def setPosition(self, x1, y1, x2=0, y2=0):
                self.coords['x1'] = x1
                self.coords['y1'] = y1
                self.coords['x2'] = x2
                self.coords['y2'] = y2
        def setDrawPosition(self, x1, y1):
                self.drawCoords['x1'] = x1
                self.drawCoords['y1'] = y1
        def setPositionUsingDraw(self):
                self.coords['x1'] = self.drawCoords['x1']-self.sprite.width()/2
                self.coords['x2'] = self.drawCoords['x1']+self.sprite.width()/2
                self.coords['y1'] = self.drawCoords['y1']-self.sprite.height()/2
                self.coords['y2'] = self.drawCoords['y1']+self.sprite.height()/2                
        def getDrawPosition(self):
                return self.drawCoords

class Player(Entity):
        def __init__(self):
                c.bind("<Motion>", self.movePlayer)
                super(Player, self).__init__()
                self.spriteList = []
                self.playerCount = 0

                for i in range(0,12):
                        formatting = "gif -index " + str(i)  
                        self.spriteList.append(PhotoImage(file = './starship.gif', format=formatting))
                self.setSprite(PhotoImage(file = './starship.gif', format="gif -index 0"))
        def movePlayer(self, event):
                if (event.x > 0 and event.x+8 < 600):
                        self.sprite.width()
                        self.drawCoords['x1'] = event.x
                        self.coords['x1'] = event.x-(self.sprite.width()/2)
                        self.coords['x2'] = event.x+(self.sprite.width()/2)
                        
                if (event.y > 0 and event.y+8 < 600):
                        self.drawCoords['y1'] = event.y
                        self.coords['y1'] = event.y-(self.sprite.height()/2)
                        self.coords['y2'] = event.y+(self.sprite.height()/2)
                
        def identifyObject(self):
                return("Player")
            
class BulletPlayer(Entity):
        def __init__(self):
                super(BulletPlayer, self).__init__()
        def identifyObject(self):
                return("bulletPlayer")

class BulletEnemy(Entity):
        def __init__(self):
                super(BulletEnemy, self).__init__()
        def identifyObject(self):
                return("bulletEnemy")
                
class Enemy(Entity):
        def __init__(self):
                super(Enemy, self).__init__()
        def identifyObject(self):
                return("enemy")

class Powerup(Entity):
        def __init__(self):
                super(Powerup, self).__init__()
                self.sprite = PhotoImage(file = './powerup.png')  
        def identifyObject(self):
                return("powerup")
        def randomLocation(self):
                x1 = random.randint(0,584)
                y1 = 16
                self.setDrawPosition(x1, y1)
                

class Renderer(object):
        def __init__(self):
                c.bind("<Button-1>", self.prepareBulletPlayer)
         
                self.drawQueue = []

                self.count = 0 # animation for
                self.backgroundCount = 0
                
                #self.heart = PhotoImage(file = './heart.png')
                self.backgrounds = []
                self.backgrounds.append(Entity())
                
                self.Player = Player()
                self.backgrounds[0].setSprite(PhotoImage(file = './space.png'))
                self.backgrounds[0].setDrawPosition(self.backgrounds[0].sprite.width()/2, 0)

                self.PlayerProp = self.Player.getDrawPosition()

                self.enemy = Enemy()
                self.enemy.setDrawPosition(0,150);
                self.enemy.setSprite(PhotoImage(file = "./enemy.png"))
                
                self.drawQueue.append(self.enemy)
                
                self.gameLoop()
                window.mainloop()

        def scrollBackground(self):
                #BACKGROUND SIZE: 600x1446
                position = self.backgrounds[self.backgroundCount].getDrawPosition()
                if (position['y1'] == 662):
                        print("woo")
                        self.backgrounds.append(Entity())
                        self.backgroundCount += 1
                        self.backgrounds[self.backgroundCount].setSprite(PhotoImage(file = './space.png'))
                        self.backgrounds[self.backgroundCount].setDrawPosition(self.backgrounds[0].sprite.width()/2, -600)
                if (position['y1'] == 1325):
                        self.backgroundCount -= 1
                        self.backgrounds[self.backgroundCount].pop()
                

                for i in self.backgrounds:
                        position = i.getDrawPosition()
                        i.setDrawPosition(position['x1'], position['y1']+1)
                        c.create_image(position['x1'],position['y1']+1, image=i.getSprite())
                
            
        def prepareBulletPlayer(self, event):
                bulletPlayer = BulletPlayer()
                position = self.Player.getDrawPosition()
                bulletPlayer.setPosition(position['x1'], position['y1'], position['x1']+2, position['y1']-10)
                self.drawQueue.append(bulletPlayer)

        def prepareBulletEnemy(self, position):
                bulletEnemy = BulletEnemy()
                bulletEnemy.setPosition(position['x1'], position['y1'], position['x1']+2, position['y1']+10)
                self.drawQueue.append(bulletEnemy)

        def detectCollision(self, Rect1, Rect2):
                coords1 = Rect1.getPosition()
                coords2 = Rect2.getPosition()
                
                return not(
		(coords1['y2'] < coords2['y1']) or
		(coords1['y1'] > coords2['y2']) or
		(coords1['x1'] > coords2['x2']) or
		(coords1['x2'] < coords2['x1']))
        
        def gameLoop(self):
                c.delete(ALL)
                global rand
                #rand = random.randint(0,30000)
                
                if (rand == 2):
                        power = Powerup()
                        power.randomLocation()
                        self.drawQueue.append(power)
                rand = 3              
                inum = 0

                self.scrollBackground()

                #c.create_text(540, 26, text="LIVES", fill="white", font=('Bebas Neue Regular', 18))
                #c.create_text(50, 26, text="SCORE", fill="white", font=('Bebas Neue Regular', 18))
                #c.create_text(50, 53, text="0", fill="white", font=('Bebas Neue Regular', 18))
                
                #c.create_image(509, 53, image=self.heart)
                #c.create_image(509+30, 53, image=self.heart)
                #c.create_image(509+60, 53, image=self.heart)

                for i in self.drawQueue: # ok, so this code basically moves everything up or down if need be
                        drawPosition = i.getDrawPosition()
                        position = i.getPosition()
                        if (i.identifyObject() == "Player"):
                                potato = 0
                                c.create_image(drawPosition['x1'], drawPosition['y1'], image=self.Player.spriteList[self.Player.playerCount])
                                i.setPositionUsingDraw()
                                object1 = i
                                for j in self.drawQueue:
                                        object2 = j
                                        if (self.detectCollision(object1, object2)):
                                                if (j is not i):
                                                        #print(j, "from", i)
                                                        break
                                inum += 1
                        elif (i.identifyObject() == "enemy"):
                                potato = self.count % 50;
                                if (potato == 0):
                                        self.prepareBulletEnemy(drawPosition)
                                i.setDrawPosition(drawPosition['x1']+1, drawPosition['y1'])
                                c.create_image(drawPosition['x1']+1, drawPosition['y1'], image=i.sprite)
                                i.setPositionUsingDraw()
                                object1 = i
                                for j in self.drawQueue:
                                        object2 = j
                                        if (self.detectCollision(object1, object2)):
                                                if (j is not i):
                                                        if (j.identifyObject() is not "bulletEnemy"): # meh
                                                                #print(j, "from", i)
                                                                break
                                if position['x1'] >= 600:
                                        self.drawQueue.pop(inum);
                                inum += 1
                                        
                        elif (i.identifyObject() == "bulletEnemy"):
                                i.setPosition(position['x1'], position['y1']+10, position['x2'], position['y2']+10)
                                c.create_rectangle(position['x1'], position['y1']+10, position['x2'], position['y2']+10, fill="grey", outline="black")
                                if position['y2'] >= 600:
                                        self.drawQueue.pop(inum);
                                inum += 1
                                
                        elif (i.identifyObject() == "bulletPlayer"):
                                
                                i.setPosition(position['x1'], position['y1']-20, position['x2'], position['y2']-20)
                                c.create_rectangle(position['x1'], position['y1']-20, position['x2'], position['y2']-20, fill="grey", outline="black")
                                if position['y2'] <= 0:
                                        self.drawQueue.pop(inum);
                                inum += 1
                                                        
                        elif (i.identifyObject() == "powerup"):
                                i.setDrawPosition(drawPosition['x1'], drawPosition['y1']+5) 
                                c.create_image(drawPosition['x1'], drawPosition['y1'], image=i.sprite)
                                i.setPositionUsingDraw()
                                if drawPosition['y1'] >= 600:
                                        self.drawQueue.pop(inum);
                                inum += 1

                if (self.count != 100):
                        self.count += 1
                else:
                        self.count = 0   

                if (self.Player.playerCount != 11):
                        self.Player.playerCount += 1
                else:
                        self.Player.playerCount = 0   
                
                window.after(16, self.gameLoop)

        def drawObjects(self, name, x1, y1, x2, y2):
                        self.drawQueue.append([name, x1, y1, x2, y2])

if __name__ == '__main__':
        renderer = Renderer()
    



