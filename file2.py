import pygame, random
from math import sqrt, sin, cos, asin, acos, pi, atan2
pygame.init()

disp_width = 800
disp_height = 640
#gunship1 = [48,128]
display = pygame.display.set_mode((disp_width,disp_height))
bg = pygame.image.load('space_or_something.png')
##pygame.mixer.music.load('soundtrack1.ogg')
##pygame.mixer.music.play(-1)
def dist(x1,y1,x2,y2):
    return(sqrt((x2-x1)**2+(y2-y1)**2))

class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def dist(self,other_point):
        return(sqrt((other_point.x-self.x)**2+(other_point.y-self.y)**2))
    
class Game_Object():
    def __init__(self,x,y,width,height,sprite):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = Point(self.x+self.width//2,self.y+self.height//2)
        self.sprite = pygame.transform.scale(pygame.image.load(sprite),(self.width,self.height))

    def draw(self):
        display.blit(self.sprite,(self.x,self.y))

class Projectile(Game_Object):
    def __init__(self,x,y,width,height,sprite,speed,damage):
        Game_Object.__init__(self,x,y,width,height,sprite)
        self.speed = speed
        self.speed_x = 0
        self.speed_y = 0
        self.timer = 0
        self.damage = damage
        self.hitbox = pygame.Rect((self.x,self.y,self.width,self.height))

    def move(self):
        self.x -= self.speed_x
        self.y -= self.speed_y
        self.hitbox = pygame.Rect((self.x,self.y,self.width,self.height))

    def set_speed(self,point):
        a = self.x - point.x
        b = self.y - point.y
        self.speed_x = self.speed*(a/dist(self.x,self.y,point.x,point.y))
        self.speed_y = self.speed*(b/dist(self.x,self.y,point.x,point.y))

    def draw(self):
        display.blit(self.sprite,(self.x,self.y))
        self.timer += 1

class Hero(Game_Object):
    def __init__(self,x,y,width,height,health,speed,rotate_speed,sprite):
        Game_Object.__init__(self,x,y,width,height,sprite)
        self.hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
        self.right = True
        self.health = 100
        self.speed = speed
        self.rotate_speed = rotate_speed
        self.projectiles = []
        self.angle = 0
        self.c = 1
        self.timer = 0
        self.gun = 0
        self.health = health

    def draw(self):
        sprite2 = pygame.transform.rotate((self.sprite),self.angle)
        self.hitbox = pygame.Rect(sprite2.get_rect())
        pygame.draw.rect(display,(255,0,0),(self.x - self.health//2,self.y - sprite2.get_height()//2 - 20,self.health,8))
        display.blit(sprite2,(self.x-(sprite2.get_width()//2),self.y-(sprite2.get_height()//2)))

    def move(self,c):
        self.x += self.speed*cos(self.angle*pi/180)*c
        self.y += self.speed*sin(self.angle*pi/180)*(-1)*c#self.c
        self.center.x += self.speed*cos(self.angle*pi/180)*c
        self.center.y += self.speed*sin(self.angle*pi/180)*(-1)*c#*self.c

    def get_damage(self,proj):
        self.health -= proj.damage
##        if self.health < 0:
##            enemies.remove(self)
        
##    def move_backward(self):
##        speed = self.speed//2
##        self.x -= speed*cos(self.angle*pi/180)
##        self.y -= speed*sin(self.angle*pi/180)*(-1)#self.c
##        self.center.x -= speed*cos(self.angle*pi/180)
##        self.center.y -= speed*sin(self.angle*pi/180)*(-1)#self.c

class Enemy(Hero):
    def set_stats(self,target):
        t = 1
        angle = (atan2((self.y-target.y),(target.x-self.x))*57.241)%360
##        angle %= 360
##        font = pygame.font.SysFont('calibri', 50, "bold")
##        text = font.render(f'{angle}', 1, (255,255,255))
##        display.blit(text, (10,100))
        self.angle %= 360
        #a = (angle - self.angle)%360
        #b = (-a)%360
        if self.angle > angle:
            if self.angle - angle < 180:
                t = -1
        else:
            if (self.angle - angle)%360 < 180:
                t = -1
        if not (self.angle < angle + self.rotate_speed*2 and self.angle > angle - self.rotate_speed*2):
            #if a>b:#angle-8 > self.angle and self.angle < angle+8:
            self.angle += self.rotate_speed*t
            #else: #angle-8 < self.angle and self.angle > angle+8:
                #self.angle -= self.rotate_speed
        #self.angle %= 360
        
##    def draw(self,target):
##        self.angle = acos((target.x-self.x)/dist(self.x,self.y,target.x,target.y))*57.241
##        if self.angle > 89 and self.flipped:
##            self.sprite = pygame.transform.flip(self.sprite,1,0)
##            self.c = 1
##            self.flipped = False
##        elif self.angle < 89 and not self.flipped:
##            self.sprite = pygame.transform.flip(self.sprite,1,0)
##            self.c = -1
##            self.flipped = True
##        sprite = pygame.transform.rotate(self.sprite,self.c*asin((target.y-self.y)/dist(self.x,self.y,target.x,target.y))*57)
##        display.blit(sprite, (self.x-(sprite.get_width()//2),self.y-(sprite.get_height()//2)))
    
    def shoot(self,target):
        self.timer = timer
        self.projectiles.append(Projectile(self.x-10,self.y-10,20,20,'projectile.png',20,5))
        self.projectiles[-1].set_speed(Point(self.x+self.width*(cos(self.angle*pi/180)),self.y+self.height*(sin(self.angle*pi/180)*(-1))))
    
    def move(self,target):
        if (abs(abs(self.x) - abs(target.x)) > 100) or (abs(abs(self.y) - abs(target.y)) > 100):
            self.x += self.speed*cos(self.angle*pi/180)
            self.y += self.speed*sin(self.angle*pi/180)*(-1)#self.c
            self.center.x += self.speed*cos(self.angle*pi/180)
            self.center.y += self.speed*sin(self.angle*pi/180)*(-1)#self.c

    def get_damage(self,proj):
        self.health -= proj.damage
        if self.health < 0:
            enemies.remove(self)
            
class Gun():
    def __init__(self,owner,sprite,disp,buck=1,x=0,y=0):
        self.owner = owner
        self.sprite = sprite
        #self.projectile = projectile
        self.disp = disp
        self.buck = buck
        self.c = -1
        self.flipped = True
        self.angle = 0
        self.add_x = x
        self.add_y = y

    def shoot(self,x,y):
        shoot_sound.play()
        for i in range(self.buck):
            self.owner.projectiles.append(Projectile(self.owner.x-10+random.randrange(-self.disp,self.disp),self.owner.y-10+random.randrange(-self.disp,self.disp),20,20,'projectile.png',40,10))
            self.owner.projectiles[-1].set_speed(Point(x+random.randrange(-self.disp,self.disp)*5,y+random.randrange(-self.disp,self.disp)*5))

    def draw(self,x,y):
        self.angle = (atan2((self.owner.y-y),(x-self.owner.x))*57.241)%360#acos((x-self.owner.x)/dist(self.owner.x,self.owner.y,x,y))*57.241
##        if self.angle > 89 and self.flipped:
##            self.sprite = pygame.transform.flip(self.sprite,1,0)
##            self.c = 1
##            self.flipped = False
##        elif self.angle < 89 and not self.flipped:
##            self.sprite = pygame.transform.flip(self.sprite,1,0)
##            self.c = -1
##            self.flipped = True
        sprite = pygame.transform.rotate(self.sprite,self.angle)#self.c*asin((y-self.owner.y)/dist(self.owner.x,self.owner.y,x,y))*57)
        display.blit(sprite, (self.owner.x-(sprite.get_width()//2),self.owner.y-(sprite.get_height()//2)))
        
game_over = False
clock = pygame.time.Clock()
hero = Hero(300,100,64,64,100,10,5,'ship_0.png')
hero.gun = Gun(hero,pygame.image.load('ship_gun_1.png'),5,5)
shoot_sound = pygame.mixer.Sound('shot.ogg')
enemies = []
timer = 0
c = -1
while not game_over:
    keys = pygame.key.get_pressed()
    clock.tick(30)
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            hero.gun.shoot(pos[0],pos[1])
##            shoot_sound.play()
##            hero.projectiles.append(Projectile(hero.x-10,hero.y-10,20,20,'projectile.png',40))
##            hero.projectiles[-1].set_speed(Point(pos[0],pos[1]))
    angle = acos((pos[0]-hero.center.x)/dist(hero.center.x,hero.center.y,pos[0],pos[1]))*57.241
    display.blit(bg,(0,0))
##    font = pygame.font.SysFont('calibri', 50, "bold")
##    text = font.render(f'{hero.angle}', 1, (255,255,255))
##    font = pygame.font.SysFont('calibri', 25, "bold")
##    text2 = font.render(f'{pos[0]}:{pos[1]}', 1, (255,255,255))
    
##    display.blit(text2, (pos[0],pos[1]))
    pygame.draw.line(display,(155,0,0),(hero.x,hero.y),(pos[0],pos[1]))
##    pygame.draw.line(display,(255,255,255),(hero.center.x,hero.center.y),(pos[0],hero.center.y))
##    pygame.draw.line(display,(255,255,255),(pos[0],hero.center.y),(pos[0],pos[1]))
    
    hero.draw()
    #pygame.draw.rect(display,(255,0,0),(600,200,200,430))
    hero.gun.draw(pos[0],pos[1])
    for enemy in enemies:
        enemy.set_stats(hero)
        enemy.move(hero)
##        font = pygame.font.SysFont('calibri', 50, "bold")
##        text = font.render(f'{enemy.angle}', 1, (255,255,255))
##        display.blit(text, (10,10))
        enemy.draw()
        if timer - enemy.timer > 15:
            enemy.shoot(hero)
        for p in enemy.projectiles:
            p.move()
            p.draw()
            if p.hitbox.colliderect(hero.hitbox):
                enemy.projectiles.remove(p)
                hero.get_damage(p)
    for p in hero.projectiles:
        p.move()
        p.draw()
        #for enemy in enemies:
            
    pygame.display.update()
    if keys[pygame.K_d]:
        hero.angle -= hero.rotate_speed
        hero.angle %= 360
    elif keys[pygame.K_a]:    
        hero.angle += hero.rotate_speed
        hero.angle %= 360
    if keys[pygame.K_w]:   
        hero.move(1)
    elif keys[pygame.K_s]:   
        hero.move(-0.5)
    if keys[pygame.K_p] and not enemies:   
        enemies.append(Enemy(400,400,64,64,40,5,4,'enemy1.png'))
##    if hero.angle > 90 or hero.angle < 270:
##        hero.c = -1
##    else:
##        hero.c = 1
    timer += 1
