import sys, random, math, pygame
from pygame.locals import *
from math import sqrt, cos, sin, atan2, pi
from time import sleep
import playGround
import weasel
import rules
import turtle
import random

#There is a distinction between what a robot and what a turtle is. A turtle is an object that gets drawn to the screen while the robot is an object that has all of the properties that
#we will care about (xlocation, ylocation, velocity, etc.).
class Simulator:
    rules = None
    robots = []
    turtles = []
    playPlace = None
    usedRobotColors = [] #This is used to keep track of the colors that the robots have so that way no 2 robots have the same color. Uses tuples of (R,G,B)
    gameTicks = 0
    window = None

    def __init__(self):
        self.rules = rules.Rules()
        self.playPlace = playGround.PlayGround(self.rules)
        self.window = turtle.Screen()
        turtle.setworldcoordinates(0,0,self.playPlace.xbound, self.playPlace.ybound)
        self.window.colormode(255)

    def incrementGameTicks(self):
        self.gameTicks += 1

    #This function is called by the handler turtle.onclick for when a click has happened on the screen.
    #The handler calls this function with the coordinates of where the click was, this function will add a robot object to the game.
    #This function will get the velocity and orientation from the user.
    #TODO implement this
    def addRobotClick(self,x,y):
        pass

    #This function starts/runs the game
    def playGame(self):
        self.addRobot('ball1', 2.25, .4, .25, 27)
        self.addRobot('ball2', .25, .25, .25, 105)
        self.addRobot('ball3', 1.25, 1.4, .25, 290)
        while self.gameTicks < 500:
            for i in range(50): #Why do this?
                self.playPlace.execture_turn()
            for index in range(0,len(self.turtles)):
                self.turtles[index].goto((self.playPlace.players[index].xloc),(self.playPlace.players[index].yloc))
                self.turtles[index].setheading(self.playPlace.players[index].orientation+90)
            print self.gameTicks
            for robot in self.robots:
                robot.dump_stats()
            print self.playPlace.players
            self.incrementGameTicks()
        turtle.done()

    #This function generates a new color for the robot and checks that it isn't too similiar to other robot colors
    #This function modifies the usedRobotColors once a new color has been found
    def getNewColor(self):
        resolution = 5 #This is an arbitrary variable that we use to set the boundary between how much 2 colors will look alike.
        gotNewColor = 0
        NewColor = (None,None,None)
        while gotNewColor == 0:
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)
            gotNewColor = 1
            NewColor = (red,green,blue)
            for color in self.usedRobotColors:
                if( (abs(color[0]-NewColor[0]) < resolution) and (abs(color[1]-NewColor[1]) < resolution) and (abs(color[2]-NewColor[2]) < resolution)):
                    gotNewColor = 0
                    break
        self.usedRobotColors.append(NewColor)
        return NewColor

    def putRobotInPlayGround(self, robot):
        self.playPlace.add_player(robot)

    #This function takes the properties of the robot as input, creates a robot object, and a turlte object. Puts items into appropiate lists.
    def addRobot(self, name, xLocation, yLocation, in_velocity, in_orientation):
        newRobotIndex = len(self.robots)
        Coordinates = {'xloc' : xLocation, 'yloc' : yLocation}
        self.robots.append(weasel.WeaselBall(str(newRobotIndex), Coordinates, velocity=in_velocity, orientation=in_orientation ))
        self.putRobotInPlayGround(self.robots[newRobotIndex])
        self.turtles.append(turtle.Turtle())
        newTurtleColor = self.getNewColor()
        self.turtles[newRobotIndex].color(newTurtleColor)
        self.turtles[newRobotIndex].pencolor(newTurtleColor)
        self.turtles[newRobotIndex].penup()
        self.turtles[newRobotIndex].setx(xLocation)
        self.turtles[newRobotIndex].sety(yLocation)
        self.turtles[newRobotIndex].pendown()

if __name__ == "__main__":
    simulator = Simulator()
    simulator.playGame()

        