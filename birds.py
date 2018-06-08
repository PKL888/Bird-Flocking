# Bird Floncking Movement by Peleg Kark-Levin
# Boids...


import random
import math
import pygame
import sys


pygame.init()

size = width, height = 800, 600
black = 0, 0, 0
white = 255, 255, 255
blue = 0, 0, 255
light_blue = 0, 0, 200
purple = 255, 0, 255
greyish = 50, 50, 50
green = 0, 255, 0
light_green = 0, 200, 0

maxVelocity = 10
numBirds = 1
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
mybird = pygame.transform.scale(mybird, (7, 7))
mybirdrect = mybird.get_rect()


def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()


def button(msg, x, y, w, h, inactive_colour, active_colour, numBirds, action):
    # mouse interaction |
    mouse = pygame.mouse.get_pos()
    print mouse

    click = pygame.mouse.get_pressed()
    print click

    # if x + width > mouse[x] > x and y + height > mouse[y] > y:
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, inactive_colour, (x, y, w, h))

        if click[0] == 1 and numBirds is not None:

            if action == "add":
                birds.append(Bird(random.randint(0, width), random.randint(0, height)))
            elif action == "remove":
                if myBirdsNum > 0:
                    birds.remove(bird)

            # numBirds += 1
            print "Yay!"
    else:
        pygame.draw.rect(screen, active_colour, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurface, textRect = text_objects(msg, smallText)
    textRect.center = ((x + (w / 2)), (y + (h / 2)))
    screen.blit(textSurface, textRect)


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

    # The adding more birds button -->
    button("Birds", 25, 25, 88, 88, blue, light_blue, numBirds, "add")

    # The goodbye birds button -->
    button("Goodbye!", 150, 25, 118, 88, green, light_green, numBirds, "remove")

    # Counting how many birds there are -->
    myBirdsNum = 0

    for i in birds:
        myBirdsNum += 1

    print myBirdsNum

    # The current amount of birds bubble -->
    pygame.draw.rect(screen, greyish, (500, 25, 250, 50))

    # Adding the text
    smallText = pygame.font.Font("freesansbold.ttf", 10)
    ttextSurface, ttextRect = text_objects("Current amount of birds:", smallText)
    ttextRect.center = ((500 + (250 / 2)), (25 + (50 / 2)))
    screen.blit(ttextSurface, ttextRect)

    # The actual quantity -->
    smallText = pygame.font.Font("freesansbold.ttf", 11)
    stextSurface, stextRect = text_objects("{0}".format(myBirdsNum), smallText)
    stextRect.center = ((700 + (50 / 2)), (25 + (50 / 2)))
    screen.blit(stextSurface, stextRect)

    # Displaying...
    pygame.display.flip()
    pygame.time.delay(10)
