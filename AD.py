#For this code I have referenced Mr.Bohn (full name Matt Bohn) Udemy class from which I have recycled code.
#I have consulted chatgpt for some parts of the code. I will adress when I have in my comments same for Mr.Bohn
#There are other files (just gifs) that are needed for this progarm to work as intened. But from my understanding I can only send this pdf file, so I will not be sending those gif files.

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
        playsound("laser.wav", False)  #Chatgpt was used for the playsound code. The space key triggers the bullet to be fired and the laser sound to be played


turtle.listen()
turtle.onkey(left, "Left")  #sets the function left to the left arrow button on the computer
turtle.onkey(right, "Right") #sets the function right to the right arrow button on the computer
turtle.onkey(space, "space") #sets the function space to the space button on the computer
    


#Enemies set up, this has been taken for Mr. Bohn's class
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
def setup_game(): 
    global win, spaceship, bullet, enemies, explosionCounters, moveShipBy, points, lives, enemiesRemaining, scoreTurtle, livesTurtle, stealthEnemy, stealthCounter, stealthVisible, bossEnemy, bossHealth, bossCounter, bossVisible #This make all these varibles, global
    moveShipBy = 0 #sets the monmentum
    
    
    #Screen set up
    win = turtle.Screen() #Makes the window
    win.title("Alien Defender") #Gives the name of the window 
    win.setup(width=1.0, height=1.0) #Sets the dimentions of the window
    win.bgpic("space-bg.gif") #Changs the backgound of the window
    win.tracer(0) #Disables the screen updates


    # Sprites set up
    turtle.register_shape("ship.gif") #register the file ship to turtle
    turtle.register_shape("bullet.gif") #register the file bullet to turtle
    turtle.register_shape("explosion.gif") #register the file explosion to turtle
    turtle.register_shape("enemy.gif") #register the file enemy to turtle
    turtle.register_shape("stealth.gif") #register the file stealth to turtle
    turtle.register_shape("boss.gif") #register the file boss to turtle
    
    #Spaceship set up
    spaceship = turtle.Turtle() #makes a turtle called spaceship
    spaceship.shape("ship.gif") #gives the design for spaceship
    spaceship.penup() #makes it so that spaceship can not draw
    spaceship.speed(0) #set the reaction speed of spaceship
    spaceship.goto(0, -200) #move it to the staring postion

    #Bullet set up
    bullet = turtle.Turtle() #makes a turtle called bullet
    bullet.hideturtle() #makes bullet nonvisable for now
    bullet.shape("bullet.gif") #gives the design for bullet
    bullet.penup() #makes it so that bullet can not draw



    #Enemies set up
    enemies = getEnemies() #gets a list of enemies
    explosionCounters = getExplosionCounterList(len(enemies)) #This makes a list to track explosion timing for each enemy.

    enemiesRemaining = len(enemies) #sets the amount of enemies to the amount in the list
    
    #code for enemy slealth
    stealthEnemy = turtle.Turtle() #makes a turtle called stealth
    stealthEnemy.hideturtle() #makes stealth nonvisable for now
    stealthEnemy.shape("stealth.gif") #gives the design for stealth
    stealthEnemy.penup() #makes it so that stealth can not draw
    stealthEnemy.goto(random.randint(-300, 300), 800) #sets the postion of stealth
    stealthCounter = 0 #sets the stealth counter to 0 for now. stealth counter gives the amount of stealth enemies that can spwan
    stealthVisible = True #makes stealth visable now

    #code for enemy boss
    bossEnemy = turtle.Turtle() #makes a turtle called boss
    bossEnemy.hideturtle() #makes boss nonvisable for now
    bossEnemy.shape("boss.gif") #gives the design for boss
    bossEnemy.penup() #makes it so that boss can not draw
    bossEnemy.goto(random.randint(-300, 300), 1000) #sets the postion of boss
    bossHealth = 2 #the boss takes two hits to kill
    bossCounter = 0 #sets the boss counter to 0 for now. boss counter gives the amount of boss enemies that can spwan
    bossVisible = True #makes the boss visable


    
    #Score set up, this was taken from Mr.Bohn's class
    points = 0 #sets the points to zero at the start
    scoreTurtle = turtle.Turtle() #makes a turtle called scoreTurtle (socre for short)
    scoreTurtle.hideturtle() #makes score nonvisable
    scoreTurtle.penup() #makes it so that score can not draw
    scoreTurtle.pencolor("yellow") #sets the color of score
    screen_width = win.window_width() #gets the width from the window
    screen_height = win.window_height() #gets the height form the window
    scoreTurtle.goto(screen_width // 2 - 150, screen_height // 2 - 50) #sets the postion of score
    scoreTurtle.write(f"Score: {points}", align="right", font=("Arial", 25, "bold")) #sets the font and desgin of points and updates score depending on points


    #Lives set up
    lives = 3 #sets the lives to 3 at the start
    livesTurtle = turtle.Turtle() #makes a turtle called livesTurtle (lives for short)
    livesTurtle.hideturtle() #makes lives nonvisable
    livesTurtle.penup() #makes it so that lives can not draw
    livesTurtle.pencolor("red") #sets the color of lives
    livesTurtle.goto(-screen_width // 2 + 150, screen_height // 2 - 50) #sets the postion of lives
    livesTurtle.write(f"Lives: {lives}", align="left", font=("Arial", 25, "bold")) #updates the lives depending on the amount of lives


#The main game play of the game
def main_game(): 
    global moveShipBy, points, lives, enemiesRemaining, stealthCounter, stealthVisible, bossCounter, bossVisible, bossHealth #This make all these varibles, global

    while enemiesRemaining > 0 and lives > 0: #keeps the game going on unless there are no more lives or enemies
        spaceship.forward(moveShipBy)

        if bullet.isvisible(): #makes the bullet turtle visable
            bullet.setheading(90) #sets the heading of bullet 
            bullet.forward(25) #moves the bullet 25 pixels each loop

        if bullet.ycor() > (win.window_height() / 2): #checks the location of bullet
            bullet.hideturtle() #if bullet has gone off screen it is hidden

        if spaceship.xcor() > 325 or spaceship.xcor() < -325: #checks the location of spaceship 
            moveShipBy = 0 #if spaceship is trying to leave the borders of the screen it is stoped

        
#ENEMIES:
        enemyIndex = 0 #counts the amount of enemies that have spwaned
        enemiesRemaining = 0 #Resets the counter for how many enemies are alives 
        for enemy in enemies:
            
            
            #Enemy 1: Code for the normal enemy (the pink ufo). 
            if enemy.ycor() > -350: #if the enemy has not gone off the screen yet
                enemy.setheading(270) #set the heading
                enemy.forward(3) #moves 3 pixels every loop
                enemiesRemaining += 1 #adding one to enemiesRemaining

            if (pixelsBetween(enemy.xcor(), bullet.xcor()) < 35 and
                    pixelsBetween(enemy.ycor(), bullet.ycor()) < 35 and
                    bullet.isvisible() and enemy.isvisible()): #detectes a collsion between a bullet and enemy
                enemy.shape("explosion.gif") #changes the desgin of the enemy to explosion.gif
                bullet.hideturtle() #hides bullet
                playsound("explosion.wav", False) #chatgpt did write the code for playsound. I was not able to understand playsound. Plays an expolsion sound
                explosionCounters[enemyIndex] = 1 #starts the explosion counter
                points += 1000 #adds 1000 points
                scoreTurtle.clear() #clears score
                scoreTurtle.write(f"Score: {points}", align="right", font=("Arial", 25, "bold")) #updates score

            if enemy.ycor() < -250 and enemy.isvisible(): #if you dont shoot the enemy
                enemy.hideturtle() #hides the enemy
                explosionCounters[enemyIndex] = 6 #justs destroys the enemy
                lives -= 1 #removes one life
                livesTurtle.clear() #clears lives
                livesTurtle.write(f"Lives: {lives}", align="left", font=("Arial", 25, "bold")) #updates lives
                if lives <= 0: #if lives reachs 0 it's game over
                    enemiesRemaining = 0
                    break

            if explosionCounters[enemyIndex] >= 1: #after 5 loops the enemy will dispear
                explosionCounters[enemyIndex] += 1
            if explosionCounters[enemyIndex] > 5:
                enemy.hideturtle()
            enemyIndex += 1 #updates enemy index
        
        
        
        #Enemy 2: Code for the sleath ufo (the balck ufo)
        if stealthEnemy.isvisible(): #makes stealth visable
            stealthEnemy.setheading(270) #sets the heading 
            stealthEnemy.forward(5) #moves 5 pixels every loop

            if (pixelsBetween(stealthEnemy.xcor(), bullet.xcor()) < 35 and
                pixelsBetween(stealthEnemy.ycor(), bullet.ycor()) < 35 and
                bullet.isvisible()): #detectes a collsion between a bullet and stealth
                stealthEnemy.shape("explosion.gif") #changes the desgin of the stealth to explosion.gif
                bullet.hideturtle() #hides bullet
                playsound("explosion.wav", False) #chatgpt did write the code for playsound. I was not able to understand playsound. Plays an expolsion sound
                stealthCounter = 1 #starts the explosion counter
                points += 2500 #adds 2500 points
                scoreTurtle.clear() #clears score
                scoreTurtle.write(f"Score: {points}", align="right", font=("Arial", 25, "bold")) #updates score

            if stealthCounter >= 1:
                stealthCounter += 1
            if stealthCounter > 5:
                stealthEnemy.hideturtle()
                stealthVisible = False #after 5 stealths have spwaned no more will

        if not stealthEnemy.isvisible() and stealthVisible: #if stealth is nonvisable
            if random.randint(1, 100) == 1: #has a 1/100 of spwaning 
                stealthEnemy.shape("stealth.gif") #sets the desgin 
                stealthEnemy.goto(random.randint(-300, 300), 800) #sets the postion
                stealthEnemy.showturtle() #makes stealth visable
                stealthCounter = 0 #Resets the stealth counter
       
        
        
        # Enemy 3: Code for the bose (the yellow ufo)
        if bossEnemy.isvisible(): #makes boss visable
            bossEnemy.setheading(270) #sets the heading
            bossEnemy.forward(1.5) #moves 1.5 pixels every loop

            if (pixelsBetween(bossEnemy.xcor(), bullet.xcor()) < 40 and
                pixelsBetween(bossEnemy.ycor(), bullet.ycor()) < 40 and
                bullet.isvisible()): #detectes a collsion between a bullet and boss
                bossHealth -= 1 #lowers the boss health
                bullet.hideturtle() #hides bullet
                playsound("explosion.wav", False) #chatgpt did write the code for playsound. I was not able to understand playsound. Plays an expolsion sound

                if bossHealth <= 0: #if the boss is shot twice 
                    bossEnemy.shape("explosion.gif") #change the desgin to explosion.gif
                    bossCounter = 1 #updates the boss counter
                    points += 3500 #adds 3500 points
                    scoreTurtle.clear() #clears turtle
                    scoreTurtle.write(f"Score: {points}", align="right", font=("Arial", 25, "bold")) #updates score

        if bossCounter >= 1:
            bossCounter += 1
        if bossCounter > 5:
            bossEnemy.hideturtle()
            bossVisible = False #after 5 bosses have spwaned no more will

        if not bossEnemy.isvisible() and bossVisible: #if boss is nonvisable
            if random.randint(1, 200) == 1: #1/200 chnage of spwaning 
                bossEnemy.shape("boss.gif") #sets the desgin
                bossEnemy.goto(random.randint(-300, 300), 1000) #sets postion
                bossEnemy.showturtle() #makes the boss visable
                bossHealth = 2 #resets the health
                bossCounter = 0 #resest the counter

        win.update() #refreshes the window
        time.sleep(0.02) #gives some needed delay


#Try again 
def try_again():
    answer = turtle.textinput("Game Over", "Try again? (y/n)") #asked the user if they want to try again
    if answer and answer.lower() == "y": #if y starts the game again
        win.bye()
        os.execl(sys.executable, sys.executable, *sys.argv) #I had to ask chatgpt for this code
    else: #if not y ends the game
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
if lives <= 0:#if lives reach 0 
    scoreTurtle.write("YOU LOST ALL LIVES!", align="center", font=("Arial", 50, "bold"))
else:#if game is beat 
    scoreTurtle.write("GAME OVER", align="center", font=("Arial", 50, "bold"))

time.sleep(2) #pauses the game for 2 seconds
try_again() #asks the user if they want to try again
