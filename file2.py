import pygame, random
from math import sqrt, sin, cos, asin, acos, pi, atan2
pygame.init()

disp_width = 800
disp_height = 640
#gunship1 = [48,128] 27,16 63,16 99,16 27,80 64,80 99,80
display = pygame.display.set_mode((disp_width,disp_height))
bg = pygame.image.load('sprites/bg.png')
red_p = pygame.image.load('sprites/projectile.png')
green_p = pygame.image.load('sprites/projectile2.png')
scope = pygame.image.load('sprites/scope.png')
finger = pygame.image.load('sprites/finger.png')
pygame.mixer.music.load(f'sounds/ost.mp3')
explosion = []
lightning = []
lightning2 = []
for i in range(9):
    explosion.append(f'sprites/expl_{i}.png')
for i in range(1,9):
    lightning.append(f'sprites/lightning_{i}.png')
for i in range(1,9):
    lightning2.append(f'sprites/lightning2_{i}.png')

##pygame.mixer.music.load('soundtrack1.ogg')
##pygame.mixer.music.play(-1)
true_scroll = [0,0]
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
        
class Sprite():
    sprites = []
    def __init__(self,x,y,width,height,sprites,cyclic,c=1):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.sprites = []
        for i in sprites:
            self.sprites.append(pygame.transform.scale(pygame.image.load(i),(self.width,self.height)))
        self.cyclic = cyclic
        self.ind = 0
        self.c = c

    def draw(self):
        display.blit(self.sprites[self.ind],(self.x-scroll[0],self.y-scroll[1]))
        self.ind += 1
        if self.ind == len(self.sprites):
            if not self.cyclic:
                Sprite.sprites.remove(self)
            else:
                self.ind = 0
            
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
        display.blit(self.sprite,(int(self.x)-scroll[0],int(self.y)-scroll[1]))
        self.timer += 1
        if self.timer > 210:
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
        pygame.draw.rect(display,(255,255,255),(int(self.x - self.health//2-1-scroll[0]),int(self.y - sprite2.get_height()//2 - 20-1-scroll[1]),self.health+2,8))
        pygame.draw.rect(display,(255,0,0),(int(self.x - self.health//2-scroll[0]),int(self.y - sprite2.get_height()//2 - 20-scroll[1]),self.health,6))
        display.blit(sprite2,(int(self.x-(sprite2.get_width()//2))-scroll[0],int(self.y-(sprite2.get_height()//2))-scroll[1]))

    def move(self,c):
        if ((self.x + self.speed*cos(self.angle*pi/180)*c) < 1500) and ((self.x + self.speed*cos(self.angle*pi/180)*c) > 400):
            self.x += self.speed*cos(self.angle*pi/180)*c
            self.center.x += self.speed*cos(self.angle*pi/180)*c
        if ((self.y + self.speed*sin(self.angle*pi/180)*(-1)*c) < 1500) and ((self.y + self.speed*sin(self.angle*pi/180)*(-1)*c) > 400):
            self.y += self.speed*sin(self.angle*pi/180)*(-1)*c#self.c
            self.center.y += self.speed*sin(self.angle*pi/180)*(-1)*c#*self.c

    def get_damage(self,damage):
        global game_over
        self.health -= damage
        if self.health < 0:
            game_over = True
        
##    def move_backward(self):
##        speed = self.speed//2
##        self.x -= speed*cos(self.angle*pi/180)
##        self.y -= speed*sin(self.angle*pi/180)*(-1)#self.c
##        self.center.x -= speed*cos(self.angle*pi/180)
##        self.center.y -= speed*sin(self.angle*pi/180)*(-1)#self.c

class Enemy(Hero): 
    def __init__(self,x,y,width,height,health,speed,rotate_speed,sprite,rate_of_fire,a,n,stop_distance,proj,target):
        Hero.__init__(self,x,y,width,height,health,speed,rotate_speed,sprite)
        self.rate_of_fire = rate_of_fire
        self.a = a
        self.n = n
        self.stop_distance = stop_distance
        self.target = target
        self.proj = proj
        
        
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
            self.projectiles.append(Projectile(self.x-10+self.width//2*a,self.y-10+self.height//2*b,20,20,'sprites/projectile2.png',self.proj[0],self.proj[1],self.projectiles))
            self.projectiles[-1].set_speed(Point(self.x+100*a,self.y+100*b))
    
    def move(self):
        if (abs(abs(self.x) - abs(self.target.x)) > self.stop_distance) or (abs(abs(self.y) - abs(self.target.y)) > self.stop_distance):
            self.x += self.speed*cos(self.angle*pi/180)
            self.y += self.speed*sin(self.angle*pi/180)*(-1)#self.c
            self.center.x += self.speed*cos(self.angle*pi/180)
            self.center.y += self.speed*sin(self.angle*pi/180)*(-1)#self.c

    def get_damage(self,damage):
        global score
        self.health -= damage
        if self.health < 0:
            Sprite.sprites.append(Sprite(self.x-self.width//2,self.y-self.height//2,70,70,explosion,False))
            score += 1
            self.alive = False

class Round_ship(Enemy):
    def __init__(self,x,y,width,height,health,speed,rotate_speed,sprite,rate_of_fire,a,n,stop_distance,proj,target):
        Enemy.__init__(self,x,y,width,height,health,speed,rotate_speed,sprite,rate_of_fire,a,n,stop_distance,proj,target)
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
        display.blit(sprite, (int(self.owner.x-(sprite.get_width()//2))-scroll[0],int(self.owner.y-(sprite.get_height()//2))-scroll[1]))
        
##class Hardpoint():
##    def __init__(self,x,y,width,height,health,sprite,angle,gun,owner):
##        self.owner = owner
##        self.add_x = x
##        self.add_y = y
##        self.x = self.owner.x + self.add_x*cos(self.owner.angle*pi/180)
##        self.y = self.owner.y + self.add_y*sin(self.owner.angle*pi/180)*(-1)
##        self.width = width
##        self.height = height
##        self.health = health
##        self.sprite = pygame.transform.scale(pygame.image.load(sprite),(self.width,self.height))
##        self.gun = gun
##        self.angle = angle
##
##    def draw(self):
##        sprite2 = pygame.transform.rotate((self.sprite),(self.angle - self.owner.angle)%360)
##        display.blit(sprite2,(int(self.x-(sprite2.get_width()//2))-scroll[0],int(self.y-(sprite2.get_height()//2))-scroll[1]))
##
##    def set_stats(self):
##        self.x = self.owner.x + self.add_x#*cos(self.owner.angle*pi/180)
##        self.y = self.owner.y - self.add_y#*sin(self.owner.angle*pi/180)
##            
##    def get_damage(self,damage):
##        self.health -= damage
##        if self.health < 0:
##            self.alive = False
            
##class Gunship(Enemy):
##    #gunship1_hardpoints = [Hardpoint(27,16,32,32,50,'sprites/g1_hardpoint1.png',90,)]
##    def __init__(self,x,y,width,height,health,speed,rotate_speed,sprite,rate_of_fire,a,n,stop_distance,target):
##        Enemy.__init__(self,x,y,width,height,health,speed,rotate_speed,sprite,rate_of_fire,a,n,stop_distance,target)
##        self.hardpoints = []
##        self.health = 0
##        for h in self.hardpoints:
##            self.health+= h.health
##
##    def set_stats(self):
##        self.health = 0
##        for h in self.hardpoints:
##            self.health+= h.health
##        t = 1
##        angle = (atan2((self.y-self.target.y),(self.target.x-self.x))*57.241)%360
##        self.angle %= 360
##        if self.angle > angle:
##            if self.angle - angle < 180:
##                t = -1
##        else:
##            if (self.angle - angle)%360 < 180:
##                t = -1
##        if not (self.angle < angle + self.rotate_speed*2 and self.angle > angle - self.rotate_speed*2):
##            self.angle += self.rotate_speed*t
##
##    def draw(self):
##        sprite2 = pygame.transform.rotate((self.sprite),self.angle)
##        pygame.draw.rect(display,(255,255,255),(int(self.x - self.health//2-1-scroll[0]),int(self.y - sprite2.get_height()//2 - 20-1-scroll[1]),self.health+2,8))
##        pygame.draw.rect(display,(255,0,0),(int(self.x - self.health//2-scroll[0]),int(self.y - sprite2.get_height()//2 - 20-scroll[1]),self.health,6))
##        display.blit(sprite2,(int(self.x-(sprite2.get_width()//2))-scroll[0],int(self.y-(sprite2.get_height()//2))-scroll[1]))
##        for h in self.hardpoints:
##            h.draw()
l1 = Sprite(320,300,80,1300,lightning,True)
l2 = Sprite(1500,300,80,1300,lightning,True)
l3 = Sprite(320,300,1200,80,lightning2,True)
l4 = Sprite(300,1500,1300,80,lightning2,True)
def draw_bounds():
    l1.draw()
    l2.draw()
    l3.draw()
    l4.draw()
        
def draw_scope():
    display.blit(scope,(pos[0],pos[1]))
    pygame.draw.line(display,(255,0,0),(int(hero.x)-scroll[0],int(hero.y)-scroll[1]),(pos[0]+12,pos[1]+12))

def change_scroll():
    global scroll,true_scroll
    true_scroll[0] += (hero.x - scroll[0] - 432)/10
    true_scroll[1] += (hero.y - scroll[1] - 352)/10
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
##    pos[0] -= scroll[0]
##    pos[1] -= scroll[1]
#=============================================================================
##def def_hardpoints1(ship):
##    for i in range(3):
##        for j in range(2):
##            ship.hardpoints.append(Hardpoint(-36+36*i,-32+64*j,32,32,50,'sprites/g1_hardpoint1.png',90+180*j,0,ship))
##            ship.hardpoints[-1].gun = Gun(ship,pygame.image.load('sprites/g1_hardpoint1_gun.png'),1)

class Button():
    def __init__(self, x,y,text):
        self.color = (255,255,255)
        self.color2 = (0,0,200)
        self.color3 = (255,255,255)
        self.x = x
        self.y = y
        self.text = text
        font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF", 50)
        text = font.render(self.text, 1, self.color)
        self.width = text.get_width()
        self.height = text.get_height()
        self.pressed = False    

    def isOver(self,pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

    def draw(self):
        font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF", 50)
        text = font.render(self.text, 1, self.color3)
        display.blit(text, (self.x + (self.width//2 - text.get_width()//2), self.y + (self.height//2 - text.get_height()//2)))
#=============================================================================  
    
game_over = False
clock = pygame.time.Clock()
hero = Hero(600,600,64,64,100,10,5,'sprites/ship_0.png')
hero.gun = Gun(hero,pygame.image.load('sprites/ship_gun_1.png'),1)
shoot_sound = pygame.mixer.Sound('sounds/shot.ogg')
enemies = []
timer = 0
c = -1
score = 0
pygame.mouse.set_visible(0)
start_b = Button(300,250,'START')
end_b = Button(300,350,"END GAME")
def start_game():
    global timer,score
    game_over = False
    hero = Hero(600,600,64,64,100,10,5,'sprites/ship_0.png')
    hero.gun = Gun(hero,pygame.image.load('sprites/ship_gun_1.png'),1)
    enemies = []
    timer = 0
    score = 0
    pygame.mouse.set_visible(0)
    while not game_over:
        try:
            keys = pygame.key.get_pressed()
            clock.tick(30)
            for event in pygame.event.get():
                pos = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
                
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    hero.gun.shoot(pos[0]+scroll[0],pos[1]+scroll[1])
        ##            shoot_sound.play()
        ##            hero.projectiles.append(Projectile(hero.x-10,hero.y-10,20,20,'projectile.png',40))
        ##            hero.projectiles[-1].set_speed(Point(pos[0],pos[1]))
            #angle = acos((pos[0]-hero.center.x)/dist(hero.center.x,hero.center.y,pos[0],pos[1]))*57.241
            display.blit(bg,(0-scroll[0]//4,0-scroll[1]//4))
        ##    font = pygame.font.SysFont('calibri', 50, "bold")
        ##    text = font.render(f'{hero.angle}', 1, (255,255,255))
        ##    font = pygame.font.SysFont('calibri', 25, "bold")
        ##    text2 = font.render(f'{pos[0]}:{pos[1]}', 1, (255,255,255))
            
        ##    display.blit(text2, (pos[0],pos[1]))
            
        ##    pygame.draw.line(display,(255,255,255),(hero.center.x,hero.center.y),(pos[0],hero.center.y))
        ##    pygame.draw.line(display,(255,255,255),(pos[0],hero.center.y),(pos[0],pos[1]))
            change_scroll()
            hero.draw()
            draw_bounds()
            
            #pygame.draw.rect(display,(255,0,0),(600,200,200,430))
            hero.gun.draw(pos[0]+scroll[0],pos[1]+scroll[1])
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
                if not enemy.projectiles and not enemy.alive:
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
            for s in Sprite.sprites:
                s.draw()
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
                enemies.append(Enemy(400,400,64,64,40,4,4,'sprites/enemy1.png',90,30,12,100,(10,5),hero))
            if keys[pygame.K_o]:   
                enemies.append(Round_ship(400,400,64,64,100,1,1,'sprites/round_ship.png',4,90,4,100,(5,2),hero))
        ##    if keys[pygame.K_g]:   
        ##        enemies.append(Gunship(400,400,128,96,100,1,1,'sprites/gunship1.png',2,90,4,100,hero))
        ##        def_hardpoints1(enemies[-1])
        ##    if hero.angle > 90 or hero.angle < 270:
        ##        hero.c = -1
        ##    else:
        ##        hero.c = 1
            
            timer += 1
        except:
            pass
    #game_over()
    
def main_menu():
    global menu
    menu = True
    y = 220
    while menu:
        clock.tick(20)
        display.fill((0,0,0))
        font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF", 100)
        text = font.render('Game name', 1, (255,255,255))
        display.blit(bg,(0,0))
        display.blit(text,(disp_width//2 - text.get_width()//2,50))
        font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF",50)
        text = font.render('START GAME',1,(255,255,255))
        display.blit(finger,((disp_width//2 - text.get_width()//2)-30,y+15))
        display.blit(text,(disp_width//2 - text.get_width()//2,220))
        text = font.render('END GAME',1,(255,255,255))
        display.blit(text,(disp_width//2 - text.get_width()//2,400))
        #display.blit(finger,((disp_width//2 - text.get_width()//2)-30,y+15))
        pygame.display.update()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                    
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_w] or keys[pygame.K_s]:
            if y == 220:
                y = 400
            else:
                y = 220
            pygame.time.delay(150)
        if keys[pygame.K_RETURN] and y==220:
            menu = False
            pygame.mixer.music.play(-1)
        elif keys[pygame.K_RETURN] and y==400:
            pygame.quit()
            quit()
def spawn_enemies():
    global enemies
    
    if not enemies:
        a = random.randrange(0,5)
        enemies.append(Enemy(spawn_zones[a][0],spawn_zones[a][1],64,64,40,4,4,'sprites/enemy1.png',90,1+score//10,1,100,(10,5),hero))
        for i in range(score//4):
            b = random.randrange(0,5)
            enemies.append(Enemy(spawn_zones[b][0],spawn_zones[a][1],64,64,40,4,4,'sprites/enemy1.png',90,1+score//10,1,100,(10,5),hero))
menu = True
spawn_zones = [[400,400],[400,1200],[1200,400],[1200,1200],[400,800],[800,400],[1200,800],[800,1200]]
##def game_over():
##    while True:
##        clock.tick(20)
##        display.fill((0,0,0))
##        font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF", 100)
##        text = font.render('GAME OVER', 1, (255,255,255))
##        display.blit(text,(disp_width//2 - text.get_width()//2,50))
##        font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF",50)
##        text = font.render(f'you scored: {score}',1,(255,255,255))
##        pygame.display.update()
##        for event in pygame.event.get():
##                if event.type == pygame.QUIT:
##                    pygame.quit()
##                    quit()
##                    
##        keys = pygame.key.get_pressed()
##        if keys[pygame.K_RETURN] and y==400:
##            pygame.quit()
##            quit()
while not game_over:
    if menu:
        main_menu()
    try:
        keys = pygame.key.get_pressed()
        clock.tick(30)
        for event in pygame.event.get():
            pos = [pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1]]
            
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                hero.gun.shoot(pos[0]+scroll[0],pos[1]+scroll[1])
    ##            shoot_sound.play()
    ##            hero.projectiles.append(Projectile(hero.x-10,hero.y-10,20,20,'projectile.png',40))
    ##            hero.projectiles[-1].set_speed(Point(pos[0],pos[1]))
        angle = acos((pos[0]-hero.center.x)/dist(hero.center.x,hero.center.y,pos[0],pos[1]))*57.241
        display.blit(bg,(0-scroll[0]//4,0-scroll[1]//4))
        font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF",50)
        text = font.render(f'score: {score}', 1, (255,255,255))
        display.blit(text, (10,10))
    ##    font = pygame.font.SysFont('calibri', 50, "bold")
    ##    text = font.render(f'{hero.angle}', 1, (255,255,255))
    ##    font = pygame.font.SysFont('calibri', 25, "bold")
    ##    text2 = font.render(f'{pos[0]}:{pos[1]}', 1, (255,255,255))
        
    ##    display.blit(text2, (pos[0],pos[1]))
        
    ##    pygame.draw.line(display,(255,255,255),(hero.center.x,hero.center.y),(pos[0],hero.center.y))
    ##    pygame.draw.line(display,(255,255,255),(pos[0],hero.center.y),(pos[0],pos[1]))
        change_scroll()
        hero.draw()
        draw_bounds()
        if not enemies:
            a = random.randrange(0,9)
            enemies.append(Enemy(spawn_zones[a][0],spawn_zones[a][1],64,64,40,4,4,'sprites/enemy1.png',10,1,1,100,(10,5),hero))
            for i in range(score//2):
                b = random.randrange(0,9)
                enemies.append(Enemy(spawn_zones[b][0],spawn_zones[b][1],64,64,40,4,4,'sprites/enemy1.png',10,1,1,100,(10,5),hero))
            for i in range(score//7):
                b = random.randrange(0,9)
                enemies.append(Round_ship(spawn_zones[b][0],spawn_zones[b][1],64,64,100,1,1,'sprites/round_ship.png',4,90,4,100,(5,2),hero))
        
        #pygame.draw.rect(display,(255,0,0),(600,200,200,430))
        hero.gun.draw(pos[0]+scroll[0],pos[1]+scroll[1])
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
            if not enemy.projectiles and not enemy.alive:
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
        for s in Sprite.sprites:
            s.draw()
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
            enemies.append(Enemy(400,400,64,64,40,4,4,'sprites/enemy1.png',90,30,12,100,(10,5),hero))
        if keys[pygame.K_o]:   
            enemies.append(Round_ship(400,400,64,64,100,1,1,'sprites/round_ship.png',4,90,4,100,(5,2),hero))
    ##    if keys[pygame.K_g]:   
    ##        enemies.append(Gunship(400,400,128,96,100,1,1,'sprites/gunship1.png',2,90,4,100,hero))
    ##        def_hardpoints1(enemies[-1])
    ##    if hero.angle > 90 or hero.angle < 270:
    ##        hero.c = -1
    ##    else:
    ##        hero.c = 1
        
        timer += 1
        
            
    except:
        pass
pygame.mixer.music.stop()
while True:
    clock.tick(20)
    display.fill((0,0,0))
    font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF", 100)
    text = font.render('GAME OVER', 1, (255,255,255))
    display.blit(text,(disp_width//2 - text.get_width()//2,50))
    font = pygame.font.Font("C:\Windows\Fonts\OCRAEXT.TTF",50)
    text = font.render(f'you scored: {score}',1,(255,255,255))
    display.blit(text,(disp_width//2 - text.get_width()//2,350))
    pygame.display.update()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
