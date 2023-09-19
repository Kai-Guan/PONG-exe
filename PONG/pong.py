import pygame, pygame.mixer, sys, math, numpy, random, cv2
from os import listdir
from os.path import isfile, join

black = (0,0,0)
white = (255,255,255)

def button(msg, x, y, w, h, defaultcolor, hovercolor, action, txtcolor,txtsize, rectAlpha = 255, txtAlpha = 255):
    global not_press
    global mousedown
    if rectAlpha == 255:
        pygame.draw.rect(screen, defaultcolor, (x, y, w, h))
    else:
        s = pygame.Surface((w,h))
        s.set_alpha(rectAlpha)
        s.fill((defaultcolor))
        screen.blit(s, (x,y))
    mouse = pygame.mouse.get_pos()

    buttonText = pygame.font.Font("minecraft.ttf",txtsize)
    buttonTextSurf = buttonText.render(msg, True, txtcolor)
    buttonTextSurf.set_alpha(txtAlpha)
    buttonTextRect = buttonTextSurf.get_rect()
    buttonTextRect.center = ((x+(w/2)), (y+(h/2)))
    screen.blit(buttonTextSurf, buttonTextRect)

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        if rectAlpha == 255:
            pygame.draw.rect(screen, hovercolor, (x, y, w, h))
        else:
            s = pygame.Surface((w,h))
            s.set_alpha(rectAlpha)
            s.fill((hovercolor))
            screen.blit(s, (x,y))
        mouse = pygame.mouse.get_pos()
        screen.blit(buttonTextSurf, buttonTextRect)
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND) 
        if not_press == True:

            click = pygame.mouse.get_pressed()

            if click[0] == 1:
                mousedown = True
                action()
                not_press = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return(True)
    else:
        return(False)
    
def ImgButton(img, x, y, action, scale = 1):
    global not_press
    global mousedown

    img = pygame.image.load(img)

    imgW = img.get_width()*scale
    imgH = img.get_height()*scale

    mouse = pygame.mouse.get_pos()

    scaledImage = pygame.transform.scale(img, (int(imgW*scale),int(imgH*scale)))
    screen.blit(scaledImage, (x, y))

    if x + imgW*scale > mouse[0] > x and y + imgH*scale > mouse[1] > y:
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
        if not_press == True:

            click = pygame.mouse.get_pressed()

            if click[0] == 1:
                mousedown = True
                action()
                not_press = False
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        return(True)
    else:
        return(False)

def dashedLine(color, start_pos, end_pos, width=1, dash_length=10):
    x1, y1 = start_pos
    x2, y2 = end_pos
    dl = dash_length

    if (x1 == x2):
        ycoords = [y for y in range(y1, y2, dl if y1 < y2 else -dl)]
        xcoords = [x1] * len(ycoords)
    elif (y1 == y2):
        xcoords = [x for x in range(x1, x2, dl if x1 < x2 else -dl)]
        ycoords = [y1] * len(xcoords)
    else:
        a = abs(x2 - x1)
        b = abs(y2 - y1)
        c = round(math.sqrt(a**2 + b**2))
        dx = dl * a / c
        dy = dl * b / c

        xcoords = [x for x in numpy.arange(x1, x2, dx if x1 < x2 else -dx)]
        ycoords = [y for y in numpy.arange(y1, y2, dy if y1 < y2 else -dy)]

    next_coords = list(zip(xcoords[1::2], ycoords[1::2]))
    last_coords = list(zip(xcoords[0::2], ycoords[0::2]))
    for (x1, y1), (x2, y2) in zip(next_coords, last_coords):
        start = (round(x1), round(y1))
        end = (round(x2), round(y2))
        pygame.draw.line(screen, color, start, end, width)
    #https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame

def roundedLine(p1, p2, color, w):
    rect = pygame.Rect(*p1, p2[0]-p1[0], p2[1]-p1[1])
    rect.normalize()
    rect.inflate_ip(w, w)
    line_image = numpy.zeros((rect.height, rect.width, 4), dtype = numpy.uint8)
    c = pygame.Color(color)
    line_image = cv2.line(line_image, (w//2, w//2), (p2[0]-p1[0]+w//2, p2[1]-p1[1]+w//2), (c.r, c.g, c.b, c.a), thickness=w)
    line_surface = pygame.image.frombuffer(line_image.flatten(), rect.size, 'RGBA')
    screen.blit(line_surface, line_surface.get_rect(center = rect.center))
    #https://stackoverflow.com/questions/70051590/draw-lines-with-round-edges-in-pygame
    #end 

def slider(p1, p2, baseColor, circleColor, lineWidth, circleR, percentage):

    mouse = pygame.mouse.get_pos()
    trueLength = ((p2[0]-(int(lineWidth/2)))-(p1[0]+(int(lineWidth/2))))

    #background line
    roundedLine((p1[0]+(int(lineWidth/2)), p2[1]), (p2[0]-(int(lineWidth/2)), p2[1]), baseColor, lineWidth)


    #mouse
    adjustedX = int((p1[0])+int(lineWidth/2)+(percentage*trueLength))

    if pygame.mouse.get_pressed()[0]:
        if p2[0] > mouse[0] > p1[0] and p1[1] + circleR > mouse[1] > p1[1] - circleR:
            mouseX = pygame.mouse.get_pos()[0]
            if mouseX < p1[0]+(int(lineWidth/2)):
                adjustedX = p1[0]+(int(lineWidth/2))
            elif mouseX > p2[0]-(int(lineWidth/2)):
                adjustedX = p2[0]-(int(lineWidth/2))
            else:
                adjustedX = mouseX



    #filler line
    roundedLine((p1[0]+(int(lineWidth/2)), p2[1]), (adjustedX, p2[1]), circleColor, lineWidth)

    
    #circle
    pygame.draw.circle(screen, circleColor, (adjustedX, p1[1]), circleR)

    #print((p1[0]+(int(lineWidth/2))+adjustedX)/trueLength)
    return round((adjustedX-int(lineWidth/2)-p1[0])/trueLength, 2)

def start1():
    global players, play, playing, difficultySelect
    players = 1
    play = True
    playing = True
    difficultySelect = True
    startPop.play()

def start2():
    global players, play, playing, gameStartStartTicks, startTimer, seconds
    players = 2
    play = True
    playing = False
    startGameTimer()
    gameReset()
    #print("2 Players")

def easyDifficulty():
    global difficultySelect, difficulty
    difficulty = "easy"
    difficultySelect = False
    gameReset()
    startGameTimer()
    #print(difficulty)

def hardDifficulty():
    global difficultySelect, difficulty
    difficulty = "hard"
    difficultySelect = False
    gameReset()
    startGameTimer()
    #print(difficulty)

def impossibleDifficulty():
    global difficultySelect, difficulty
    difficulty = "impossible"
    difficultySelect = False
    gameReset()
    startGameTimer()
    #print(difficulty)

def setting():
    global settingmenu
    if settingmenu == True:
        settingmenu = False
    else:
        settingmenu = True
    startPop.play()

def musicVolumeToggle():
    global musicVolume, previousVolume
    if musicVolume != 0:
        previousVolume = musicVolume
        musicVolume = 0
    else:
        musicVolume = previousVolume
        click.play()


def startGameTimer():
    global gameStartStartTicks, startTimer, seconds
    startTimer = True
    gameStartStartTicks=pygame.time.get_ticks()
    seconds = 3

def quit():
    pygame.quit()
    sys.exit()

class Paddle(pygame.sprite.Sprite):
    def __init__(self, color, width, height, location):
        super().__init__()
        self.width = width
        self.height = height
        self.location = location
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(black)
        self.image.set_colorkey(black)

        pygame.draw.rect(self.image, color, (0, 0, width, height))
        
        self.rect = self.image.get_rect()

    def update(self):
        key = pygame.key.get_pressed()
        if self.location == "L":
            if key[pygame.K_w]:
                self.up()
            if key[pygame.K_s]:
                self.down()
        if self.location == "R":
            if key[pygame.K_UP]:
                self.up()
            if key[pygame.K_DOWN]:
                self.down()
        global reset
        if reset == True:
            self.reset()

    def up(self):
        if self.rect.y > 62:
            self.rect.y -= 7
            
    def down(self):
        if self.rect.y < 443:
            self.rect.y += 7

    def reset(self):
        if self.location == "L":
            self.rect.x = 20
            self.rect.y = 225
        if self.location == "R":
            self.rect.x = 470
            self.rect.y = 225
        if self.location == "R":
            global reset
            reset = False

class Ball(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.speed = 1
        self.width = 10
        self.height = 10
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(white)

        pygame.draw.rect(self.image, white, [0, 0, self.width, self.height])

        self.velocity = [random.randint(4,5)*self.speed*-1,random.randint(-6,6)*self.speed]
        
        self.rect = self.image.get_rect()

        self.rect.x = 245
        self.rect.y = 245

    def update(self):
        global reset, scoreRight, scoreLeft, playing, play, difficulty
        self.rect.x += (self.velocity[0]*self.speed)/2
        self.rect.y += (self.velocity[1]*self.speed)/2
        if self.rect.x>=500:
            scoreLeft += 1
            self.reset()
            reset = True
        if self.rect.x<=0 and difficulty != "impossible":
            scoreRight += 1
            self.reset()
            reset = True
        if self.rect.x<=0 and difficulty == "impossible":
            self.rect.y = machine.rect.y+22
            self.rect.x = machine.rect.x+10
        if self.rect.y>490:
            self.velocity[1] = -self.velocity[1]
            self.rect.y = 490
            pop.play()
        if self.rect.y<57:
            self.velocity[1] = -self.velocity[1]
            self.rect.y = 55
            pop.play()
        self.rect.x += (self.velocity[0]*self.speed)/2
        self.rect.y += (self.velocity[1]*self.speed)/2

    def reset(self):
        global scoreLeft, scoreRight, playing, play, start_ticks
        self.rect.x = 245
        self.rect.y = 245
        self.speed = 1
        xvelocity = random.uniform(3,5)

        n = random.choice((0,1))
        if n == 0:
            y = random.randint(2,6)
        elif n == 1:
            y = random.randint(-6,-2)

        if (scoreLeft+scoreRight)%2 == 0:
            x = 1
        elif (scoreLeft+scoreRight)%2 == 1:
            x= -1
        self.velocity = [xvelocity*x*self.speed,y*self.speed]

        startPop.play()

        if scoreRight == 7 or scoreLeft == 7:
            playing = False
            start_ticks=pygame.time.get_ticks()

    def bounce(self,side):
        self.velocity[0] = -self.velocity[0]
        self.velocity[1] = self.velocity[1]*random.uniform(0.8,1.2)
        self.rect.x += self.velocity[0]*self.speed
        self.rect.y += self.velocity[1]*self.speed
        if side == "Left":
            self.rect.x = 30
        if side == "Right":
            self.rect.x = 460
        pop.play()
        self.speed+=0.2

class Machine(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.color = color
        self.image = pygame.Surface((width, height))
        self.image.fill(black)
        self.image.set_colorkey(black)

        pygame.draw.rect(self.image, color, (0, 0, width, height))
        
        self.rect = self.image.get_rect()

    def update(self, difficulty):
        global reset
        if difficulty == "easy":
            if ball.rect.y<=self.rect.y+10:
                if ball.rect.y+15>=self.rect.y+10:
                    self.up(5)
                else:
                    self.up(6)
            if ball.rect.y+10>=self.rect.y+40:
                if ball.rect.y-15<=self.rect.y+40:
                    self.down(5)
                else:
                    self.down(6)
            if reset == True:
                self.reset()
        elif difficulty == "hard":
            if ball.rect.y<=self.rect.y+10:
                if ball.rect.y+5>=self.rect.y+10:
                    self.up(5)
                else:
                    self.up(8)
            if ball.rect.y+10>=self.rect.y+40:
                if ball.rect.y-5<=self.rect.y+40:
                    self.down(5)
                else:
                    self.down(8)
            if reset == True:
                self.reset()
        elif difficulty == "impossible":
            if ball.rect.y>78 and ball.rect.y<476:
                self.rect.y = ball.rect.y-22.5
 
    def up(self, amount):
        if self.rect.y > amount+55:
            self.rect.y -= amount
            
    def down(self, amount):
        if self.rect.y < 450-amount:
            self.rect.y += amount

    def reset(self):
        self.rect.x = 20
        self.rect.y = 225

def scores():
    global playing, play, scoreLeft, scoreRight
    text = pygame.font.Font("minecraft.ttf",50)
    textSurf = text.render(str(scoreRight), True, (255, 255, 255))
    screen.blit(textSurf, (262,5))

    textSurf = text.render(str(scoreLeft), True, (255, 255, 255))
    LScoreSize= text.size(str(scoreLeft))
    screen.blit(textSurf, (240-LScoreSize[0],5))

def gameReset():
    global scoreLeft, scoreRight, paused
    scoreLeft = 0
    scoreRight = 0
    paused = False
    paddleL.reset()
    paddleR.reset()
    machine.reset()
    ball.reset()

def stop():
    global play, playing, difficultySelect, pausevar
    play, playing, difficultySelect, pausevar = False, False, False, False
    click.play()

def pause():
    global paused
    click.play()
    if paused == False:
        paused = True
    else:
        paused = False

######Initialise#####
pygame.init()
screen = pygame.display.set_mode(size=(500,500), flags=pygame.SCALED, display=0, vsync=1)
pygame.display.set_caption('PONG')

not_press = True
paused = False
play = False
reset = False
playing = False
difficultySelect = False
startTimer = False
paused = False
settingmenu = False
difficulty = str()
objectList2Players = pygame.sprite.Group()
objectList1Player = pygame.sprite.Group()
machineList = pygame.sprite.Group()
scoreLeft = 0
scoreRight = 0
musicVolume = 1

clock = pygame.time.Clock()

#timer
start_ticks=pygame.time.get_ticks()
seconds=(pygame.time.get_ticks()-start_ticks)/1000
gameStartStartTicks=pygame.time.get_ticks()
gameStartseconds=(pygame.time.get_ticks()-gameStartStartTicks)/1000

#music
#https://downloads.khinsider.com/game-soundtracks/album/soul-knight-ost
songs = [f for f in listdir("songs") if isfile(join("songs", f))]
#pygame.mixer.music.load("songs/Blizzard.mp3")
songName = random.choice(songs)
print(f"Song: {songName}")
pygame.mixer.music.load(f"songs/{songName}")
pygame.mixer.music.set_volume(musicVolume)
pygame.mixer.music.play(-1)

#sfx
pop = pygame.mixer.Sound("sfx/pop.mp3")
startPop = pygame.mixer.Sound("sfx/start pop.wav")
click = pygame.mixer.Sound("sfx/click.wav")
clickVolume = 5
startPopVolume = 0.6
click.set_volume(5)
startPop.set_volume(0.6)

pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

#Left Paddle
paddleL = Paddle(white, 10, 50, "L")
paddleL.rect.x = 20
paddleL.rect.y = 200
objectList2Players.add(paddleL)

#Right Paddle
paddleR = Paddle(white, 10, 50, "R")
paddleR.rect.x = 470
paddleR.rect.y = 200
objectList2Players.add(paddleR)
objectList1Player.add(paddleR)

#Machine Paddle
machine = Machine(white, 10, 50)
machine.rect.x = 20
machine.rect.y = 200
machineList.add(machine)

#Ball
ball = Ball()
objectList2Players.add(ball)
objectList1Player.add(ball)
#####################

def controller():
    global playing, play, start_ticks, players, difficulty, gameStartseconds, gameStartStartTicks, startTimer, seconds, pausevar, settingMenu, musicVolume
    if not play:#title screen or setting menu
        if not settingmenu: # title screen
            screen.fill((40, 40, 43))#((51, 255, 211))
            P2 = button("2 Players",((screenWidth-175)/2),screenHeight-(screenHeight-330),175,50,white,(100,100,100),start2,black,30)
            P1 = button("1 Player",((screenWidth-175)/2),screenHeight-(screenHeight-270),175,50,white,(100,100,100),start1,black,30)
            settingButton = ImgButton("setting.png", 440, 440, setting, 0.5)
            if P1 == False and P2 == False and settingButton == False:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            logoImage = pygame.image.load("PONG.png")
            scaleMultiplyer = 2
            scaledImage = pygame.transform.scale(logoImage, (int(142*scaleMultiplyer),int(75*scaleMultiplyer)))
            screen.blit(scaledImage, ((screenWidth-scaledImage.get_width())/2, scaledImage.get_height()/2-50))
            pausevar = False
        else: # setting menu
            screen.fill((40, 40, 43))
            
            text = pygame.font.Font("minecraft.ttf",55)
            textSurf = text.render("Settings", True, (255, 255, 255))
            textSize = text.size("Settings")
            screen.blit(textSurf, ((500-textSize[0])/2,(230-textSize[1])/2))

            
            text = pygame.font.Font("minecraft.ttf",25)
            textSurf = text.render("Volume", True, (255, 255, 255))
            textSize = text.size("Volume")
            screen.blit(textSurf, ((500-textSize[0])/2, 175))

            musicVolume = 1*slider((50,220), (410,220), (255,255,255), (63, 72, 204), 20, 15, musicVolume/1)

            if musicVolume != 0:
                volumeButton = ImgButton("Volume On.png", 430, 210, musicVolumeToggle, 1)
            else:
                volumeButton = ImgButton("Volume Off.png", 430, 210, musicVolumeToggle, 1)

            pygame.mixer.music.set_volume(musicVolume)
            click.set_volume(clickVolume*musicVolume)
            startPop.set_volume(startPopVolume*musicVolume)


            text = pygame.font.Font("minecraft.ttf",25)
            textSurf = text.render("I'll add more", True, (255, 255, 255))
            textSize = text.size("I'll add more")
            screen.blit(textSurf, ((500-textSize[0])/2, 350))
            textSurf = text.render("stuff here later.", True, (255, 255, 255))
            textSize = text.size("stuff here later.")
            screen.blit(textSurf, ((500-textSize[0])/2, 380))



            settingButton = ImgButton("setting.png", 440, 440, setting, 0.5)
            if settingButton == False and volumeButton == False:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            #########################


    elif players == 2 and play:
        screen.fill((40, 40, 43))
        if startTimer == True:

            scaleMultiplyer = 1

            image = pygame.image.load("WS.png")
            scaledImage = pygame.transform.scale(image, (int(image.get_width()*scaleMultiplyer),int(image.get_height()*scaleMultiplyer)))
            screen.blit(scaledImage, (25-(scaledImage.get_width()/2), 180-(scaledImage.get_height()/2)))

            image = pygame.image.load("UD.png")
            scaledImage = pygame.transform.scale(image, (int(image.get_width()*scaleMultiplyer),int(image.get_height()*scaleMultiplyer)))
            screen.blit(scaledImage, (475-(scaledImage.get_width()/2), 180-(scaledImage.get_height()/2)))

            text = pygame.font.Font("minecraft.ttf",100)
            gameStartseconds=(pygame.time.get_ticks()-gameStartStartTicks)/1000
            if gameStartseconds<=3:
                seconds = 1
                if gameStartseconds<=2:
                    seconds = 2
                    if gameStartseconds<=1:
                        seconds = 3
            if gameStartseconds>=3:
                startTimer = False
                playing = True
            textSurf = text.render(str(seconds), True, (169, 169, 169))
            textSize = text.size(str(seconds))
            screen.blit(textSurf, ((500-textSize[0])/2,(500-textSize[1])/2))

        elif startTimer == False:
            if playing and not paused:
                objectList2Players.update()
            elif not playing and not paused:
                seconds=(pygame.time.get_ticks()-start_ticks)/1000
                text = pygame.font.Font("minecraft.ttf",75)
                textSurf = text.render("Game Over", True, (169, 169, 169))
                textSize = text.size("Game Over")
                screen.blit(textSurf, ((500-textSize[0])/2,(500-textSize[1])/2))
                if seconds >= 3:
                    play = False
        objectList2Players.draw(screen)
        if pygame.sprite.collide_mask(ball, paddleL):
            ball.bounce("Left")
        if pygame.sprite.collide_mask(ball, paddleR):
            ball.bounce("Right")
        scores()
        dashedLine(white,(250,55),(250,500),width=4,dash_length=15)
        pygame.draw.line(screen, white, (0,55), (500,55), 2)
        exit = button("Exit",420,5,75,50,(40, 40, 43),(40, 40, 43),stop,(255,255,255),30, 0, 127)
        if gameStartseconds>=3:
            if paused == False:
                pausevar = button("Pause",30,5,85,50,(40, 40, 43),(40, 40, 43),pause,(255,255,255),30, 0, 127)
            elif paused == True:
                pausevar = False
                pausevar = button("Unpause",15,5,125,50,(40, 40, 43),(40, 40, 43),pause,(255,255,255),30, 0, 127)
        if exit == False and pausevar == False:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

    elif players == 1 and play:
        if difficultySelect == False:
            screen.fill((40, 40, 43))
            if startTimer == True:
                image = pygame.image.load("UD.png")
                scaleMultiplyer = 1
                scaledImage = pygame.transform.scale(image, (int(image.get_width()*scaleMultiplyer),int(image.get_height()*scaleMultiplyer)))
                screen.blit(scaledImage, (475-(scaledImage.get_width()/2), 180-(scaledImage.get_height()/2)))

                text = pygame.font.Font("minecraft.ttf",100)
                gameStartseconds=(pygame.time.get_ticks()-gameStartStartTicks)/1000
                if gameStartseconds<3:
                    seconds = 1
                    if gameStartseconds<=2:
                        seconds = 2
                        if gameStartseconds<=1:
                            seconds = 3
                if gameStartseconds>=3:
                    startTimer = False
                    playing = True
                textSurf = text.render(str(seconds), True, (169, 169, 169))
                textSize = text.size(str(seconds))
                screen.blit(textSurf, ((500-textSize[0])/2,(500-textSize[1])/2))
            if startTimer == False:
                if playing and not paused:
                    machine.update(difficulty)
                    objectList1Player.update()
                elif not playing and not paused:
                    seconds=(pygame.time.get_ticks()-start_ticks)/1000
                    text = pygame.font.Font("minecraft.ttf",75)
                    textSurf = text.render("Game Over", True, (169, 169, 169))
                    textSize = text.size("Game Over")
                    screen.blit(textSurf, ((500-textSize[0])/2,(500-textSize[1])/2))
                    if seconds >= 3:
                        play = False
            objectList1Player.draw(screen)
            machineList.draw(screen)
            if pygame.sprite.collide_mask(ball, machine):
                ball.bounce("Left")
            if pygame.sprite.collide_mask(ball, paddleR):
                ball.bounce("Right")
            scores()
            dashedLine(white,(250,55),(250,500),width=4,dash_length=15)
            dashedLine(white,(0,55),(500,55),width=1,dash_length=5)
            exit = button("Exit",420,5,75,50,(40, 40, 43),(40, 40, 43),stop,(255,255,255),30, 0, 127)
            if gameStartseconds>=3:
                if paused == False:
                    pausevar = button("Pause",30,5,85,50,(40, 40, 43),(40, 40, 43),pause,(255,255,255),30, 0, 127)
                elif paused == True:
                    pausevar = button("Unpause",15,5,125,50,(40, 40, 43),(40, 40, 43),pause,(255,255,255),30, 0, 127)
            if pausevar == False and exit == False:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        elif difficultySelect == True:
            screen.fill((40, 40, 43))#((51, 255, 211))
            text = pygame.font.Font("minecraft.ttf",55)
            textSurf = text.render("Select Difficulty", True, (255, 255, 255))
            textSize = text.size("Select Difficulty")
            screen.blit(textSurf, ((500-textSize[0])/2,(230-textSize[1])/2))
            easy = button("Easy",((screenWidth-175)/2),screenHeight-(screenHeight-210),175,50,white,(100,100,100),easyDifficulty,black,30)
            hard = button("Hard",((screenWidth-175)/2),screenHeight-(screenHeight-270),175,50,white,(100,100,100),hardDifficulty,black,30)
            impossible = button("Impossible",((screenWidth-175)/2),screenHeight-(screenHeight-330),175,50,white,(100,100,100),impossibleDifficulty,black,30)
            exit = button("Back",((screenWidth-85)/2),screenHeight-(screenHeight-420),85,30,(40, 40, 43),(40, 40, 43),stop,(255,255,255),30, 0, 127)
            if easy == False and hard == False and impossible == False and exit == False:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

def run():
    global screenWidth, screenHeight, not_press
    while True:
        clock.tick(30)
        screenWidth, screenHeight = screen.get_size()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                not_press = True
        
        controller()

        pygame.display.update()

if __name__=="__main__":
    run()