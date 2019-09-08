#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 08:59:30 2018

@author: jakobvalen
"""
import turtle 
import os  
import math  
import random


#Create Main Screen 
MainScreen=turtle.Screen() 
MainScreen.bgcolor("black") 
MainScreen.title("Jakob's Alien Shooter Game")   
MainScreen.bgpic("space2.gif") #Add a space background

#Create the border where the game will take place
border_pen = turtle.Turtle() 
border_pen.speed(0) 
border_pen.color("white") 
border_pen.penup() 
border_pen.setposition(-300,-300)  
border_pen.pendown()
border_pen.pensize(3)   

for side in range(4): 
    border_pen.fd(600) 
    border_pen.lt(90)  
border_pen.hideturtle()   

# Initilaze the score
score=0  
game_on=True #set to true when game is playing

score_pen = turtle.Turtle()   
score_pen.speed(0) 
score_pen.color("white") 
score_pen.penup() 
score_pen.setposition(-290,280) 
scorestring="Score:%s"%score 
score_pen.write(scorestring,False)
score_pen.hideturtle() 
# Import the invader and player shapes for game
turtle.register_shape("player.gif") 
turtle.register_shape("invader.gif")





#Create the player
ship=turtle.Turtle() 
ship.color("red")
ship.shape("player.gif") 
ship.penup() 
ship.speed(0)
ship.setposition(0,-250) #Set position to middle of screen
ship.setheading(90) #Make the ship face upward
shipspeed=15

num_of_aliens = 9 # The number of space invaders

aliens=[]  # The list that stores all space invaders

for i in range(num_of_aliens): 
    aliens.append(turtle.Turtle()) 
# Create the space invaders
for alien in aliens: 
    alien.color("green") 
    alien.shape("invader.gif")  
    alien.setheading(270)
    alien.penup()
    alien.speed(0)  
    x=random.randint(-200,200) 
    y=random.randint(100,250)
    alien.setposition(x,y)  
    
alienspeed=2  # All aliens will have the same speed 

 
#Create the lasers for our player to defend themselves
laser=turtle.Turtle() 
laser.color("yellow")  
laser.shape("circle") 
laser.penup()  
laser.speed(0) 
laser.shapesize(0.5,0.5) 
laser.hideturtle() 
laserspeed=40

#ready- laser is ready to fire 
#fire- laser is firing 
laserstate = "ready" 

#Move the player left, stop at the left border
def move_left(): 
    x = ship.xcor() 
    x-=shipspeed  
    if x< -280: 
        x=-280
    ship.setx(x) 
#Move the player right, stop at the right border
def move_right(): 
    x = ship.xcor() 
    x+=shipspeed  
    if x>280: 
        x=280
    ship.setx(x) 
#Check if player is ready to fire than fire
def fire_laser(): 
    global laserstate 
    if laserstate=="ready":  
        os.system("afplay laser.wav&")# Make a lser sound effect
        laserstate="fire" 
        x=ship.xcor() 
        y=ship.ycor()+10 
        laser.setposition(x,y) #Sets the position of the laser relative to the player
        laser.showturtle() 
#Using pythagerous therom check to see if a collision between two objects has occured
def isHit(o1,o2): 
    dist=math.sqrt(math.pow(o1.xcor()-o2.xcor(),2)+math.pow(o1.ycor()-o2.ycor(),2))
    if dist<25: # If the value of distance is less than 15 we will consider that a hit
        return True 
    else: 
        return False 

#The key listener for our game
turtle.listen() 
turtle.onkey(move_left, "Left") # Move left if left button pressed 
turtle.onkey(move_right, "Right") #Move right if right button pressed
turtle.onkey(fire_laser, "space") #Fire if space-bar pressed

#This is the main game loop which runs until our player collides with an invader 
# or an invader passes our player
while game_on:  
    #Move all the space invaders 
    for alien in aliens:
        x=alien.xcor()
        x+=alienspeed 
        alien.setx(x) 
        #If one invader hits the right border, shift all invaders down and move left
        if alien.xcor()>280:  
            for a in aliens:
                y=a.ycor() 
                y-=40
                a.sety(y) 
            alienspeed*=-1 #Move left (opposite direction)
            
        #If one invader hits the left border, shift all invaders down and move right
        if alien.xcor()<-280:  
            for a in aliens:
                y=a.ycor() 
                y-=40
                a.sety(y)  
            alienspeed*=-1 #Move right (opposite direction) 
            
        #If an invader has passed our player, end the game
        if alien.ycor()<-250 : 
            MainScreen.bgpic("gameover.gif")
            print("GAME OVER") 
            game_on=False
         # Check to see if a laser has hit an invader then move invader to 
         # a random spot near the top of the screen
        if isHit(laser,alien):  
            os.system("afplay explosion.wav&") #Make an explosion sound effect
            laser.hideturtle #Hide laser then reset position
            laserstate="ready" 
            laser.setposition(0,-400)
            x=random.randint(-200,200) 
            y=random.randint(100,250)
            alien.setposition(x,y)  
            score+=10 #Update the score, each invader hit is 10 points
            scorestring="Score:%s"%score  
            score_pen.clear()
            score_pen.write(scorestring,False)
        #Check if an invader has hit the ship, if so end game   
        if isHit(alien,ship):  
            os.system("afplay explosion.wav&") #Make an explosion sound effect
            ship.hideturtle() 
            MainScreen.bgpic("gameover.gif")#Display game over background  
            print("GAME OVER") 
            game_on=False
    
     # While player is firing move laser      
    if laserstate=="fire": 
        y=laser.ycor() 
        y+=laserspeed 
        laser.sety(y)
    #Once laser is out of bounds hide the laser
    if laser.ycor()>275:  
        laser.hideturtle() 
        laserstate="ready" 
        

delay = raw_input("Press enter to finish")