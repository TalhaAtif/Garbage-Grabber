#TALHA ATIF ICS-3U1 FINAL SUMMATIVE
import os
from pygame import *
from random import *

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (100, 100)  #Puts screen in top right corner, 50 pixels down

import pygame  #Imports everything needed
import math
import random

BLUE = (0, 0, 255)  #Sets all colour values
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
SELECT = (130, 159, 255)
ORANGE = (255, 165, 0)
GRAY = (68, 68, 68)
LBlue = (0, 102, 204)
DBlue = (0, 82, 165)
GRAY = (40, 40, 40)
LGray = (65, 65, 65)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
init()
SIZE = 1000, 700
screen = display.set_mode(SIZE)
running = True

def drawGame(): 
    #This function draws most of the things on the game board
    #It draws the slider bars for the magnet gun and the speed control
    #It also tells the game when the user has lost, when the healthNum reaches 5
    #It means the user has run out of health and died
    global restart #Resets all variables and lists when true
    global restartScreen #Activates the "you died" or "you won" screens 
    global magnetSpeed #The amount of pixels the magnet moves each time you press a or d
    global won #activates when you win, starting the win animation sequence
    global died #activates when you loose all your health, showing the death screen
    #I use alot of global variables to allow this function to control and checks them easily
    if healthNum==5: #When health reaches 5 it means you have run out of health. Health starts at 0 and goes to 4
        #this corresponds to the list of health bars at different health amounts
        restartScreen= True #Shows restart screen
        died= True #You have lost all your health
    else:
        drawImage(0,0,Backround) #Draws backround
        drawImage(35, 300, speedBar) #Draws the rail the speed control is on
        drawImage(100, 600, magnetBar) #Draws the rail the magnet gun is on
        drawImage(25, sliderCord, Slider) #Draws speed control slider
        if won == False: #If the player has not won
            drawImage(800,420, partsList[0]) #Draws empty robot
            drawImage(790, 320, healthBar[healthNum]) #Draws health bar
            for e in partsCollected: #Draws all the collected robot parts
                drawImage(800,420, e)
        drawImage(magnetCord, 500, menuList[6]) #Draws magnet gun
        drawImage(25, 525, menuList[7]) #Draws hitbox toggle
        drawImage(10, 10, backButton) #Draws back button
        
def drawImage(x, y, Image): #Function to blit image to screen, probably my most useful function
    Part = Rect(x, y, Image.get_width(), Image.get_height())
    screen.blit(Image, Part)

def magnetBeam(x,y, Slow): #Draws "laser" whenever your shoot the magnet gun
    if Slow== True: #If the magnet gun movement is above 75% the lasers shoot at half speed
        y= y-4
    else: #If it is below 75% movement speed they shoot at full
        y= y-8
    drawImage(x,y, Laser) #Draws laster image 
    return y #Returns y cord of laser (x cord doesnt change)
    
def moveObject(Object, x, direction): #Used to move the garbage can on the start menu
    if x == 110: #changes direction of the object when it hits a ceratain x value
        direction = "left"
    elif x == 610:
        direction = "right"
    if direction == "left":
        x += 1 #Moves the object 1 pixel left or right depending on the direction
    elif direction == "right":
        x = x - 1
    Part = Rect(x, 453, Object.get_width(), Object.get_height())
    screen.blit(Object, Part) #Draws object
    return (x, direction)

def drawTargets(x): #This function draws all my targets. 
    global targetList #A list of the images for the targets
    global targetRect #A list of all the rectangle coordinates
    global Hitboxes #toggles hitboxes
    global won #Checks if the player has won
    for e in range(len(targetList)):
        if e < 8: #Changes the coordiantes of all the rectanges in the list
            targetRect[e] = Rect((e*125+x+12), 107, 101,101) 
            drawImage(e*125+x+12, 107, targetList[e]) #Draws all the images in the rectangles
            if Hitboxes == True and won == False: #Will not show hitboxes during the win animation
                draw.rect(screen, BLACK, (targetRect[e]),5) #Makes the rectanlges visible (hitboxes)
    return x #returns the x cord of the furthest rectangle to the left

def missDraw(missCord, magnetCord): #Draws the "goon attack" when you hit an incorrect target
    global missAnimation #Toggles weather you missed or not 
    global healthNum #Health remaining
    y=0 #resets y everytime function is called
    if healthNum== 4: #If you are on the lowest health the "batman boss" will be called
        e= 0
        if missCord > magnetCord:
            missCord= (missCord-(3/(healthNum-1)))  #When the goons are getting to the x cord
            #Function uses a custom speed for the batman boss, to build suspense
            drawImage((missCord+((e-1)*30)), 100, bossMan)
            missAnimation= True
        else:
            missCord= (missCord-4) #Once the boss reaches the set x cord it will move downwards
            #It moves down much faster than it moves left or right
            y= int(700-((missCord+600)-magnetCord))
            drawImage((magnetCord+((e-1)*30)), y, bossMan) 
        if y > 440:
            healthNum+=1
            missAnimation= False
        
    else:
        magnetCord+= 12
        for e in range (healthNum+1): #Draw 1 more goon for each time you loose health
            #You loose health in this order, (starting at 15), 14, 12, 9, 5, 0 (lose)
            if missCord > magnetCord:
                missCord= (missCord-(3/(healthNum+1))) #Moves the guards a certain amount, which is
                #divided by the number of guards to keep speed consistent
                drawImage((missCord+((e-1)*30)), 100, Guard) 
                missAnimation= True
            else:
                missCord= (missCord-(3/(healthNum+1)))     
                y= int(700-((missCord+600)-magnetCord)) #Since the screen is 700 pixels 
                #high we subtract our number from 700 to move down
                drawImage((magnetCord+((e-1)*30)), y, Guard)            
        if y > 540: #When the guards reach the gun the animation stops and the health bar goes down
            healthNum+=1
            missAnimation= False
    return missAnimation, missCord

def targetHit(BeamX, BeamY): #Checks what target was hit (most complet function)
    global healthNum #Health remaining
    global missAnimation #Determines if you missed or not
    Target= Rect(BeamX, BeamY, 11, 20) #Sets dimentions for laser beam to find out if it collided with a target
    for e in targetRect: #Checks for collision with each of the rectangles
        if e.colliderect(Target): #If it collides with a rectangle:
            index1= (targetRect.index(e)) #Finds what number in the rectangle list the collided rectangle is
            if targetList[index1] in targetListOG: #Checks if the target is one of the robot parts
                indexTarget= (targetList[index1]) #Finds what spot in the target list the target is
                index2= (targetListOG.index(targetList[index1])) #Finds where in the unshuffled robot part list the target it
                #The line below adds the robot peice to the parts collected list
                partsCollected.append(partsList[index2+1]) #using the spot in the unshuffled list, finds the location in the robot list with different resolution images
                del targetList[index1] #deleted the target from the list of targets in us
            else:
                del targetList[index1] #Deleted target from target list even if it's not a robot part
                missAnimation= True #Activates the wrong target animation, unltimatley losing heath
    return missAnimation

Factory = image.load("Final.png").convert_alpha() #Load the factory
Robot = image.load("Robot.png").convert_alpha() #Starts loading all the robot parts for the parts collected image in the bottom right
Head = image.load("Head.png").convert_alpha()
Torso = image.load("Torso.png").convert_alpha()

leftShoulder = image.load("Left shoulder.png").convert_alpha()
leftArm = image.load("Left arm.png").convert_alpha()
leftKnee = image.load("Left knee.png").convert_alpha()
leftLeg = image.load("Left leg.png").convert_alpha()

rightShoulder = image.load("Right shoulder.png").convert_alpha()
rightArm = image.load("Right arm.png").convert_alpha()
rightKnee = image.load("Right knee.png").convert_alpha()
rightLeg = image.load("Right leg.png").convert_alpha()

HeadT = image.load("HeadT.png").convert_alpha() #Starts collecting all the robot parts for the target list on top of the screen
TorsoT = image.load("TorsoT.png").convert_alpha()
leftShoulderT = image.load("Left shoulderT.png").convert_alpha()
leftArmT = image.load("Left armT.png").convert_alpha()
leftKneeT = image.load("Left kneeT.png").convert_alpha()
leftLegT = image.load("Left legT.png").convert_alpha()
rightShoulderT = image.load("Right shoulderT.png").convert_alpha()
rightArmT = image.load("Right armT.png").convert_alpha()
rightKneeT = image.load("Right kneeT.png").convert_alpha()
rightLegT = image.load("Right legT.png").convert_alpha()

hitBox= image.load("Hitboxes.png").convert_alpha() #Loads in miscelanious imagess
magnetBar = image.load("Magnet bar.png").convert_alpha()
speedBar = image.load("Speed slider.png").convert_alpha()
Menu = image.load("Menu.png").convert_alpha() #Start menu states, Start game, How to play and Quit
menuStart = image.load("Menu start.png").convert_alpha()
menuHow = image.load("Menu how.png").convert_alpha()
menuQuit = image.load("Menu quit.png").convert_alpha()
garbageCan = image.load("Garbage can.png").convert_alpha() #Start menu garbage can
magnetGun = image.load("Magnet gun.png").convert_alpha() 
Slider= image.load("Slider.png").convert_alpha()
Backround= image.load("Backround.png").convert_alpha() #Backround for the main game

Laser= image.load("Laser.png").convert_alpha() #All the targets that are NOT robot parts
Washer= image.load("Washer.png").convert_alpha()
Camera= image.load("Camera.png").convert_alpha()
Soda= image.load("Soda.png").convert_alpha()
Coffee= image.load("Coffee.png").convert_alpha()
Battery= image.load("Battery.png").convert_alpha()
Microwave= image.load("Microwave.png").convert_alpha()
Mouse= image.load("Mouse.png").convert_alpha()
TV= image.load("TV.png").convert_alpha()
Plastic= image.load("Plastic.png").convert_alpha()
PC= image.load("PC.png").convert_alpha()
Laptop= image.load("Laptop.png").convert_alpha()

restartMenu= image.load("Restart.png").convert_alpha() #Different states for the "you died" menu
quitPress= image.load("QuitPress.png").convert_alpha()
restartPress= image.load("RestartPress.png").convert_alpha()
bossMan= image.load("bossMan.png").convert_alpha() #Batman goon for factory

winMenu= image.load("winScreen.png").convert_alpha() #Different states for the "you won" menu
quitWin= image.load("winQuit.png").convert_alpha()
restartWin= image.load("winRestart.png").convert_alpha()

maxHealth= image.load("Max.png").convert_alpha() #Health bar states
oneHit= image.load("14.png").convert_alpha()
twoHit= image.load("12.png").convert_alpha()
threeHit= image.load("9.png").convert_alpha()
fourHit= image.load("5.png").convert_alpha() #Lowest health before death
Guard= image.load("Guard.png").convert_alpha() #Guards / goons for factory

Robot1= image.load("Robot 1.png").convert_alpha() #Robot animation for win sequence
Robot2= image.load("Robot 2.png").convert_alpha()
Robot3= image.load("Robot 3.png").convert_alpha()
Robot4= image.load("Robot 4.png").convert_alpha()

backButton= image.load("back.png").convert_alpha() #Back button

Factory1= image.load("Factory 1.png").convert_alpha() #Factory animation for win sequence
Factory2= image.load("Factory 2.png").convert_alpha()
Factory3= image.load("Factory 3.png").convert_alpha()
Factory4= image.load("Factory 4.png").convert_alpha()
Factory5= image.load("Factory 5.png").convert_alpha()
Factory6= image.load("Factory 6.png").convert_alpha()
Factory7= image.load("Factory 7.png").convert_alpha()
Factory8= image.load("Factory 8.png").convert_alpha()
Factory9= image.load("Factory 9.png").convert_alpha()
Factory10= image.load("Factory 10.png").convert_alpha()
Factory11= image.load("Factory 11.png").convert_alpha()
Factory12= image.load("Factory 12.png").convert_alpha()
Factory13= image.load("Factory 13.png").convert_alpha()
Factory14= image.load("Factory 14.png").convert_alpha()
Factory15= image.load("Factory 15.png").convert_alpha()
Factory16= image.load("Factory 16.png").convert_alpha()
Factory17= image.load("Factory 17.png").convert_alpha()

# I USED CONVERT ALPHA BECAUSE THE PYGAME DOCUMENTATION SAID IT SPEEDS UP IMAGE BLITING,
# GREATLY REDUCING LAG. HOWEVER IT INCREASES THE INITIAL LOAD TIME.

winBeam= image.load("greenBeam.png").convert_alpha() #Laser the robot uses in the win animation
Tutorial= image.load("tutorial.png").convert_alpha() #tutorial screen
restartScreen= False #sets restart / "you died" screen to off
restart= True #initialized all the lists and variables, as well as creating and shuffling the target list
# Game Loop
while running == True: #Main game loop
    if restart== True: #Resets all lists and variables
        robotMove= [Robot1, Robot2, Robot3, Robot4]
        #Robot animation for win sequence
        factoryMove= [Factory1, Factory2, Factory3, Factory4, Factory5, Factory6, Factory7, Factory8, Factory9,
                      Factory10, Factory11, Factory12, Factory13, Factory14, Factory15, Factory16, Factory17]
        #factory animation
        restartList= [restartMenu, quitPress, restartPress]
        #You died screen
        winList= [winMenu, quitWin, restartWin]
        #You won screen
        healthBar= [maxHealth, oneHit, twoHit, threeHit, fourHit]
        #Health bars for different health levels
        menuList = [Menu, menuStart, menuHow, menuQuit, garbageCan, Factory, magnetGun, hitBox]
        #List of images for the menu + some misc ones
        partsList = [Robot, Head, Torso, leftShoulder, leftArm, leftKnee, leftLeg, rightShoulder, rightArm, rightKnee, rightLeg]
        #List of robot parts
        trashList= [Washer, Soda, Coffee, Battery, Microwave, Mouse, TV, Camera, Plastic, PC, Laptop]
        #List of random targets
        keysList = [K_a, K_d, K_s, K_w]
        #List of keys for more efficent code
        myClock = pygame.time.Clock()  #60 fps (Mr. Van Rooyen Code)
        targetList= [HeadT, TorsoT, leftShoulderT, leftArmT, leftKneeT, leftLegT, rightShoulderT, rightArmT, rightKneeT, rightLegT]
        #Resized robot parts for the targets
        targetRect= [0,0,0,0,0,0,0,0]
        #List of rectangles for the target collisio checking
        targetListOG= []
        #Unshuffled targets
        partsCollected= []
        #Collected robot parts
        robotParts= []
        #Used to create shuffled target list
        for e in range(len(menuList)): #Does resizing for all needed images
            if e == 7:
                menuList[e] = transform.smoothscale(menuList[e], (50,50))
            elif e == 5 or e == 6:
                menuList[e] = transform.smoothscale(menuList[e], (175, 175))
            elif e == 4:
                menuList[e] = transform.smoothscale(menuList[e], (250, 175))
            else:
                menuList[e] = transform.smoothscale(menuList[e], (1000, 700))
                
        for e in range(len(partsList)):
            partsList[e] = transform.smoothscale(partsList[e], (200, 200))
            if e < 4:
                robotMove[e] = transform.smoothscale(robotMove[e], (200, 200))
            
        for e in range (len(targetList)):
            targetList[e]=(transform.smoothscale(targetList[e], (101, 101)))
            
        for e in range (len(factoryMove)):
            factoryMove[e]=(transform.smoothscale(factoryMove[e], (175, 175)))        
    
        for e in targetList:
            targetListOG.append(e)
        
        for e in targetListOG:
            robotParts.append(e)
        #Copies robots parts into 2 list (needed later)
            
        numCheck= 0 #Used to ensure a 4:1 ratio
        targetList= []
        
        for e in range (((9-(len(partsCollected)))*4)+4): #Uses an equation to ensure the 
            #List is long enough that the target belt is never empty
            if numCheck == 0: #used for the 4:1 ratio
                partNumber= random.randint(0,((len(robotParts))-1))
                targetList.append(robotParts[partNumber])
                del robotParts[partNumber] #Adds a random robot part, then deletes from list of avalible parts
                #to avoid duplicate robot parts
            else: #Adds a random trash peice
                trashNumber= random.randint(0, ((len(trashList))-1))
                targetList.append(trashList[trashNumber])
            numCheck+= 1
            if numCheck== 4: #For every 4 trash pieces there will be 1 robot peice
                numCheck= 0
        shuffle(targetList) #Shuffles the list
        
        healthNum= 0 #Max health
        shoot= False #Gun is not shooting
        Hitboxes= False #Hitboxes off
        shotCord= 500 #Laser shoots from y= 500
        sliderCord = 390 #Speed slider starts centered
        magnetCord = 363 #Magnet gun starts centered
        magnetSpeed = 6.5 #Default magnet speed
        drawImage(0, 0, menuList[0]) #Draws backround for main menu
        currentScreen = "startMenu" #Sets screen to main menu
        clickArea = 0 #What button is being hovered over
        robotState= 0 #For robot animation
        died= False #Player is alive
        clickSpot = 0 #For died and won screens
        missAnimation= False #Player did not hit incorrect target
        garbageX = 195 #used for main menu garbage can
        direction = "left" #garbage can starts moving left
        magnetDirection = "noMove" #magnet and speed slider are not moving
        sliderDirection = "noMove" 
        targetX= 0 #Targets start with the furthest to the left at 0
        partsCollected= [] #collected robot parts (you win when this is the length of the robot parts list)
        missCord= 800 #the x cord where the guards "Spawn" when you hit an incorrect target 
        restart= False #disables the variable that resets all variables and lists
        Slow= False #Laser shoots at normal speed
        won = False #User did not win yet
        
        cheatNum=0
        #used for developer "cheat code"
        
    button = 0 #checks button (not sure what is does but to scared to delete)
    
    for e in event.get():  # checks all events that happen
        if e.type == pygame.QUIT:  #If X is pressed, game will immediatly end
            running = False 
            
        elif restartScreen== True: #on die / win screen, will highlight the button you're hovering over
            if e.type == MOUSEMOTION:
                mx, my = e.pos
                if mx > 257 and mx < 737:
                    if my > 210 and my < 325:
                        clickSpot = 2
                    elif my > 450 and my < 570:
                        clickSpot = 1
                    else:
                        clickSpot = 0
                else:
                    clickSpot = 0
        
            elif e.type == MOUSEBUTTONDOWN: #Checks where you mouse is hovering and reacts accordingly
                if clickSpot != 0:
                    if clickSpot == 1: #clickSpot 1 is quit button
                        running = False
                    if clickSpot == 2: #clickSpot 2 is restart button
                        currentScreen = "startMenu" 
                        restartScreen = False #Turns of restart screen
                        restart= True #Resets all variables
        elif currentScreen == "tutorial": #On tutorial screen will display game guide and "plot"
            if e.type == MOUSEBUTTONDOWN: #If you click it will check if you are on the "back" button and react accordingly
                mouseX, mouseY= e.pos
                if mouseX>50 and mouseX<110 and mouseY > 130 and mouseY < 160:
                    currentScreen= "startMenu"
                    restart= True #if you go back all variables reset again, and the screen changes to the main menu                
        elif currentScreen == "mainGame": #While you are in the main game
            if e.type == KEYUP: #When you let go of a key, the slider or magnet gun will stop moving
                for z in range(0, 2): #a and d
                    if e.key == keysList[z]:
                        magnetDirection = "noMove"
                for z in range (2,4): #s and w
                    if e.key == keysList[z]:
                        sliderDirection = "noMove"
            elif e.type == KEYDOWN: #when you press a key, the assigned object (Magnet gun or slider) will stay moving until the key is unpressed
                if e.key == K_a: #magnet gun
                    magnetDirection = "left"
                elif e.key == K_d: #magnet gun
                    magnetDirection = "right"
                elif e.key == K_s: #speed slider
                    sliderDirection = "down"
                elif e.key == K_w:#speed slider
                    sliderDirection = "up"
                
                
                #THE FOLLOWING ENABLE CHEATS TO HELP DEBUG OR TEST, UNCOMMENT THESE TO ENABLE THESE CHEATS
                #PRESS P TO WIN INSTANTLY
                #PRESS O TO ADD A ROBOT PART TO THE COLLECTED PARTS
                #PRESS I TO DIE INSTANTLY
               
                elif e.key == K_p: 
                    won= True
                elif e.key == K_o:
                    cheatNum += 1
                    partsCollected.append(partsList[cheatNum])
                elif e.key == K_i:
                    healthNum= 5
                
                    
            if e.type == MOUSEBUTTONDOWN: #when you click
                if won == False: #Clicks will not register if you are in the win sequence aka have already won
                    mouseX, mouseY= e.pos #saves mouse x and y cords
                    if mouseX<75 and mouseX>25 and mouseY > 525 and mouseY < 575:
                        if Hitboxes== True: #if your mouse is over the hitbox button it will toggle hitboxes on or off
                            #depending on what they were toggled to previously
                            Hitboxes = False
                        elif Hitboxes== False:
                            Hitboxes= True
                    elif mouseX>10 and mouseX<70 and mouseY > 10 and mouseY < 40:
                        currentScreen= "startMenu" #if you press the start button all variables are reset 
                        #and you are sent back to start menu
                        
                        #IF YOU COMMENT OUT RESTART = TRUE YOU CAN EFFECTIVLEY SAVE YOUR PROGRESS, SAVING YOUR PROGRESS WHEN YOU GO BACK INTO THE GAME
                        #THIS CAN BE USED FOR DEBUGGING OR TESTING
                        
                        restart= True
                    elif shoot == False: #If the mouse is not on the hitbox toggle or back button, the gun will shoot a laser
                        if missAnimation== False:
                            shoot = True
                            shootCord= (magnetCord+82) #will shoot from the center of the magnet gun (since the laser is 11 pixels wide 
                            #this will spawn it in the exact center of the gun)
                    
        elif currentScreen == "startMenu": #When you are on start menu
            if e.type == MOUSEMOTION:
                mx, my = e.pos #saves mouse cords
                if mx > 365 and mx < 635: #checks what button the mouse is hovering over
                    if my > 175 and my < 258:
                        clickArea = 1
                    elif my > 263 and my < 346:
                        clickArea = 2
                    elif my > 355 and my < 438:
                        clickArea = 3
                    else:
                        clickArea = 0
                else:
                    clickArea = 0

            elif e.type == MOUSEBUTTONDOWN:
                if clickArea != 0: #check where your mouse was when you clicked, then reacts accoringly
                    if clickArea == 3:
                        running = False #quit button
                    elif clickArea == 2: #how to play button
                        currentScreen = "tutorial"
                    elif clickArea == 1: #start button
                        currentScreen = "mainGame"

    if restartScreen== True: #if you are on the died / won screen
        if died== True: #if you lost will show you died screen
            drawImage(0,0, restartList[clickSpot])
        elif won== True: #if you won will show you won screen
            drawImage(0,0, winList[clickSpot]) 
        #since the died and won screen both have quit and restart I resued the code
    elif currentScreen == "tutorial": #when you are in the tutorial you will see the game guide
        drawImage(0, 0, Tutorial)
        drawImage(50,130, backButton)
    elif currentScreen == "startMenu": #if you are on the start menu the game will highlight the button you are hovering over
        drawImage(0, 0, menuList[clickArea])
        garbageX, direction = moveObject(menuList[4], garbageX, direction) #will draw the garbage can moving constatly
        
    elif currentScreen == "mainGame": #MAIN GAME 
        if (len(partsCollected)) == ((len(partsList))-1): #when you collect all the robot parts, you win
            won= True        
        drawGame() #draws all game images needed, in the coordinates they should be
        if restartScreen== False: #if you are still alive and have not won:
            drawTargets(targetX) #Draws targets
            if missAnimation== True: #when you are in the miss animation you can do everything exept move you GUN and shoot, you can still change speed and enable hitboxes etc.
                missAnimation, missCord= missDraw(missCord, (magnetCord+43)) # persice number so the guards always visually hit the magnet gun
                if missAnimation == False: #If the miss animation is done, the y cord is reset
                    missCord= 800
            targetSpeed= (((len(partsCollected))/1.1)+2) #The targets move faster as you collect more robot parts
            if won == False and died == False: #if you have not won or died, the targets will move the specified amount (set in line above)
                targetX= targetX-targetSpeed
            else: #if you have won or died:
                targetX+= 2 #the targets will move into the factory, start of win animations
                if targetX < 840: #while the targets are moving back into the factory, the robots eyes are red
                    drawImage( 800, 420, robotMove[1])
                else: #once the targets are off screen the robots eyes turn back to normal for now
                    robotState += 1 #the robot animation progresses to its next stage every 7 "loops"
                    if robotState < 27:
                        currentRobot= int(robotState/7)
                    elif robotState > 27: #one the robot animation AND factory animation are done, the you win screen shows up
                        if robotState > 128:
                            time.wait(500)
                            restartScreen= True
                        currentFactory= int((robotState-27)/6) #The factory animation will move stages every 6 "loops"
                        #it is a 17 stage animation
                        if robotState > 128: #Once the factory is done, it is locked at stage 17 during the 500 millisecond wait
                            currentFactory= 16
                        drawImage(825, 50, factoryMove[currentFactory]) #will draw factory
                        drawImage(835, 205, winBeam) #draws robots "anti polluition beam" that turning factory into trees
                    
                    drawImage(800, 420,robotMove[currentRobot]) #draws robot
                    time.wait(200) #waits between robot stages
                    
            if targetX <= -125: #whenver a target is fully off the screen, it moves back to zero
                #this gives the illusion of an infinite target stream (the images dont move back, just the rectangles)
                targetX= 0 
                targetList.append(targetList[0]) #adds image that is off screen to the back of the list
                del targetList[0] #deletes the image
                targetRect.append(targetRect[0]) #adds rectangle that is off screen to the end of the list
                del targetRect[0] #deletes off screen rectangle
        
            if robotState <= 27: #
                drawImage(825, 50, menuList[5]) #While robot animation is on but factory animation is not on
                #the factory will stay normal
            if shoot == True: #if you shoot and you have the magnet speed above 75%, the laser will move slower
                if magnetSpeed > 8.5:
                    Slow= True
                    shotCord= magnetBeam(shootCord, shotCord, Slow)
                else: #if the speed is not above 75% the laser moves normal speed
                    shotCord= magnetBeam(shootCord, shotCord, Slow)
                if shotCord < 169: #when the target hits a certain number (slow or normal speed)
                    #it will disappear and calculate what it hit in the same fram, keeping the game looking smooth
                    missAnimation= targetHit(shootCord, shotCord)
                if shotCord < 170:
                    shoot = False
                    Slow= False
                    shotCord = 500 #resets y cord of laser
                    
            if missAnimation == False and shoot== False: #if the laser is not traveling and
                #you are not in the middle of the miss animation
                if magnetDirection != "noMove" : #the magnet will keep moving if you hold down a or d
                    if magnetDirection == "left":
                        magnetCord = magnetCord - magnetSpeed
                    elif magnetDirection == "right":
                        magnetCord = magnetCord + magnetSpeed
                    
                    if magnetCord >= 50 and magnetCord <= 680: #when the magnet gun is in the border of the magnet gun rail
                        ()
                    else:
                        if magnetCord < 50: #if it tries to move past the border, it will reset to the edge or the rail
                            magnetCord = 50 #left or right edge
                        elif magnetCord > 680: 
                            magnetCord = 680
                
            if sliderDirection != "noMove": #if the w or s are held down the speed control will keep moving
                currentSpeed = magnetSpeed #saves current speed in case you try to move the slider past the limit
                if sliderCord >= 290 and sliderCord <= 490:
                    if sliderDirection == "down":
                        sliderCord+= 3 #will increase or lower speed, and move the speed control visually
                        magnetSpeed = magnetSpeed - 0.15  
                    elif sliderDirection == "up":
                        sliderCord= sliderCord-3
                        magnetSpeed += 0.15                 
                if sliderCord < 290: #if you try to move the slider of the rails, it will reset to the previous speed
                    sliderCord = 290 #stopping any speed exploits
                    magnetSpeed = currentSpeed
                if sliderCord > 490:
                    sliderCord = 490
                    magnetSpeed = currentSpeed    


    display.flip() #Displays EVERYTHING that was drawn
    myClock.tick(60)  # waits long enough to have 60 fps (mr. Van rooyen code)

quit() #quits game 
