#For this code I have referenced Mr.Bohn (full name Matt Bohn) Udemy class from which I have recycled code.
#From Mr.Bohn class I have used his images and audio files.
#I have consulted chatgpt for some parts of the code. I will adress when I have in my comments same for Mr.Bohn

#imports
import turtle
import time
import random
import sys
import os
from playsound import playsound

#Arrow key commands

def left():
    global moveShipBy
    moveShipBy = -5   #when the left arrow is pressed the ship moves left 5 on the screen

def right():
    global moveShipBy
    moveShipBy = 5    #when the right arrow is pressed the ship moves righ 5 on the screen

def space():
    global bullet
    global spaceship
    if not bullet.isvisible():
        bullet.goto(spaceship.xcor(), spaceship.ycor() + 45)
        bullet.showturtle()
        playsound("laser.wav", False)  #The space key triggers the bullet to be fired and the laser sound to be played


turtle.listen()
turtle.onkey(left, "Left")  #sets the function left to the left arrow button on the computer
turtle.onkey(right, "Right") #sets the function right to the right arrow button on the computer
turtle.onkey(space, "space") #sets the function space to the space button on the computer
    


#Enemies set up this has been taken for Mr. Bohn's class
def getEnemies():
    enemies = []
    for x in range(1, 6): #This gets five enemies and places them randomly
        e = turtle.Turtle()
        e.hideturtle()
        e.shape("enemy.gif")
        e.penup()
        e.goto(random.randint(-350, 350), int(800 * x))
        e.showturtle()
        enemies.append(e)
    return enemies

def pixelsBetween(value1, value2): #This checks how close two objects are to each other 
    return abs(value1 - value2)

def getExplosionCounterList(enemyCount): #This makes a list to track explosion timing for each enemy.
    return [0 for _ in range(enemyCount)]


#ThE Game set up
def setup_game(): #
    global win, spaceship, bullet, enemies, explosionCounters, moveShipBy, points, lives, enemiesRemaining, scoreTurtle, livesTurtle, stealthEnemy, stealthCounter, stealthVisible, bossEnemy, bossHealth, bossCounter, bossVisible
    
    
    
    #Screen set up
    win = turtle.Screen()
    win.title("Alien Defender")
    win.setup(width=1.0, height=1.0)
    win.bgpic("space-bg.gif")
    win.tracer(0)


    # Sprites set up
    turtle.register_shape("ship.gif")
    turtle.register_shape("bullet.gif")
    turtle.register_shape("enemy.gif")
    turtle.register_shape("explosion.gif")
    turtle.register_shape("stealth.gif")
    turtle.register_shape("boss.gif")

    spaceship = turtle.Turtle()
    spaceship.shape("ship.gif")
    spaceship.penup()
    spaceship.speed(0)
    spaceship.goto(0, -200)

    bullet = turtle.Turtle()
    bullet.hideturtle()
    bullet.shape("bullet.gif")
    bullet.penup()



    #Enemies set up
    enemies = getEnemies()
    explosionCounters = getExplosionCounterList(len(enemies))

    moveShipBy = 0
    points = 0
    lives = 3
    enemiesRemaining = len(enemies)
    
    stealthEnemy = turtle.Turtle()
    stealthEnemy.hideturtle()
    stealthEnemy.shape("stealth.gif")
    stealthEnemy.penup()
    stealthEnemy.goto(random.randint(-300, 300), 800)
    stealthCounter = 0
    stealthVisible = True

    bossEnemy = turtle.Turtle()
    bossEnemy.hideturtle()
    bossEnemy.shape("boss.gif")
    bossEnemy.penup()
    bossEnemy.goto(random.randint(-300, 300), 1000)
    bossHealth = 2
    bossCounter = 0
    bossVisible = True


    
    #Score set up
    scoreTurtle = turtle.Turtle()
    scoreTurtle.hideturtle()
    scoreTurtle.penup()
    scoreTurtle.pencolor("yellow")
    screen_width = win.window_width()
    screen_height = win.window_height()
    scoreTurtle.goto(screen_width // 2 - 150, screen_height // 2 - 50)
    scoreTurtle.write(f"Score: {points}", align="right", font=("Arial", 25, "bold"))


    #Lives set up
    livesTurtle = turtle.Turtle()
    livesTurtle.hideturtle()
    livesTurtle.penup()
    livesTurtle.pencolor("red")
    livesTurtle.goto(-screen_width // 2 + 150, screen_height // 2 - 50)
    livesTurtle.write(f"Lives: {lives}", align="left", font=("Arial", 25, "bold"))



def main_game():
    global moveShipBy, points, lives, enemiesRemaining
    global stealthCounter, stealthVisible, bossCounter, bossVisible, bossHealth

    while enemiesRemaining > 0 and lives > 0:
        spaceship.forward(moveShipBy)

        if bullet.isvisible():
            bullet.setheading(90)
            bullet.forward(25)

        if bullet.ycor() > (win.window_height() / 2):
            bullet.hideturtle()

        if spaceship.xcor() > 325 or spaceship.xcor() < -325:
            moveShipBy = 0

        
#ENEMIES:
        enemyIndex = 0
        enemiesRemaining = 0
        for enemy in enemies:
            
            
            #Enemy 1: Code for the normal enemy (the pink ufo)
            if enemy.ycor() > -350:
                enemy.setheading(270)
                enemy.forward(3)
                enemiesRemaining += 1

            if (pixelsBetween(enemy.xcor(), bullet.xcor()) < 35 and
                    pixelsBetween(enemy.ycor(), bullet.ycor()) < 35 and
                    bullet.isvisible() and enemy.isvisible()):
                enemy.shape("explosion.gif")
                bullet.hideturtle()
                playsound("explosion.wav", False)
                explosionCounters[enemyIndex] = 1
                points += 1000
                scoreTurtle.clear()
                scoreTurtle.write(f"Score: {points}", align="right", font=("Arial", 25, "bold"))

            if enemy.ycor() < -250 and enemy.isvisible():
                enemy.hideturtle()
                explosionCounters[enemyIndex] = 6
                lives -= 1
                livesTurtle.clear()
                livesTurtle.write(f"Lives: {lives}", align="left", font=("Arial", 25, "bold"))
                if lives <= 0:
                    enemiesRemaining = 0
                    break

            if explosionCounters[enemyIndex] >= 1:
                explosionCounters[enemyIndex] += 1
            if explosionCounters[enemyIndex] > 5:
                enemy.hideturtle()
            enemyIndex += 1
        
        
        
        #Enemy 2: Code for the sleath ufo (the balck ufo)
        if stealthEnemy.isvisible():
            stealthEnemy.setheading(270)
            stealthEnemy.forward(5)

            if (pixelsBetween(stealthEnemy.xcor(), bullet.xcor()) < 35 and
                pixelsBetween(stealthEnemy.ycor(), bullet.ycor()) < 35 and
                bullet.isvisible()):
                stealthEnemy.shape("explosion.gif")
                bullet.hideturtle()
                playsound("explosion.wav", False)
                stealthCounter = 1
                points += 3000
                scoreTurtle.clear()
                scoreTurtle.write(f"Score: {points}", align="right", font=("Arial", 25, "bold"))

            if stealthCounter >= 1:
                stealthCounter += 1
            if stealthCounter > 5:
                stealthEnemy.hideturtle()
                stealthVisible = False

        if not stealthEnemy.isvisible() and stealthVisible:
            if random.randint(1, 100) == 1:
                stealthEnemy.shape("stealth.gif")
                stealthEnemy.goto(random.randint(-300, 300), 800)
                stealthEnemy.showturtle()
                stealthCounter = 0
        
        
        
        # Enemy 3: Code for the bose (the yellow ufo)
        if bossEnemy.isvisible():
            bossEnemy.setheading(270)
            bossEnemy.forward(1.5)

            if (pixelsBetween(bossEnemy.xcor(), bullet.xcor()) < 40 and
                pixelsBetween(bossEnemy.ycor(), bullet.ycor()) < 40 and
                bullet.isvisible()):
                bossHealth -= 1
                bullet.hideturtle()
                playsound("explosion.wav", False)

                if bossHealth <= 0:
                    bossEnemy.shape("explosion.gif")
                    bossCounter = 1
                    points += 3500
                    scoreTurtle.clear()
                    scoreTurtle.write(f"Score: {points}", align="right", font=("Arial", 25, "bold"))

        if bossCounter >= 1:
            bossCounter += 1
        if bossCounter > 5:
            bossEnemy.hideturtle()
            bossVisible = False

        if not bossEnemy.isvisible() and bossVisible:
            if random.randint(1, 200) == 1:
                bossEnemy.shape("boss.gif")
                bossEnemy.goto(random.randint(-300, 300), 1000)
                bossEnemy.showturtle()
                bossHealth = 2
                bossCounter = 0

        win.update()
        time.sleep(0.02)


#Retrying fuction
def try_again():
    answer = turtle.textinput("Game Over", "Try again? (y/n)")
    if answer and answer.lower() == "y":
        win.bye()
        os.execl(sys.executable, sys.executable, *sys.argv)
    else:
        scoreTurtle.clear()
        scoreTurtle.goto(0, 0)
        scoreTurtle.color("white")
        scoreTurtle.write("Thanks for playing!", align="center", font=("Arial", 40, "bold"))
        time.sleep(2)
        win.bye()



# STARTING THE GAME
setup_game()
main_game()



# Game over message
scoreTurtle.goto(0, 0)
if lives <= 0:
    scoreTurtle.write("YOU LOST ALL LIVES!", align="center", font=("Arial", 50, "bold"))
else:
    scoreTurtle.write("GAME OVER", align="center", font=("Arial", 50, "bold"))

time.sleep(2)
try_again()
