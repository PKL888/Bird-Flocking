# Bird Floncking Movement by Peleg Kark-Levin
# Boids...


import random
import math
import pygame
import sys


pygame.init()

size = width, height = 800, 600
white = 255, 255, 255
black = 0, 0, 0

maxVelocity = 10
numBirds = 50
birds = []


class Bird:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocityX = random.randint(1, 10) / 10.0
        self.velocityY = random.randint(1, 10) / 10.0

    def distance(self, bird):
        distX = self.x - bird.x
        distY = self.y - bird.y

        return math.sqrt((distX ** 2) + (distY ** 2))

    # Rule 1: Seperation - steer to avoid crowding local flockmates
    def seperate(self, birds, minDistanceBetweenBirds):
        if len(birds) < 1:
            return

        distanceX = 0
        distanceY = 0
        closerBirds = 0

        for bird in birds:
            distance = self.distance(bird)

            if distance < minDistanceBetweenBirds:
                closerBirds += 1

                xDiff = (self.x - bird.x)
                yDiff = (self.y - bird.y)

                if xDiff >= 0:
                    xDiff = math.sqrt(minDistanceBetweenBirds) - xDiff
                elif xDiff < 0:
                    xDiff = -math.sqrt(minDistanceBetweenBirds) - xDiff

                if yDiff >= 0:
                    yDiff = math.sqrt(minDistanceBetweenBirds) - yDiff
                elif yDiff < 0:
                    yDiff = -math.sqrt(minDistanceBetweenBirds) - yDiff

                distanceX += xDiff
                distanceY += yDiff

        if closerBirds == 0:
            return

        self.velocityX -= distanceX / 5
        self.velocityY -= distanceY / 5

    # Rule 2: Alignment - steer towards the average heading of local flockmates
    def alignment(self, birds):
        if len(birds) < 1:
            return

        # calculate the average velocities of other birds
        avgdX = 0
        avgdY = 0

        for bird in birds:
            avgdX += bird.velocityX
            avgdY += bird.velocityY

        avgdX /= len(birds)
        avgdY /= len(birds)

        # set our velocity towards others
        self.velocityX += (avgdX / 40)
        self.velocityY += (avgdY / 40)

    # Rule 3: Cohesion - steer toward the average position of local flockmates
    def cohesion(self, birds):
        if len(birds) < 1:
            return

        # calculate the average distance from the other birds in the flock...
        avgvX = 0
        avgvY = 0

        for bird in birds:
            if bird.x == self.x and bird.y == self.y:
                continue

            avgvX += (self.x - bird.x)
            avgvY += (self.y - bird.y)

        avgvX /= len(birds)     # arithmetical operation
        avgvY /= len(birds)     # of average taking calc

        # set velocity in comparison to the others
        distance = -math.sqrt((avgvX ** 2) + (avgvY ** 2))

        self.velocityX -= (avgvX / 100)
        self.velocityY -= (avgvY / 100)

    # actually move the birds
    def move(self):
        if abs(self.velocityX > maxVelocity or abs(self.velocityY >
                                                   maxVelocity)):
            scalingFactor = maxVelocity / max(abs(self.velocityX),
                                              abs(self.velocityY))
            self.velocityX *= scalingFactor
            self.velocityY *= scalingFactor

        self.x += self.velocityX
        self.y += self.velocityY


screen = pygame.display.set_mode(size)

mybird = pygame.image.load("bluebird2.png")
mybird = pygame.transform.scale(mybird, (5, 5))
mybirdrect = mybird.get_rect()

# create the birds in random positions
for i in range(numBirds):
    birds.append(Bird(random.randint(0, width), random.randint(0, height)))

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    for bird in birds:
        closerBirds = []

        for otherBird in birds:
            if otherBird == bird:
                continue

            distance = bird.distance(otherBird)

            if distance < 200:
                closerBirds.append(otherBird)

        bird.cohesion(closerBirds)
        bird.alignment(closerBirds)
        bird.seperate(closerBirds, 20)

        # ensure birds stay within the screen
        # if they rebound they lose some of their velocity
        border = 25

        if bird.x < border and bird.velocityX < 0:
            bird.velocityX = -bird.velocityX * random.random()

        if bird.x > width - border and bird.velocityX > 0:
            bird.velocityX = -bird.velocityX * random.random()

        if bird.y < border and bird.velocityY < 0:
            bird.velocityY = -bird.velocityY * random.random()

        if bird.y > height - border and bird.velocityY > 0:
            bird.velocityY = -bird.velocityY * random.random()

        bird.move()

    screen.fill(black)

    for bird in birds:
        mybirdrect = pygame.Rect(mybirdrect)

        mybirdrect.x = bird.x
        mybirdrect.y = bird.y

        screen.blit(mybird, mybirdrect)

    pygame.display.flip()
    pygame.time.delay(10)
