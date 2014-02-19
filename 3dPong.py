# 3D PONG with Targets

from Tkinter import *
import random
import tkFont
import tkFileDialog
import tkSnack
import pygame


def play_sound(music_file):
    pygame.mixer.init()
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

def mousePressed(event):
    
    if(canvas.data.onTitleScreen):
        if((event.x>=canvas.data.startButtonX) and
            (event.x<=canvas.data.startButtonX+canvas.data.startSizeX)and(event.y>=canvas.data.startButtonY) and (event.y<=canvas.data.startButtonY+canvas.data.startSizeY)):
            canvas.data.onTitleScreen=False
            
        if((event.x>=canvas.data.startButtonX) and
            (event.x<=canvas.data.startButtonX+canvas.data.startSizeX)and(event.y>=canvas.data.startButtonY+100) and (event.y<=canvas.data.startButtonY+canvas.data.startSizeY+100)):
            canvas.data.onInfoScreen=True
            canvas.data.onTitleScreen=False
            canvas.delete(ALL)

    elif(canvas.data.onInfoScreen):
         if((event.x>=canvas.data.backX) and
            (event.x<=canvas.data.backX+canvas.data.backButtonSizeX)and(event.y>=canvas.data.backY) and (event.y<=canvas.data.backY+canvas.data.backButtonSizeY)):
             canvas.data.onInfoScreen=False
             canvas.data.onTitleScreen=True
             canvas.delete(ALL)
    
    else:
        canvas.data.missed=False
        canvas.data.stopped=False
        canvas.data.ballFill="yellow"
    redrawAll()
    
def Move(event):
    x, y = event.x, event.y
    canvas.data.mouseX=x
    canvas.data.mouseY=y
    
     
def keyPressed(event):
    if (event.char == "c"):
        canvas.data.levelCheat=True
      
    elif (event.char == "f")and(canvas.data.onTitleScreen):
        canvas.data.freePlayMode=True
    elif (event.char == "l")and(canvas.data.onTitleScreen):
        canvas.data.freePlayMode=False
    elif (event.char == "p"):
        canvas.data.isPaused = not canvas.data.isPaused
    elif (event.char == "s"):
        
        doTimerFired()
        
    elif (event.char == "r"):
        init()
    redrawAll()

def update():
    canvas.data.AICenterX=canvas.data.AISizeX/2+canvas.data.AILeft
    canvas.data.AICenterY=canvas.data.AISizeY/2+canvas.data.AITop
    canvas.data.ballCenterX=canvas.data.ballLeft+canvas.data.ballSize/2
    canvas.data.ballCenterY=canvas.data.ballTop+canvas.data.ballSize/2
    
def doTimerFired():
    canvas.data.counter += 1
   
    if(not canvas.data.stopped):
        hitBall()
        if(not canvas.data.missed):
            moveWholeBall()
            
            update()
           
        
        if(canvas.data.ballGrowing): canvas.data.x=0
        
      
        if(canvas.data.haveTargets):
            removeTargets()
        else:
            if((not canvas.data.ballGrowing)and(canvas.data.x==0)):
                predictMotion()
                canvas.data.x=1
            hitAI()
            aiFollowBall(canvas.data.gotoCenterX,canvas.data.gotoCenterY)
    redrawAll() 
    

def predictMotion():
    templeft=canvas.data.ballLeft
    temptop=canvas.data.ballTop
    tempsize=canvas.data.ballSize
    tempstep=canvas.data.moveStep
    tempgrow=canvas.data.ballGrowing
    tempbcornerx=canvas.data.borderCornerX
    tempbcornery=canvas.data.borderCornerY
    tempbsizex=canvas.data.borderSizeX
    tempbsizey=canvas.data.borderSizeY
    tempballcenterx,tempballcentery=canvas.data.ballCenterX,canvas.data.ballCenterY
    while(canvas.data.ballSize>=canvas.data.minSize):

        
        canvas.data.testingAI=True
        moveWholeBall()
        update()
       
        
    
    canvas.data.gotoCenterX=canvas.data.ballLeft+canvas.data.ballSize/2
    canvas.data.gotoCenterY=canvas.data.ballTop+canvas.data.ballSize/2
    
    canvas.data.ballCenterX,canvas.data.ballCenterY= tempballcenterx,tempballcentery
    canvas.data.ballGrowing=tempgrow
    
    canvas.data.ballLeft=templeft
    canvas.data.ballTop=temptop
    canvas.data.ballSize=tempsize
    canvas.data.moveStep=tempstep
    canvas.data.borderCornerX=tempbcornerx
    canvas.data.borderCornerY=tempbcornery
    canvas.data.borderSizeX=tempbsizex
    canvas.data.borderSizeY=tempbsizey
    canvas.data.testingAI=False
    
    
def moveWholeBall():
    moveBall()
    changeBallSize()
    changeMoveStep()
    changeBorderSize()
def moveLeft():
    canvas.data.ballLeft -= canvas.data.moveStep

def moveRight():
    canvas.data.ballLeft += canvas.data.moveStep

def moveUp():
    canvas.data.ballTop -= canvas.data.moveStep

def moveDown():
    canvas.data.ballTop += canvas.data.moveStep

def moveTarget(left,top,xspeed,yspeed,cornerX,cornerY,sizeX,SizeY):
    space=2
    
    if (canvas.data.headingRight == True):
        if (canvas.data.ballLeft + canvas.data.ballSize > canvas.data.borderCornerX+canvas.data.borderSizeX-(space+3)):
            canvas.data.headingRight = False
        else:
            moveRight()
    else:
        if (canvas.data.ballLeft < canvas.data.borderCornerX+space):
            canvas.data.headingRight = True
        else:
            moveLeft()
    if (canvas.data.headingDown == True):
        if (canvas.data.ballTop + canvas.data.ballSize > canvas.data.borderCornerY+canvas.data.borderSizeY-(space+4)):
            canvas.data.headingDown = False
        else:
            moveDown()
    else:
        if (canvas.data.ballTop < canvas.data.borderCornerY+space):
            canvas.data.headingDown = True
        else:
            moveUp()
def moveBall():
    space=2
    
    if (canvas.data.headingRight == True):
        if (canvas.data.ballLeft + canvas.data.ballSize > canvas.data.borderCornerX+canvas.data.borderSizeX-(space+3)):
            canvas.data.headingRight = False
        else:
            moveRight()
    else:
        if (canvas.data.ballLeft < canvas.data.borderCornerX+space):
            canvas.data.headingRight = True
        else:
            moveLeft()
    if (canvas.data.headingDown == True):
        if (canvas.data.ballTop + canvas.data.ballSize > canvas.data.borderCornerY+canvas.data.borderSizeY-(space+4)):
            canvas.data.headingDown = False
        else:
            moveDown()
    else:
        if (canvas.data.ballTop < canvas.data.borderCornerY+space):
            canvas.data.headingDown = True
        else:
            moveUp()


def removeTargets():
    for target in canvas.data.targets:
        if(ballHitTarget(target[3],target[4],target[2])):
            canvas.data.targets.remove(target)
            if(canvas.data.freePlayMode): createTarget()
        
def ballHitTarget(centerx,centery,size):
    ballcenterx=canvas.data.ballLeft+canvas.data.ballSize/2
    ballcentery=canvas.data.ballTop+canvas.data.ballSize/2
    ballsize=canvas.data.ballSize
    if((ballsize>=size-10)and(ballsize<=size+10)and(abs(ballcenterx-centerx)<=size/2+ballsize/2)and(abs(ballcentery-centery)<=size/2+ballsize/2)):
        canvas.data.score+=1
        if((canvas.data.freePlayMode)and(canvas.data.delay>=2)and(canvas.data.score % 2==0)): canvas.data.delay=canvas.data.delay-2
        soundFile="hit1.wav"
        play_sound(soundFile)
        return True
    return False


def hitBall():
    mouseX=canvas.data.mouseX
    mouseY=canvas.data.mouseY
    paddleSizeX=canvas.data.paddleSizeX
    paddleSizeY=canvas.data.paddleSizeY   
    right= canvas.data.headingRight
    down= canvas.data.headingDown
    ballLeft=canvas.data.ballLeft
    ballTop=canvas.data.ballTop
    ballSize=canvas.data.ballSize
    ballCenterX=ballLeft+ballSize/2
    ballCenterY=ballTop+ballSize/2
    maxSize=canvas.data.maxSize
    topLeft=(ballSize>=maxSize-3)and((ballCenterX>mouseX-paddleSizeX/2-ballSize/2)and(ballCenterY>mouseY-paddleSizeY/2-ballSize/2)
                                      and(ballCenterX<mouseX)and(ballCenterY<mouseY))
    #
    bottomLeft=(ballSize>=maxSize-3)and((ballCenterX>mouseX-paddleSizeX/2-ballSize/2)and(ballCenterY<mouseY+paddleSizeY/2+ballSize/2)
                                      and(ballCenterX<mouseX)and(ballCenterY>mouseY))
    #
    topRight=(ballSize>=maxSize-3)and((ballCenterX<mouseX+paddleSizeX/2+ballSize/2)and(ballCenterY>mouseY-paddleSizeY/2-ballSize/2)
                                      and(ballCenterX>mouseX)and(ballCenterY<mouseY))

    bottomRight=(ballSize>=maxSize-3)and((ballCenterX<mouseX+paddleSizeX/2+ballSize/2)and(ballCenterY<mouseY+paddleSizeY/2+ballSize/2)
                                      and(ballCenterX>mouseX)and(ballCenterY>mouseY)) 
    soundfile="ballbounce.wav"

    if(topLeft):
        if((canvas.data.headingRight)and(canvas.data.headingDown)):
            canvas.data.headingRight=False
            canvas.data.headingDown=False
            
        elif((not canvas.data.headingRight)and(canvas.data.headingDown)):
            canvas.data.headingRight=False
            canvas.data.headingDown=False
    
        elif(canvas.data.headingRight): canvas.data.headingRight=False

        canvas.data.alreadyHit+=1
        if(not canvas.data.missed)and(canvas.data.alreadyHit==1): play_sound(soundfile)
                            
        return "topLeft"
    elif(bottomLeft):
     
        if((canvas.data.headingRight)and(not canvas.data.headingDown)):
            canvas.data.headingRight=False
            canvas.data.headingDown=True
        
        elif(canvas.data.headingRight): canvas.data.headingRight=False
        canvas.data.alreadyHit+=1
        if(not canvas.data.missed)and(canvas.data.alreadyHit==1): play_sound(soundfile)
        return "bottomLeft"
    elif(topRight):
    
        if((not canvas.data.headingRight)and(canvas.data.headingDown)):
            canvas.data.headingRight=True
            canvas.data.headingDown=False
        elif((canvas.data.headingRight)and(canvas.data.headingDown)): canvas.data.headingDown=False
        elif((not canvas.data.headingRight)and(not canvas.data.headingDown)):
            canvas.data.headingRight=True
        canvas.data.alreadyHit+=1
        if(not canvas.data.missed)and(canvas.data.alreadyHit==1): play_sound(soundfile) 
        return "topRight"
    elif(bottomRight):
       
        if((not canvas.data.headingRight)and(canvas.data.headingDown)):
            canvas.data.headingRight=True
            canvas.data.headingDown=True
        elif((canvas.data.headingRight)and(not canvas.data.headingDown)): canvas.data.headingDown=True
        elif((not canvas.data.headingRight)and(not canvas.data.headingDown)):
            canvas.data.headingRight=True
            canvas.data.headingDown=True
            
        canvas.data.alreadyHit+=1
        if(not canvas.data.missed)and(canvas.data.alreadyHit==1): play_sound(soundfile)
        return "bottomRight"
    elif((ballSize>=maxSize)and(not topLeft)and(not topRight)and(not bottomLeft)and(not bottomRight)):
        if(canvas.data.missed==False): canvas.data.lives-=1
        canvas.data.ballFill="Blue"
        canvas.data.missed=True


def hitAI():
    AICenterX=canvas.data.AICenterX
    AICenterY=canvas.data.AICenterY
    AISizeX=canvas.data.AISizeX
    AISizeY=canvas.data.AISizeY   
    right= canvas.data.headingRight
    down= canvas.data.headingDown
    ballLeft=canvas.data.ballLeft
    ballTop=canvas.data.ballTop
    ballSize=canvas.data.ballSize
    ballCenterX=ballLeft+ballSize/2
    ballCenterY=ballTop+ballSize/2
    minSize=canvas.data.minSize
    topLeft=(ballSize<=minSize+3)and((ballCenterX>AICenterX-AISizeX/2-ballSize/2)and(ballCenterY>AICenterY-AISizeY/2-ballSize/2)
                                      and(ballCenterX<AICenterX)and(ballCenterY<AICenterY))
    #
    bottomLeft=(ballSize<=minSize+3)and((ballCenterX>AICenterX-AISizeX/2-ballSize/2)and(ballCenterY<AICenterY+AISizeY/2+ballSize/2)
                                      and(ballCenterX<AICenterX)and(ballCenterY>AICenterY))
    #
    topRight=(ballSize<=minSize+3)and((ballCenterX<AICenterX+AISizeX/2+ballSize/2)and(ballCenterY>AICenterY-AISizeY/2-ballSize/2)
                                      and(ballCenterX>AICenterX)and(ballCenterY<AICenterY))

    bottomRight=(ballSize<=minSize+3)and((ballCenterX<AICenterX+AISizeX/2+ballSize/2)and(ballCenterY<AICenterY+AISizeY/2+ballSize/2)
                                      and(ballCenterX>AICenterX)and(ballCenterY>AICenterY)) 

    if(topLeft):
        if((canvas.data.headingRight)and(canvas.data.headingDown)):
            canvas.data.headingRight=False
            canvas.data.headingDown=False
        elif((not canvas.data.headingRight)and(canvas.data.headingDown)):
            canvas.data.headingRight=False
            canvas.data.headingDown=False
        elif(canvas.data.headingRight): canvas.data.headingRight=False
    elif(bottomLeft):
     
        if((canvas.data.headingRight)and(not canvas.data.headingDown)):
            canvas.data.headingRight=False
            canvas.data.headingDown=True
        elif(canvas.data.headingRight): canvas.data.headingRight=False
    elif(topRight):
    
        if((not canvas.data.headingRight)and(canvas.data.headingDown)):
            canvas.data.headingRight=True
            canvas.data.headingDown=False
        elif((canvas.data.headingRight)and(canvas.data.headingDown)): canvas.data.headingDown=False
        elif((not canvas.data.headingRight)and(not canvas.data.headingDown)):
            canvas.data.headingRight=True
        print True
    elif(bottomRight):
       
        if((not canvas.data.headingRight)and(canvas.data.headingDown)):
            canvas.data.headingRight=True
            canvas.data.headingDown=True
        elif((canvas.data.headingRight)and(not canvas.data.headingDown)): canvas.data.headingDown=True
        elif((not canvas.data.headingRight)and(not canvas.data.headingDown)):
            canvas.data.headingRight=True
            canvas.data.headingDown=True
        
    elif((ballSize<=minSize+5)and(not topLeft)and(not topRight)and(not bottomRight)and(not bottomLeft)):
        canvas.data.ballFill="red"
        canvas.data.missed=True

    
    
def changeMoveStep():
    if((not canvas.data.ballGrowing)):
        canvas.data.moveStep=canvas.data.moveStep-.01
        
    elif((canvas.data.ballGrowing)):
        canvas.data.moveStep=canvas.data.moveStep+.01
    if(canvas.data.ballSize<70): canvas.data.alreadyHit=0
        
   
    


def changeBallSize():
    minSize=canvas.data.minSize
    maxSize=canvas.data.maxSize
    rate=1.01
    ratemove=1.001
    rateborder=1.01
    if((not canvas.data.ballGrowing)and(canvas.data.ballSize<=minSize)):
        canvas.data.ballGrowing=True
        canvas.data.ballSize=canvas.data.ballSize*rate
        canvas.data.moveStep=canvas.data.moveStep*ratemove
        
    elif((canvas.data.ballGrowing)and(canvas.data.ballSize>minSize)and(canvas.data.ballSize<maxSize)):
        canvas.data.ballSize=canvas.data.ballSize*rate
        canvas.data.moveStep=canvas.data.moveStep*ratemove
    elif((canvas.data.ballGrowing)and(canvas.data.ballSize>=maxSize)):
        canvas.data.ballSize=canvas.data.ballSize*(1-(rate-1))
        canvas.data.moveStep=canvas.data.moveStep*(1-(ratemove-1))
        
        canvas.data.ballGrowing=False
    elif((not canvas.data.ballGrowing)and(canvas.data.ballSize>minSize)and(canvas.data.ballSize<=maxSize)):
        canvas.data.ballSize=canvas.data.ballSize*(1-(rate-1))
        canvas.data.moveStep=canvas.data.moveStep*(1-(ratemove-1))
    
    

def changeBorderSize():
    minSize=canvas.data.minSize
    maxSize=canvas.data.maxSize
    rate=1.2
    rated=2.4
    if((not canvas.data.ballGrowing)):
        changeBorderCorner(rate)
        adjustBorder(-1.0*rated)
        
    elif((canvas.data.ballGrowing)):
        changeBorderCorner(-1.0*rate)
        adjustBorder(rated)

def changeBorderCorner(rate):
    canvas.data.borderCornerX=canvas.data.borderCornerX+rate
    canvas.data.borderCornerY=canvas.data.borderCornerY+rate
    
def adjustBorder(rate):
    canvas.data.borderSizeX=canvas.data.borderSizeX+rate
    canvas.data.borderSizeY=canvas.data.borderSizeY+rate


    
     
    

def canAIMove(left,top):
    spacex=canvas.data.spaceX
    spacey=canvas.data.spaceY
    maxs=canvas.data.maxs
    maxs1=canvas.data.maxs1
    maxsy=canvas.data.maxsy
    
    if((left>maxs+spacex)and(left+canvas.data.AISizeX<canvas.data.canvasWidth-maxs1-spacex)and(top>maxs)
       and(top+canvas.data.AISizeY<canvas.data.canvasHeight-maxsy-spacey)): return True
    
    return False

def calcAIMoveStep():
    return abs(canvas.data.AICenterX-canvas.data.ballCenterX)/20,abs(canvas.data.AICenterY-canvas.data.ballCenterY)/20
def aiFollowBall(centerX,centerY):
    update()
    
    AIcenterX,AIcenterY=canvas.data.AICenterX,canvas.data.AICenterY
    if((abs(AIcenterX-centerX)>5)and(abs(AIcenterY-centerY)>5)):
        print "x"
        moveStepX,moveStepY=calcAIMoveStep()

        topLeft=((centerX<AIcenterX)and(centerY<AIcenterY))
        topRight=((centerX>AIcenterX)and(centerY<AIcenterY))
        bottomLeft=((centerX<AIcenterX)and(centerY>AIcenterY))
        bottomRight=((centerX>AIcenterX)and(centerY>AIcenterY))
        left=canvas.data.AILeft
        top=canvas.data.AITop

        if((topLeft)):
            left-=moveStepX
            top-=moveStepY
        elif((topRight)):
            left+=moveStepX
            top-=moveStepY
        elif((bottomLeft)):
            left-=moveStepX
            top+=moveStepY
        elif((bottomRight)):
            left+=moveStepX
            top+=moveStepY
            
        canMove=canAIMove(left,top)
       
        if(canMove):
            canvas.data.AILeft=left
            canvas.data.AITop=top
        
        update()
      
    
def createTarget():
    newTarget=[]
    size=5*random.randint(5,14)
    xspeed=random.randint(3,8)
    yspeed=random.randint(3,8)
    #left=11.56*size-89.295
    
    left=random.randint((canvas.data.maxs-10),(canvas.data.canvasWidth-canvas.data.maxs1-5))
    #top=-6.267*size+581.832
    top=random.randint(canvas.data.maxs-5,canvas.data.canvasHeight-canvas.data.maxsy+5)
    minCornerX=196.754-2.206*size
    minCornerY=minCornerX
    maxWidth=minCornerX+4.231*size+611.8
    maxHeight=maxWidth-300
    
    newTarget.append(left)
    newTarget.append(top)
    newTarget.append(size)
    newTarget.append(left+size/2)
    newTarget.append(top+size/2)
    newTarget.append(xspeed)
    newTarget.append(yspeed)
    newTarget.append(minCornerX)
    newTarget.append(minCornerY)
    newTarget.append(maxWidth)
    newTarget.append(maxHeight)
    canvas.data.targets.append(newTarget)
    return newTarget



def timerFired():
    update()
    if (not canvas.data.isGameOver)and(canvas.data.isPaused == False):
        doTimerFired()
      
    
   
    delay=canvas.data.delay
    canvas.after(delay, timerFired) # pause, then call timerFired again


def levelRunner():
    if((len(canvas.data.targets)==0)or(canvas.data.levelCheat)):
        
        canvas.data.level+=1
        canvas.data.delay-=2
        initTargets()
        canvas.data.newLevel=True
        canvas.data.levelCheat=False
        canvas.data.stopped=True
    if(canvas.data.level==7):
        canvas.data.win=True
        canvas.data.isGameOver=True

def drawAI():
   
    canvas.create_rectangle(canvas.data.AILeft,canvas.data.AITop,
                            canvas.data.AILeft+canvas.data.AISizeX,canvas.data.AITop+canvas.data.AISizeY,fill="gray",stipple="gray25")
    canvas.create_line ( canvas.data.AILeft, canvas.data.AITop+canvas.data.AISizeY/2, canvas.data.AILeft+canvas.data.AISizeX, canvas.data.AITop+canvas.data.AISizeY/2,fill="red")
    canvas.create_line ( canvas.data.AICenterX, canvas.data.AITop, canvas.data.AICenterX, canvas.data.AITop+canvas.data.AISizeY,fill="red")

def drawWinner():
    canvas.create_text(500,200,text="CONGRATS! YOU BEAT THE GAME!",font="Times 40",fill="white")
    canvas.create_text(500,400,text="Press (r) to go back to the menu",font="Times 20",fill="white")
    

def drawLevel():
    levelRunner()
    canvas.create_text(500,100,text="Level %d"%(canvas.data.level),font="Times 40",fill="red")
    
def drawFlash():
    pos=hitBall()
    if(pos=="topLeft"):
        canvas.create_rectangle(canvas.data.mouseX-canvas.data.paddleSizeX/2,canvas.data.mouseY-canvas.data.paddleSizeY/2,canvas.data.mouseX,canvas.data.mouseY,fill="white",stipple="gray50")
    elif(pos=="bottomLeft"):
        canvas.create_rectangle(canvas.data.mouseX-canvas.data.paddleSizeX/2, canvas.data.mouseY, canvas.data.mouseX, canvas.data.mouseY+canvas.data.paddleSizeY/2,fill="white",stipple="gray50")
    elif(pos=="topRight"):
        canvas.create_rectangle(canvas.data.mouseX, canvas.data.mouseY-canvas.data.paddleSizeY/2,canvas.data.mouseX+canvas.data.paddleSizeX/2, canvas.data.mouseY,fill="white",stipple="gray50")
    elif(pos=="bottomRight"):
        canvas.create_rectangle(canvas.data.mouseX,canvas.data.mouseY,canvas.data.mouseX+canvas.data.paddleSizeX/2,canvas.data.mouseY+canvas.data.paddleSizeY/2,fill="white",stipple="gray50")

def drawPaddle():

    
    canvas.create_rectangle(canvas.data.mouseX-canvas.data.paddleSizeX/2,canvas.data.mouseY-canvas.data.paddleSizeY/2,
                            canvas.data.mouseX+canvas.data.paddleSizeX/2,canvas.data.mouseY+canvas.data.paddleSizeY/2,fill="gray",stipple="gray25")
    canvas.create_line ( canvas.data.mouseX-canvas.data.paddleSizeX/2, canvas.data.mouseY, canvas.data.mouseX+canvas.data.paddleSizeX/2, canvas.data.mouseY,fill="blue")
    canvas.create_line ( canvas.data.mouseX, canvas.data.mouseY-canvas.data.paddleSizeY/2, canvas.data.mouseX, canvas.data.mouseY+canvas.data.paddleSizeY/2,fill="blue")

def drawBackground():
    canvas.create_rectangle(0,0,canvas.data.canvasWidth,canvas.data.canvasHeight,fill="white")
def drawBorder():
    
    canvas.create_rectangle(canvas.data.borderCornerX,canvas.data.borderCornerY,canvas.data.borderCornerX+canvas.data.borderSizeX,
                            canvas.data.borderCornerY+canvas.data.borderSizeY,fill=None,outline="yellow",width=3)
    
def drawBall():
     canvas.create_oval(canvas.data.ballLeft,
                            canvas.data.ballTop,
                            canvas.data.ballLeft + canvas.data.ballSize,
                            canvas.data.ballTop + canvas.data.ballSize,
                            fill=canvas.data.ballFill)
def drawAllTargets():
    for target in canvas.data.targets:
        
        drawTarget(target[0],target[1],target[2])
    
def drawTarget(left,top,size):
    spacing=size/5
    canvas.create_oval(left,top,left+size,top+size,fill=None,outline="red",width=size/5)
    canvas.create_oval(left+spacing,top+spacing,left+4*spacing,top+4*spacing,fill="white")
    canvas.create_oval(left+spacing*2,top+spacing*2,left+3*spacing,top+3*spacing,fill="red")
    


def drawDepth():
    spacex=canvas.data.spaceX
    spacey=canvas.data.spaceY
    maxs=canvas.data.maxs
    maxs1=canvas.data.maxs1
    maxsy=canvas.data.maxsy
    #canvas.create_line(canvas.data.canvasWidth-maxs1,canvas.data.canvasWidth
    canvas.create_polygon(spacex, spacey,maxs,maxs ,maxs, canvas.data.canvasHeight-maxsy-spacey,spacex, canvas.data.canvasHeight-spacey,fill="LimeGreen")
    canvas.create_polygon(canvas.data.canvasWidth-spacex, spacey,canvas.data.canvasWidth-maxs1-spacex, maxs,
                          canvas.data.canvasWidth-maxs1-spacex, canvas.data.canvasHeight-maxsy-spacey,canvas.data.canvasWidth-spacex, canvas.data.canvasHeight-spacey,fill="LimeGreen")

    canvas.create_polygon(spacex, spacey,maxs,maxs,
                          canvas.data.canvasWidth-maxs1-spacex, maxs,canvas.data.canvasWidth-spacex, spacey,fill="Black")
    canvas.create_polygon(spacex, canvas.data.canvasHeight-spacey,maxs, canvas.data.canvasHeight-maxsy-spacey,
                          canvas.data.canvasWidth-maxs1-spacex, canvas.data.canvasHeight-maxsy-spacey,canvas.data.canvasWidth-spacex, canvas.data.canvasHeight-spacey,fill="Black") 

    canvas.create_rectangle(0,spacey,spacex, canvas.data.canvasHeight-spacey,fill="GreenYellow")
    canvas.create_rectangle(canvas.data.canvasWidth,spacey,canvas.data.canvasWidth-spacex, canvas.data.canvasHeight-spacey,fill="GreenYellow")
    canvas.create_rectangle(0,0,canvas.data.canvasWidth,spacey,fill="DimGray")
    canvas.create_rectangle(0,canvas.data.canvasHeight-spacey,canvas.data.canvasWidth,canvas.data.canvasHeight,fill="DimGray")

    
    canvas.create_rectangle(maxs,maxs,canvas.data.canvasWidth-maxs1-spacex, canvas.data.canvasHeight-maxsy-spacey,fill="DimGray")
##    for x in xrange(spacex,maxs,35):
##         canvas.create_rectangle(x,x, canvas.data.canvasWidth-x,
##                         canvas.data.canvasHeight-x,fill=None,outline="LawnGreen",width=(maxs-x)*.03)

def drawText():
    # draw the text
    
    if((canvas.data.haveTargets)and(canvas.data.inGame)):
        canvas.create_text(200,20,text="Score: %d"%(canvas.data.score),fill="white",font=tkFont.Font(family="MS Sans Serif",size=18))
        canvas.create_text(400,20,text="Lives: ",fill="white",font=tkFont.Font(family="MS Sans Serif",size=18))
        for x in xrange(canvas.data.lives):
            canvas.create_oval(440+30*x,10,460+30*x,30,fill="red")
    
    canvas.create_text(150,180,text="Mouse Position %d,%d"%(canvas.data.mouseX,canvas.data.mouseY),fill="white")

def drawGameOver():
    canvas.create_text(500,200,text="GAME OVER",font="Times 60",fill="white")
    canvas.create_text(500,400,text="Press (r) to go back to the menu",font="Times 20",fill="white")
    
    
    
def drawInfo():
    info="Controls: \n\n Use the mouse to move the paddle to hit the ball. Aim at targets to score points.\n Depending on where the ball hits the paddle, the ball will bounce in different directions.\n\nIn Free Mode: Hit as many targets as you can. The ball will get faster so try to keep up\n\nIn Level Mode: Progress through 7 increasingly difficult levels to win"
    canvas.create_text(500,40,text="INSTRUCTIONS",font=tkFont.Font(family="Helvetica bold",size=40),fill="red")
    canvas.create_rectangle(canvas.data.backX,canvas.data.backY,canvas.data.backX+canvas.data.backButtonSizeX,canvas.data.backY+canvas.data.backButtonSizeY,fill="black")
    canvas.create_text(canvas.data.backX+43,canvas.data.backY+25,text="< Back",fill="white",font="Helvetica 18")
    canvas.create_text(500,200,text=info,font="Times 18")
def drawTitleScreen():
    canvas.create_text(500,200,text="3D-TARGET PONG",font="Times 60",fill="white")
    sizex=100
    sizey=40
    canvas.create_rectangle(canvas.data.startButtonX-5,canvas.data.startButtonY-5,canvas.data.startButtonX+canvas.data.startSizeX+5,canvas.data.startButtonY+canvas.data.startSizeY+5,fill="red")
    canvas.create_rectangle(canvas.data.startButtonX,canvas.data.startButtonY,canvas.data.startButtonX+canvas.data.startSizeX,canvas.data.startButtonY+canvas.data.startSizeY,fill="black")
    canvas.create_text(canvas.data.startButtonX+150,canvas.data.startButtonY+22,text="Play Game",fill="white",font=tkFont.Font(family="Helvetica",size=25))

    canvas.create_rectangle(canvas.data.startButtonX-5,canvas.data.startButtonY-5+100,canvas.data.startButtonX+canvas.data.startSizeX+5,canvas.data.startButtonY+canvas.data.startSizeY+5+100,fill="red")
    canvas.create_rectangle(canvas.data.startButtonX,canvas.data.startButtonY+100,canvas.data.startButtonX+canvas.data.startSizeX,canvas.data.startButtonY+canvas.data.startSizeY+100,fill="black")
    canvas.create_text(canvas.data.startButtonX+150,canvas.data.startButtonY+22+100,text="Instructions",fill="white",font=tkFont.Font(family="Helvetica",size=25))

    canvas.create_text(200,400,text="Pick a Mode: \n\n Free Play (f) \n\n Levels(l)",font="Times 20",fill="white")
def redrawAll():
    canvas.delete(ALL)
    
    if((not canvas.data.onTitleScreen)and(not canvas.data.onInfoScreen)):
        drawBackground()
        drawDepth()
        if(canvas.data.haveTargets):
            drawAllTargets()
        if(not canvas.data.freePlayMode):
            drawLevel()
        if(not canvas.data.testingAI):
            drawBall()
        drawText()
        #drawBorder()
        drawPaddle()

    if(not canvas.data.stopped and not canvas.data.missed):
        drawFlash()
    if( canvas.data.onTitleScreen):
        drawDepth()
        drawTitleScreen()
    if(canvas.data.onInfoScreen):
        drawInfo()
    if(canvas.data.lives==0):
        canvas.data.isGameOver=True
        drawGameOver()
    if((canvas.data.win)and(canvas.data.isGameOver)and(not (canvas.data.lives==0))):
        drawWinner()
   

def initTargets():
    
    canvas.data.targets=[]
    for x in xrange(canvas.data.maxTargets+1):
        createTarget()
    

def init():
    canvas.data.win=False
    canvas.data.levelCheat=False
    canvas.data.newLevel=True
    canvas.data.level=1
    canvas.data.freePlayMode=False
    canvas.data.isGameOver=False
    canvas.data.lives=3
    canvas.data.backX=50
    canvas.data.backY=canvas.data.canvasHeight-80
    canvas.data.backButtonSizeX=100
    canvas.data.backButtonSizeY=50
    canvas.data.onInfoScreen=False
    canvas.data.startSizeX=300
    canvas.data.startSizeY=50
    canvas.data.startButtonX=(canvas.data.canvasWidth-canvas.data.startSizeX)/2
    canvas.data.startButtonY=300
    canvas.delete(ALL)
    canvas.data.alreadyHit=0
    canvas.data.title=0
    canvas.data.onTitleScreen=True
    canvas.data.score=0
    canvas.data.inGame=True
    canvas.data.testingAI=False
    canvas.data.AISizeX=80
    canvas.data.AISizeY=60
    canvas.data.AILeft=canvas.data.canvasWidth/2-canvas.data.AISizeX/2
    canvas.data.AITop=canvas.data.canvasHeight/2-canvas.data.AISizeY/2
    canvas.data.AICenterX=canvas.data.AISizeX/2+canvas.data.AILeft
    canvas.data.AICenterY=canvas.data.AISizeY/2+canvas.data.AITop
    canvas.data.AIMoveStep=5
    canvas.data.maxTargets=4
    canvas.data.targets=[]
    canvas.data.haveTargets=True
    canvas.data.paddleSizeX=150
    canvas.data.paddleSizeY=90
    canvas.data.minSize=25
    canvas.data.maxSize=120
    canvas.data.moveStep=10
    canvas.data.borderCornerX=20
    canvas.data.borderCornerY=20
    canvas.data.borderSizeX= canvas.data.canvasWidth-43
    canvas.data.borderSizeY= canvas.data.canvasHeight-38
    canvas.data.ballGrowing=False
    canvas.data.ballLeft = 500
    canvas.data.ballTop = 400
    canvas.data.mouseX=0
    canvas.data.mouseY=0
    canvas.data.ballFill = "yellow"
    canvas.data.ballSize = canvas.data.maxSize-1
    canvas.data.ballCenterX=canvas.data.ballLeft+canvas.data.ballSize/2
    canvas.data.ballCenterY=canvas.data.ballTop+canvas.data.ballSize/2
    canvas.data.circleCenters = [ ]
    canvas.data.counter = 0
    canvas.data.headingRight = True
    canvas.data.headingDown = True
    canvas.data.isPaused = False
    canvas.data.missed=False
    canvas.data.spaceX=30
    canvas.data.spaceY=30
    canvas.data.maxs=208
    canvas.data.maxs1=188
    canvas.data.maxsy=188
    canvas.data.gotoCenterX=0
    canvas.data.gotoCenterY=0
    canvas.data.x=1
    canvas.data.stopped=True
    canvas.data.delay = 15
    if(canvas.data.haveTargets): initTargets()
    
    

def run():
    # create the root and the canvas
    global canvas
    global root
    root = Tk()
    root.title("3D PONG")
    canvasWidth = 1000
    canvasHeight = 700
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight)
    canvas.pack()
    # Set up canvas data and call init
    class Struct: pass
    canvas.data = Struct()
    canvas.data.canvasWidth = canvasWidth
    canvas.data.canvasHeight = canvasHeight

    init()
    # set up events
    root.bind("<Motion>", Move)
    root.bind("<Button-1>",mousePressed)
    root.bind("<Key>", keyPressed)
    timerFired()
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()
