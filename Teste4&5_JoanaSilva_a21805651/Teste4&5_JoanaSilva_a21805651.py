import pygame, turtle, math, random, winsound
from random import randint, choice

pygame.init()

pygame.display.set_caption("TheMazeRun")

wn = turtle.Screen()
wn.setup(700,700)
wn.title("The Maze Game")
wn.bgcolor("black")
wn.tracer(0)

#winsound.PlaySound('99188__guiton__dark01.wav', winsound.SND_FILENAME)

#RegisterShape
images = [
"SansDown.gif",
"SansDown1.gif",
"SansLeft.gif",
"SansLeft1.gif",
"SansRight.gif",
"SansRight1.gif",
"SansUp.gif",
"SansUp1.gif",
"wall.gif",
"EnemyRight.gif",
"EnemyLeft.gif",
"coins.gif"
]

for image in images:
    turtle.register_shape(image)

#create pen
class Pen(turtle.Turtle):
  def __init__(self):
    turtle.Turtle.__init__(self)
    self.shape("square")
    self.color("white")
    self.penup()
    self.speed(0)
    
class Player(turtle.Turtle):
  def __init__(self):
    turtle.Turtle.__init__(self)
    self.shape("SansDown1.gif")
    self.color("blue")
    self.penup()
    self.speed(0)
    self.gold = 0

 
  def go_up(self):
    move_to_x = self.xcor()
    move_to_y = self.ycor() + 24
    self.shape("SansUp.gif")
    
    if (move_to_x,move_to_y) not in walls:
        self.goto(move_to_x, move_to_y)
  
  def go_down(self):
    move_to_x = self.xcor()
    move_to_y = self.ycor() - 24
    self.shape("SansDown.gif")
    
    if (move_to_x,move_to_y) not in walls:
        self.goto(move_to_x, move_to_y)  
        
  def go_right(self):
    move_to_y = self.ycor()
    move_to_x = self.xcor() + 24
    self.shape("SansRight.gif")
    
    if (move_to_x, move_to_y) not in walls:
        self.goto(move_to_x, move_to_y) 
        
  def go_left(self):
    move_to_y = self.ycor()
    move_to_x = self.xcor() - 24
    self.shape("SansLeft.gif")
    
    if (move_to_x,move_to_y) not in walls:
        self.goto(move_to_x, move_to_y)

  def is_collision(self, other):
      a = self.xcor()-other.xcor()
      b = self.ycor()-other.ycor()
      distance = math.sqrt((a ** 2) + (b ** 2))

      if distance < 5:
          return True
      else:
          return False

class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("coins.gif")
        self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(200,200)
        self.hideturtle()

class Enemy(turtle.Turtle):
  def __init__(self, x, y):
    turtle.Turtle.__init__(self)
    self.shape("EnemyLeft.gif")
    self.color("red")
    self.penup()
    self.speed(0)
    self.gold = 25
    self.goto(x, y)
    self.direction = random.choice(["up", "down", "left", "right"])

  def move(self):
    if self.direction == "up":
      dx = 0
      dy = 24
    elif self.direction == "down":
      dx = 0
      dy = -24
    elif self.direction == "left":
      dx = -24
      dy = 0
      self.shape("EnemyLeft.gif")
    elif self.direction == "right":
      dx = 24
      dy = 0
      self.shape("EnemyRight.gif")
    else:
      dx = 0
      dy = 0

    if self.is_close(player):
      if player.xcor() < self.xcor():
        self.direction = "left"
      elif player.xcor() > self.xcor():
        self.direction = "right"
      elif player.ycor() < self.ycor():
        self.direction = "down"
      elif player.ycor() > self.ycor():
        self.direction = "up"

    move_to_x = self.xcor() + dx
    move_to_y = self.ycor() + dy

    if (move_to_x, move_to_y) not in walls:
       self.goto(move_to_x, move_to_y)
    else:
        self.direction = random.choice(["up", "down", "left", "right"])

    turtle.ontimer(self.move, t=random.randint(100, 300))

  def is_close(self, other):
    a = self.xcor()-other.xcor()
    b = self.ycor()-other.ycor()
    distance = math.sqrt((a ** 2) + (b ** 2))

    if distance < 75:
      return True
    else:
      return False
      
  def destroy(self):
    self.goto(2000, 2000)
    self.hideturtle()
                               

#create Levels list
levels = [""]

#define first level
level_1 = [
"XXXXXXXXXXXXXXXXXXXXXXXXX",
"XP  XXXXXXE            XX",
"X  XXXXXXX  XXXXXX  XX XX",
"X       XX  XXXXXX  X XXX",
"X       XX  XXX        XX",
"XXXXXX  XX  XXXT       XX",
"XXXXXX  XX  XXXXXX  XXXXX",
"XXXXXX  XX    XXXX  XXXXX",
"X TXXX        XXXX  XXXXX",
"X  XXX   XXXXXXXXXXXXXX",
"X                XXXXXXXX",
"XXXXXXXXXXXX     XXXXX TX",
"XXXXXXXXXXXXXXX  XXXXX  X",
"XXX TXXXXXXXXXX         X",
"XXE                     X",
"XXX         XXXXXXXXXXXXX",
"XXXXXXXXXX  XXXXXXXXXXXXX",
"XXXXXXXXXX              X",
"XXT  XXXXX              X",
"XX   XXXXXXXXXXXXX  XXXXX",
"XXE   YXXXXXXXXXXX  XXXXX",
"XX          XXXX        X",
"XXXX                   TX",
"XXXXXXXXXXXXXXXXXXXXXXXXX"
]

#Gold
treasures = []
enemies = []
exits = []

#Add maze to mazes list
levels.append(level_1)

#Create Level Setup Function

def setup_maze(level):
  for y in range(len(level)):
    for x in range(len(level[y])):
      character = level[y][x]
      screen_x = -288 + (x * 24)
      screen_y = 288 - (y * 24)
      
      if character == "X":
        pen.goto(screen_x, screen_y)
        pen.shape("wall.gif")
        pen.stamp()
        walls.append((screen_x,screen_y))
        
      if character == "P":
        player.goto(screen_x, screen_y)

      if character == "T":
        treasures.append(Treasure(screen_x, screen_y))

      if character == "E":
        enemies.append(Enemy(screen_x, screen_y))

      if character == "O":
        if player.gold == 600:
          eexits.append(Exit(screen_x, screen_y))
          print("Congrats you WON")
        
#Create class instances
pen = Pen()
player = Player()

# Walls
walls = []
print(walls)

#Level Setup
setup_maze(levels[1])
print(walls)


#Keyboard
turtle.listen()
turtle.onkey(player.go_left,"Left")
turtle.onkey(player.go_right,"Right")
turtle.onkey(player.go_up,"Up")
turtle.onkey(player.go_down,"Down")


#Screen Updates = OFF
wn.tracer(0)

for enemy in enemies:
  turtle.ontimer(enemy.move, t = 250)


#Main Game Loop
while True:
    for treasure in treasures:
        if player.is_collision(treasure):
            player.gold += treasure.gold
            print("Player Gold: {}".format(player.gold))
            treasure.destroy()
            treasures.remove(treasure)

    for enemy in enemies:
      if player.is_collision(enemy):
        print("Player died!!")
        quit()
      
  
    wn.update()




