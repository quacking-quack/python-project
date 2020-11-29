import pygame, random
from math import sqrt, sin, cos, asin, acos, pi, atan2
pygame.init()

disp_width = 800
disp_height = 640
#gunship1 = [48,128]
display = pygame.display.set_mode((disp_width,disp_height))
bg = pygame.image.load('sprites/space_or_something.png')
red_p = pygame.image.load('sprites/projectile.png')
green_p = pygame.image.load('sprites/projectile2.png')
scope = pygame.image.load('sprites/scope.png')
##pygame.mixer.music.load('soundtrack1.ogg')
##pygame.mixer.music.play(-1)
scroll = [0,0]
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
    def __init__(self,x,y,width,height,sprite,speed,damage,owner):
        Game_Object.__init__(self,x,y,width,height,sprite)
        self.speed = speed
        self.speed_x = 0
        self.speed_y = 0
        self.timer = 0
        self.damage = damage
        self.owner = owner
        self.to_remove = False
        #self.hitbox = pygame.Rect((self.x,self.y,self.width,self.height))

    def move(self):
        self.x -= self.speed_x
        self.y -= self.speed_y
        #self.hitbox = pygame.Rect((self.x,self.y,self.width,self.height))

    def set_speed(self,point):
        a = self.x - point.x
        b = self.y - point.y
        self.speed_x = self.speed*(a/dist(self.x,self.y,point.x,point.y))
        self.speed_y = self.speed*(b/dist(self.x,self.y,point.x,point.y))

    def draw(self):
        display.blit(self.sprite,(int(self.x)+scroll[0],int(self.y)+scroll[1]))
        self.timer += 1
        if self.timer > 90:
            self.owner.remove(self)

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
        self.alive = True

    def draw(self):
        sprite2 = pygame.transform.rotate((self.sprite),self.angle)
        #self.hitbox = pygame.Rect(sprite2.get_rect())
        pygame.draw.rect(display,(255,255,255),(int(self.x - self.health//2-1)+scroll[0],int(self.y - sprite2.get_height()//2 - 20-1)+scroll[1],self.health+2,8))
        pygame.draw.rect(display,(255,0,0),(int(self.x - self.health//2)+scroll[0],int(self.y - sprite2.get_height()//2 - 20)+scroll[1],self.health,6))
        display.blit(sprite2,(int(self.x-(sprite2.get_width()//2))+scroll[0],int(self.y-(sprite2.get_height()//2))+scroll[1]))

    def move(self,c):
        self.x += self.speed*cos(self.angle*pi/180)*c
        self.y += self.speed*sin(self.angle*pi/180)*(-1)*c#self.c
        self.center.x += self.speed*cos(self.angle*pi/180)*c
        self.center.y += self.speed*sin(self.angle*pi/180)*(-1)*c#*self.c

    def get_damage(self,damage):
        self.health -= damage
##        if self.health < 0:
##            enemies.remove(self)
        
##    def move_backward(self):
##        speed = self.speed//2
##        self.x -= speed*cos(self.angle*pi/180)
##        self.y -= speed*sin(self.angle*pi/180)*(-1)#self.c
##        self.center.x -= speed*cos(self.angle*pi/180)
##        self.center.y -= speed*sin(self.angle*pi/180)*(-1)#self.c

class Enemy(Hero): 
    def __init__(self,x,y,width,height,health,speed,rotate_speed,sprite,rate_of_fire,a,n,stop_distance,target):
        Hero.__init__(self,x,y,width,height,health,speed,rotate_speed,sprite)
        self.rate_of_fire = rate_of_fire
        self.a = a
        self.n = n
        self.stop_distance = stop_distance
        self.target = target
        
        
    def set_stats(self):
        t = 1
        angle = (atan2((self.y-self.target.y),(self.target.x-self.x))*57.241)%360
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
        
    def shoot(self):
        self.timer = timer
        for i in range(self.n):
            a = (cos((self.angle+self.a*i)*pi/180))
            b = sin((self.angle+self.a*i)*pi/180)*(-1)
            self.projectiles.append(Projectile(self.x-10+self.width//2*a,self.y-10+self.height//2*b,20,20,'sprites/projectile2.png',5,5,self.projectiles))
            self.projectiles[-1].set_speed(Point(self.x+100*a,self.y+100*b))
    
    def move(self):
        if (abs(abs(self.x) - abs(self.target.x)) > self.stop_distance) or (abs(abs(self.y) - abs(self.target.y)) > self.stop_distance):
            self.x += self.speed*cos(self.angle*pi/180)
            self.y += self.speed*sin(self.angle*pi/180)*(-1)#self.c
            self.center.x += self.speed*cos(self.angle*pi/180)
            self.center.y += self.speed*sin(self.angle*pi/180)*(-1)#self.c

    def get_damage(self,damage):
        self.health -= damage
        if self.health < 0:
            self.alive = False

class Round_ship(Enemy):
    def __init__(self,x,y,width,height,health,speed,rotate_speed,sprite,rate_of_fire,a,n,stop_distance,target):
        Enemy.__init__(self,x,y,width,height,health,speed,rotate_speed,sprite,rate_of_fire,a,n,stop_distance,target)
        self.c = random.randrange(-1,2,2)
        
    def set_stats(self):
        self.angle += self.rotate_speed*self.c
        self.angle %= 360
    
    def move(self):
        angle = (atan2((self.y-self.target.y),(self.target.x-self.x))*57.241)%360
        if (abs(abs(self.x) - abs(self.target.x)) > self.stop_distance) or (abs(abs(self.y) - abs(self.target.y)) > self.stop_distance):
            self.x += self.speed*cos(angle*pi/180)
            self.y += self.speed*sin(angle*pi/180)*(-1)#self.c
            self.center.x += self.speed*cos(angle*pi/180)
            self.center.y += self.speed*sin(angle*pi/180)*(-1)#self.c
        
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
            self.owner.projectiles.append(Projectile(self.owner.x-10+random.randrange(-self.disp,self.disp),self.owner.y-10+random.randrange(-self.disp,self.disp),20,20,'sprites/projectile.png',25,10,self.owner.projectiles))
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
        display.blit(sprite, (int(self.owner.x-(sprite.get_width()//2))+scroll[0],int(self.owner.y-(sprite.get_height()//2))+scroll[1]))
def draw_scope():
    display.blit(scope,(pos[0]+scroll[0],pos[1]+scroll[1]))
    pygame.draw.line(display,(255,0,0),(int(hero.x)+scroll[0],int(hero.y)+scroll[1]),(pos[0]+12+scroll[0],pos[1]+12+scroll[1]))
game_over = False
clock = pygame.time.Clock()
hero = Hero(300,100,64,64,100,10,5,'sprites/ship_0.png')
hero.gun = Gun(hero,pygame.image.load('sprites/ship_gun_1.png'),1)
shoot_sound = pygame.mixer.Sound('sounds/shot.ogg')
enemies = []
timer = 0
c = -1
pygame.mouse.set_visible(0)
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
    
##    pygame.draw.line(display,(255,255,255),(hero.center.x,hero.center.y),(pos[0],hero.center.y))
##    pygame.draw.line(display,(255,255,255),(pos[0],hero.center.y),(pos[0],pos[1]))
    
    hero.draw()
    
    #pygame.draw.rect(display,(255,0,0),(600,200,200,430))
    hero.gun.draw(pos[0],pos[1])
    for enemy in enemies:
        if enemy.alive:
            enemy.set_stats()
            enemy.move()
            enemy.draw()
            if timer - enemy.timer > enemy.rate_of_fire:
                enemy.shoot()    
        for p in enemy.projectiles:
            p.move()
            p.draw()
            if dist(p.x,p.y,hero.x,hero.y) < hero.width/2:
                if not p.to_remove:
                    hero.get_damage(p.damage)
                    p.to_remove = True
        for p in enemy.projectiles:
            if p.to_remove:
                enemy.projectiles.remove(p)
    for enemy in enemies:
        if not enemy.projectiles:
            enemies.remove(enemy)
    for p in hero.projectiles:
        p.move()
        p.draw()
        for enemy in enemies:
            if enemy.alive:
                if dist(p.x,p.y,enemy.x,enemy.y) < enemy.width/2: 
                    if not p.to_remove:
                        enemy.get_damage(p.damage)
                        p.to_remove = True
    for p in hero.projectiles:
        if p.to_remove:
            hero.projectiles.remove(p)
                
    draw_scope()        
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
    if keys[pygame.K_p]:   
        enemies.append(Enemy(400,400,64,64,40,4,4,'sprites/enemy1.png',10,0,1,100,hero))
    if keys[pygame.K_o]:   
        enemies.append(Round_ship(400,400,64,64,100,1,1,'sprites/round_ship.png',2,90,4,100,hero))
##    if hero.angle > 90 or hero.angle < 270:
##        hero.c = -1
##    else:
##        hero.c = 1
    
    timer += 1
