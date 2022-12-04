from typing import Container
import pygame,sys,time,random,shutil
from pygame import display

from pygame.constants import K_LEFT, K_RIGHT, WINDOWHITTEST
from pygame.draw import circle
pygame.init()

screenWidth,screenHeight = (800,600)

screen = pygame.display.set_mode((screenWidth,screenHeight))

WHITE = (255,255,255)                   #colour rgbs
BLACK = (39,39,39,255)
DIMWHITE = (255,255,255,0.4)
RED = (253, 53, 64)
GREEN = (0,255,0)	
BLUE = (0,0,255)
GREY = (211,211,211)
GOLD = (212,190,127,255)

buttonWidth = 180
buttonHeight = 50
buttonSpace = 10
beforeCharacterWidth,beforeCharacterHeight = (150,192)
currentCharacterWidth,currentCharacterHeight = (250,320)
afterCharacterWidth,afterCharacterHeight = (150,192)
newList = []

buttonFont = pygame.font.SysFont("Roboto",30)
pageTitleFont = pygame.font.SysFont("Roboto",50)
countFont = pygame.font.SysFont("Roboto",120)
u_base_font = pygame.font.Font(None,32)
p_base_font = pygame.font.Font(None,32)
logoutFont = pygame.font.SysFont("Roboto",15)

usernameRect = pygame.Rect(screenWidth//2,screenHeight//3,200,32)
passwordRect = pygame.Rect(screenWidth//2,screenHeight//2,200,32)
submitRect = pygame.Rect((screenWidth//2)-buttonWidth//2,screenHeight//1.5,200,50)
scoreRect = pygame.Rect(20,20,200,85)
selectRect = pygame.Rect((screenWidth//2)-buttonWidth//2,screenHeight-100,200,50)
currentCharacterRect = pygame.Rect(screenWidth//2-(currentCharacterWidth//2),screenHeight-(currentCharacterHeight//2),currentCharacterWidth,currentCharacterHeight)
beforeCharacterRect = pygame.Rect(screenWidth//2,screenHeight-(beforeCharacterHeight//2),beforeCharacterWidth,beforeCharacterHeight)
afterCharacterRect = pygame.Rect((screenWidth//2)-(currentCharacterWidth//2)+120,(screenHeight//2)-(beforeCharacterHeight//2),beforeCharacterWidth,beforeCharacterHeight)
helpRect = pygame.Rect(25,25,50,50)
startRect = pygame.Rect(100,screenHeight-10,10,50)
endRect = pygame.Rect(screenWidth-100,screenHeight-10,10,50)
moveRect = pygame.Rect(100,screenHeight-100,10,10)
skipRect = pygame.Rect(screenWidth - (buttonWidth+10),screenHeight-150,buttonWidth,buttonHeight)
quitRect = pygame.Rect(10,screenHeight-150,buttonWidth,buttonHeight)
logoutRect = pygame.Rect(0,0,0,0)

color_active = BLUE
color_passive = (211,211,211)
u_color = color_passive
p_color = color_passive
u_active = False
p_active = False
user_text = ''
pass_text = ''
incorrectInfo = False
characterList = ["blackpanther2.jpg","blackpanther.jpg","blackpanther3.jpg"]
index = 1
beforeIndex = 0
afterIndex = 2
locked = False
level1List = [["JUMPING JACKS","level 1 images/jumping jacks.png","level 1 images/1.jpg",400,400,400,400],["PLANK HOLD","level 1 images/plank hold.jpg","level 1 images/2.jpg",400,400,400,400],["RUNNING ON SPOT","level 1 images/running.png","level 1 images/3.jpg",400,400,400,400],["HIGH KNEES","level 1 images/high knees.png","level 1 images/4.jpg",400,400,400,400],["LUNGES","level 1 images/lunge.png","level 1 images/5.jpg",400,400,400,400]]
level2List = [["SQUATS","level 2 images/squats.jpg","level 2 images/1.jpg",400,400,400,400],["SIT UPS","level 2 images/situps.jpg","level 2 images/2.jpg",400,400,400,400],["SIDE PLANK","level 2 images/sideplank.jpg","level 2 images/3.jpg",400,400,400,400],["PUSH UPS","level 2 images/pushup.jpg","level 2 images/4.jpg",400,400,400,400],["BENCH DIPS","level 2 images/dips.jpg","level 2 images/5.jpg",400,400,400,400]]
level3List = [["CLOSE-GRIP PUSHUP","level 3 images/closepushup.jpg", "level 3 images/1.jpg",400,400,400,400],["DECLINE PUSHUPS","level 3 images/declinepushup.jpg","level 3 images/2.jpg"],["JUMP SQAUTS","level 3 images/jumpsquat.jpg","level 3 images/3.jpg",400,400,400,400],["PIKE PUSHUPS","level 3 images/pikepushup.jpg","level 3 images/4.jpg",400,400,400,400],["PUNCHES","level 3 images/punching.jpg","level 3 images/5.jpg",400,400,400,400],["SEATED IN & OUTS","level 3 images/seatedin.jpg","level 3 images/6.jpg",400,400,400,400],["SPIDERMAN PUSHUPS","level 3 images/spidermanpushup.jpg","level 3 images/7.jpg",400,400,400,400]]
speed = 3
distance = 100
check = True
once = True
addScore = 20
penalty = 0




def loadImage(url,width,height,centerx,centery):
    logoVar = pygame.image.load(url)
    logoVar = pygame.transform.scale(logoVar, (width, height))
    logoRect = logoVar.get_rect()
    logoRect.center = (centerx,centery)
    screen.blit(logoVar,logoRect)
    return logoRect

def loadText(text,font,centerx,centery):
    if font == logoutFont:
      color = BLACK
    else:
      color = GOLD
    titleText = font.render(text,True,color)
    titleRect = titleText.get_rect()
    titleRect.center = (centerx,centery)
    screen.blit(titleText, titleRect)

def titleText(text,font,colour):
  titleText = font.render(text,True,colour)
  titleRect = titleText.get_rect()
  titleRect.center = (screenWidth//2,100)
  screen.blit(titleText,titleRect)

def user_pass(username, password, font, screenWidth, screenHeight): #function creates prompt text - username and password
  screenWidth,screenHeight = screen.get_size()
  usernameText = font.render(username,True,BLACK)                     #username
  usernameRect = usernameText.get_rect()
  usernameRect.topright = ((screenWidth//2)-50,screenHeight//3)
  screen.blit(usernameText,usernameRect)

  passwordText = font.render(password,True,BLACK)                     #password
  passwordRect = passwordText.get_rect()
  passwordRect.topright = ((screenWidth//2)-50,screenHeight//2)
  screen.blit(passwordText, passwordRect)

def input(screen, inputRect, color, base_font, text, color_active, color_passive, active):
  pygame.draw.rect(screen,color,inputRect,2)                        #anything typed into the input field becomes the text to be rendered and blitted
  text_surface = base_font.render(text,True,color)
  screen.blit(text_surface, (inputRect.x+5,inputRect.y+5))
  inputRect.w = max(200,text_surface.get_width() + 10)              #the input box will either be 200px or larger depending on how much you type
  if active:                                                        #when hovered, color becomes red
    color = BLACK
  else:
    color = GOLD
  return color,text 

condition = 1

go = True
while go:
  for event in pygame.event.get():
    mousePos = pygame.mouse.get_pos()
    if event.type ==pygame.QUIT:
      go = False
    if event.type == pygame.KEYDOWN:                              #when any key on the keyboard is down
      if u_active:
        if event.key == pygame.K_BACKSPACE:                         #delete text from input field on backspace
          user_text = user_text[:-1]
        elif event.key == pygame.K_RETURN:                          #leave the input field when enter is pressed
          u_active = False
          usernameValue = user_text                                 #store the value in the input field
        else:
          user_text += event.unicode                                #if not backspace or enter, add the value of the key(a,b,c,d...) to a variable
      if p_active:                                                  #same concept for password
        if event.key == pygame.K_BACKSPACE:                         #backspace deletes last key
          pass_text = pass_text[:-1]
        elif event.key == pygame.K_RETURN:                          #enter leaves the input field
          p_active = False
          usernameValue = user_text                                 #stores whatever is in the input field in a variable
        else:
          pass_text += event.unicode
      if event.key == pygame.K_ESCAPE:
        go = False
      if event.key == K_LEFT:
        index -= 1
        if index == 0:
          beforeIndex = 2
          afterIndex = 1
        if index == 1:
          beforeIndex = 0
          afterIndex = 2
        if index == 2:
          beforeIndex = 1
          afterIndex = 0
        if index == 3:
          index = 0
          beforeIndex = 2
          afterIndex = 1
        if index == -1:
          index = 2
          beforeIndex = 1
          afterIndex = 0
      if event.key == K_RIGHT:
        index += 1
        if index == 0:
          beforeIndex = 2
          afterIndex = 1
        if index == 1:
          beforeIndex = 0
          afterIndex = 2
        if index == 2:
          beforeIndex = 1
          afterIndex = 0
        if index == 3:
          index = 0
          beforeIndex = 2
          afterIndex = 1
        if index == -1:
          index = 2
          beforeIndex = 1
          afterIndex = 0
    if event.type == pygame.MOUSEBUTTONDOWN:
      if condition == 1 and loginRect.collidepoint(mousePos):
        condition = 2
      if condition == 1 and registerRect.collidepoint(mousePos):
        condition = 3
      if usernameRect.collidepoint(mousePos):                      #if username input field is clicked
        u_active = True                                             #set username active to true so red box is created around the input text field on click
        p_active = False                                            #the red box around password input field will deactivate
      elif passwordRect.collidepoint(mousePos):                    #same for password input field
        p_active = True                                             #when password input field is clicked, password red box is activated
        u_active = False                                            #username red box is deactivated
      else:
        u_active = False                                            #if neither input field is chosen, deactivate both
        p_active = False

      if condition == 2 and submitRect.collidepoint(mousePos):
        username = user_text
        password = pass_text
        user_text = ''
        pass_text = ''
        textFile = open("User Database.txt","r")
        for line in textFile:
          line = line.strip()
          lineList = line.split(",")
          if username == lineList[0] and password == lineList[1]:
            incorrectInfo = False
            score = int(lineList[2])
            condition = 4
          if username != lineList[0] and password != lineList[1]:
            incorrectInfo = True
            
      if condition == 2 and backRect.collidepoint(mousePos) or condition == 3 and backRect.collidepoint(mousePos):
        condition = 1
        user_text = ''
        pass_text = ''  

      if condition == 3 and submitRect.collidepoint(mousePos):
        username = user_text
        password = pass_text
        user_text = ''
        pass_text = ''
        textFile = open("User Database.txt","r")
        incorrectInfo = False
        for line in textFile:
          line = line.strip()
          lineList = line.split(",")
          if username != lineList[0]:
            incorrectInfo = False
          else:
            incorrectInfo = True
            break
        
        if incorrectInfo == False:
          textFile = open("User Database.txt","a")
          textFile.write("\n" + username + "," + password + "," + "0")
          textFile.close()
          condition = 4
        textFile.close()
        
      if condition == 4 and backRect.collidepoint(mousePos):
        index -= 1
        if index == 0:
          beforeIndex = 2
          afterIndex = 1
        if index == 1:
          beforeIndex = 0
          afterIndex = 2
        if index == 2:
          beforeIndex = 1
          afterIndex = 0
        if index == 3:
          index = 0
          beforeIndex = 2
          afterIndex = 1
        if index == -1:
          index = 2
          beforeIndex = 1
          afterIndex = 0
        
        
      if condition == 4 and nextRect.collidepoint(mousePos):
        index += 1
        if index == 0:
          beforeIndex = 2
          afterIndex = 1
        if index == 1:
          beforeIndex = 0
          afterIndex = 2
        if index == 2:
          beforeIndex = 1
          afterIndex = 0
        if index == 3:
          index = 0
          beforeIndex = 2
          afterIndex = 1
        if index == -1:
          index = 2
          beforeIndex = 1
          afterIndex = 0

      if condition == 4 and selectRect.collidepoint(mousePos):
        if index == 1:
          locked = False
          condition = 5
          newList = level1List
          loopList = ["5","4","3","2","1","GO"]
          addScore = 20
          speed = 0.5
          currentSpeed = 0.5
          penalty = 4
          # Set list to Beginner List
        if index == 0 and score>=500:
          locked = False
          condition = 5
          newList = level2List
          loopList = ["5","4","3","2","1","GO"]
          addScore = 40
          speed = 0.3
          currentSpeed = 0.3
          penalty = 8
          #Set list to Intermediate List
        if index == 2 and score>=1000:
          locked = False
          condition = 5
          newList = level3List
          loopList = ["5","4","3","2","1","GO"]
          addScore = 50
          speed = 0.2
          currentSpeed = 0.2
          penalty = 10

        if index == 0:
          if score < 500:
            locked = True
            required = 500
          else:
            condition = 5
            locked = False
            #Set list to Intermediate List
        if index == 2:
          if score < 1000:
            locked = True
            required = 1000
          else:
            condition = 5
            locked = False

      if condition == 4 and logoutRect.collidepoint(mousePos):
        condition = 1
        username = ''
        password = ''

      if condition == 6 and skipRect.collidepoint(mousePos):
        condition = 5
        addScore -= penalty
      
      if condition == 6 and quitRect.collidepoint(mousePos):
        condition = 4
      
      if condition == 7 and backRect.collidepoint(mousePos):
        score += addScore
        condition = 4
        lineNum = 0
        readFile = open("User Database.txt","rt")
        writeFile = open("NewFile.txt","wt")
        for line in readFile:
          line = line.strip()
          line = line.split(",")
          if line[0] != username:
            writeFile.write(line[0] + "," + line[1] + "," + line[2] + "\n")
          else:
            writeFile.write(username + "," + password + "," + str(score) + "\n")
        readFile.close()
        writeFile.close()
        shutil.copy("newfile.txt", "User Database.txt")

      
        
    loginRect = pygame.Rect(screenWidth//2 - (buttonWidth+buttonSpace), screenHeight*0.8, buttonWidth, buttonHeight)
    registerRect = pygame.Rect(screenWidth//2 + buttonSpace, screenHeight*0.8, buttonWidth, buttonHeight)
    backRect = pygame.Rect(50,50,35,screenHeight-35)
    nextRect = pygame.Rect(50,50,35,screenHeight-35)

  screenWidth,screenHeight = pygame.display.get_surface().get_size()  

  if condition == 1:
    screen.fill(WHITE)
    incorrectInfo = False
    loadImage("logo.png",300,120,screenWidth//2,screenHeight//4)
    pygame.draw.rect(screen,BLACK,loginRect,0)                        #draw login and register buttons
    pygame.draw.rect(screen,BLACK,registerRect,0)
    loadText("LOGIN",buttonFont, loginRect.centerx,loginRect.centery)
    loadText("REGISTER",buttonFont, registerRect.centerx,registerRect.centery)
    loadImage("blackpanther.jpg",125,180,(screenWidth//2)-100,loginRect.top-screenHeight//5)
    loadImage("blackpanthercover.jpg",250,200,(screenWidth//2)+85,loginRect.top-screenHeight//5)

  if condition == 2:
    usernameRect = pygame.Rect(screenWidth//2,screenHeight//3,200,32)
    passwordRect = pygame.Rect(screenWidth//2,screenHeight//2,200,32)
    submitRect = pygame.Rect((screenWidth//2)-buttonWidth//2,screenHeight//1.5,200,50)
    screen.fill(WHITE)
    titleText("LOGIN",pageTitleFont,GOLD)
    user_pass("USERNAME: ","PASSWORD: ", buttonFont,screenWidth,screenHeight)
    userVar = input(screen, usernameRect, u_color, u_base_font, user_text, color_active, color_passive, u_active)        #create input text field for username and store returned values - color and text
    u_color = userVar[0]
    passVar = input(screen, passwordRect, p_color, p_base_font, pass_text, color_active, color_passive, p_active)        #create input text field for password and store returned values - color and text
    p_color = passVar[0]
    pygame.draw.rect(screen,BLACK,submitRect,0)
    loadText("SUBMIT",buttonFont,submitRect.centerx,submitRect.centery)
    backVar = pygame.image.load("back.jpg")
    backVar = pygame.transform.scale(backVar, (75, 75))
    backRect = backVar.get_rect()
    backRect.center = (35,screenHeight-35)
    screen.blit(backVar,backRect)
    
    if incorrectInfo:
      incorrectText = buttonFont.render("Invalid Info. No Such User",True,GOLD)                                           #output error message
      incorrectRect = incorrectText.get_rect()
      incorrectRect.center = (screenWidth//2,submitRect.bottom + 30)
      screen.blit(incorrectText,incorrectRect)

  if condition == 3:
    score = 0
    usernameRect = pygame.Rect(screenWidth//2,screenHeight//3,200,32)
    passwordRect = pygame.Rect(screenWidth//2,screenHeight//2,200,32)
    submitRect = pygame.Rect((screenWidth//2)-buttonWidth//2,screenHeight//1.5,200,50)
    screen.fill(WHITE)
    titleText("REGISTER", pageTitleFont, GOLD)
    user_pass("USERNAME: ","PASSWORD: ", buttonFont,screenWidth,screenHeight)
    userVar = input(screen, usernameRect, u_color, u_base_font, user_text, color_active, color_passive, u_active)
    u_color = userVar[0]
    passVar = input(screen, passwordRect, p_color, p_base_font, pass_text, color_active, color_passive, p_active)
    p_color = passVar[0]
    pygame.draw.rect(screen,BLACK,submitRect,0)
    loadText("SUBMIT",buttonFont,submitRect.centerx,submitRect.centery)
    backVar = pygame.image.load("back.jpg")
    backVar = pygame.transform.scale(backVar, (50, 50))
    backRect = backVar.get_rect()
    backRect.center = (35,screenHeight-35)
    screen.blit(backVar,backRect)
    if incorrectInfo:
      incorrectText = buttonFont.render("Invalid. User Already Exists",True,GOLD)                                           #output error message
      incorrectRect = incorrectText.get_rect()
      incorrectRect.center = (screenWidth//2,submitRect.bottom + 30)
      screen.blit(incorrectText,incorrectRect)
 
  if condition == 4:
    screen.fill(WHITE)
    # textFile.close()
    pygame.draw.rect(screen,GOLD,(scoreRect),2)     
    loadImage("profile.jpg",30,30,scoreRect.left+25,scoreRect.top+25)
    loadText(username,buttonFont,scoreRect.centerx,scoreRect.top+25)
    loadImage("star.jpg",30,30,scoreRect.left+25,scoreRect.bottom-25)
    loadText(str(score),buttonFont,scoreRect.centerx,scoreRect.bottom-25)
    currentCharacterRect = pygame.Rect((screenWidth//2)-(currentCharacterWidth//2),(screenHeight//2)-(currentCharacterHeight//2),currentCharacterWidth,currentCharacterHeight)
    pygame.draw.rect(screen,WHITE,(currentCharacterRect),0)
    loadImage(characterList[index],currentCharacterWidth,currentCharacterHeight,currentCharacterRect.centerx,currentCharacterRect.centery)
    beforeCharacterRect = pygame.Rect((screenWidth//2)-currentCharacterWidth*1.1,(screenHeight//2)-(beforeCharacterHeight//2),beforeCharacterWidth,beforeCharacterHeight)
    pygame.draw.rect(screen,GREY,(beforeCharacterRect),2)
    loadImage(characterList[beforeIndex],beforeCharacterWidth,beforeCharacterHeight,beforeCharacterRect.centerx,beforeCharacterRect.centery)
    afterCharacterRect = pygame.Rect((screenWidth//2)+currentCharacterWidth*0.5,(screenHeight//2)-(beforeCharacterHeight//2),beforeCharacterWidth,beforeCharacterHeight)
    pygame.draw.rect(screen,GREY,(afterCharacterRect),2)
    loadImage(characterList[afterIndex],afterCharacterWidth,afterCharacterHeight,afterCharacterRect.centerx,afterCharacterRect.centery)
    nextRect = loadImage("next.png",70,70,screenWidth-35,screenHeight//2)
    backRect = loadImage("back.png",70,70,35,screenHeight//2)
    pygame.draw.rect(screen,BLACK,(selectRect),0)
    loadText("SELECT",buttonFont,selectRect.centerx,selectRect.top+25) 
    logoutVar = pygame.image.load("logout.jpg")
    logoutVar = pygame.transform.scale(logoutVar, (40, 40))
    logoutRect = logoutVar.get_rect()
    logoutRect.center = (50,screenHeight-50)
    screen.blit(logoutVar,logoutRect)
    loadText("LOGOUT",logoutFont,logoutRect.centerx,logoutRect.bottom+10)


    if locked:
      incorrectText = buttonFont.render("Locked!!! You need " + str(required) + " points to unlock",True,GOLD)                                           #output error message
      incorrectRect = incorrectText.get_rect()
      incorrectRect.center = (screenWidth//2,submitRect.bottom + 30)
      screen.blit(incorrectText,incorrectRect)

  if condition == 5:
    if newList != []:
      screen.fill(WHITE)
      currentExcersize = random.choice(newList)
      newList.remove(currentExcersize)
      for item in loopList:
        mousePos = pygame.mouse.get_pos()
        screen.fill(WHITE)
        loadText(currentExcersize[0],pageTitleFont,screenWidth//2,100)
        loadText(item,countFont,screenWidth//2,screenHeight//2)
        pygame.display.update()
        time.sleep(1)
      condition = 6
      check = True
      distance = 100
    else: 
      condition = 7

  if condition == 6:
    sizex = 400
    sizey = 400
    if check:
      screen.fill(WHITE)
      check = False
    startRect = pygame.Rect(100,screenHeight-50,10,25)
    endRect = pygame.Rect(screenWidth-100,screenHeight-50,10,25)
    moveRect = pygame.Rect(distance,screenHeight-50,10,10)
    mousePos = pygame.mouse.get_pos()
    pygame.draw.rect(screen,BLACK,(helpRect),0)
    loadText(currentExcersize[0],pageTitleFont,screenWidth//2,50)
    loadText("?",pageTitleFont,helpRect.centerx,helpRect.centery)
    if helpRect.collidepoint(mousePos):
      url = currentExcersize[1]
      speed = 0
    else:
      url = currentExcersize[2]
      speed = currentSpeed
    loadImage(url,sizex,sizey,screenWidth//2,screenHeight//2)
    pygame.draw.rect(screen,BLACK,(startRect),0)
    pygame.draw.rect(screen,BLACK,(endRect),0)
    pygame.draw.rect(screen,GOLD,(moveRect),0)
    distance += speed
    pygame.draw.rect(screen,BLACK,(skipRect),0)
    loadText("SKIP",buttonFont,skipRect.centerx,skipRect.centery)
    pygame.draw.rect(screen,BLACK,(quitRect),0)
    loadText("QUIT",buttonFont,quitRect.centerx,quitRect.centery)
    if moveRect.right >= endRect.left:
      speed = 0
      condition = 5
      
  if condition == 7:
    screen.fill(WHITE)
    loadText("Complete!!!",countFont,screenWidth//2,screenHeight//2)
    loadText("Don't Forget to Join Back Tomorrow",buttonFont,screenWidth//2,screenHeight//2+100)
    backVar = pygame.image.load("back.jpg")
    backVar = pygame.transform.scale(backVar, (75, 75))
    backRect = backVar.get_rect()
    backRect.center = (35,screenHeight-35)
    screen.blit(backVar,backRect)





    
    
  
  
    




    

    
    
    
  pygame.display.update()
pygame.quit()
sys.exit()