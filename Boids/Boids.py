import pygame, math, random, numpy
# from numpy import *

Black = (0,0,0)
White = (255,255,255)
Blue = (0,0,255)

ScreenSize = (900,600)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(ScreenSize)
pygame.display.set_caption("Boids Simulation")

number_of_boids = 100
maxForce = 10

def distanceFormula(x1,y1,x2,y2):
    X = (x2-x1)**2
    Y = (y2-y1)**2
    distance = math.sqrt(X+Y)
    return distance

#Function to calculate a unit vector to be used later
# Vector1 = new origin
# Vector2 = direction of new vector
def UnitVector(Vector1,Vector2):
    NewVector = Vector2 - Vector1
    mag = 1/math.sqrt(NewVector[0]**2 + NewVector[1]**2)
    unitVector = Vector2*mag
    return unitVector

# self made funcion that I made to fit what I needed
# This function will scale down a vector to have any desired magnitude
def SetMag(self, magnitude):
    mag = 1/math.sqrt(self[0]**2 + self[1]**2)
    desiredMag = mag*self*magnitude
    return desiredMag

#class to create and update boids
#radius of boids is set to be 5
#higher speed value = higher speed
class boid(pygame.sprite.Sprite):
    def __init__(self, ScreenSize, size=5, speed=10): 
        super().__init__()
        self.x = random.randint(1, ScreenSize[0] - 1)
        self.y = random.randint(1, ScreenSize[1] - 1)
        self.size = size
        self.color = Black
        self.speed = speed
        self.velocity = numpy.random.uniform(size=2)
        self.velocity = SetMag(self.velocity, random.uniform(2,5))
        self.acceleration = numpy.zeros(2)
        self.maxSpeed = 5
    
    def display(self):
        pygame.draw.circle(screen,self.color, (int(self.x),int(self.y)), self.size)
    
    def cohesion(self, Flock, perceptionRadius=25):
        nearby = []
        AvgX = 0
        AvgY = 0
        for boid in Flock:
            if (self != boid) and (distanceFormula(self.x,self.y,boid.x,boid.y) <= (perceptionRadius)):
                nearby.append(boid)
                AvgX += boid.x
                AvgY += boid.y
        if len(nearby) > 1:
            AvgX /= len(nearby)
            AvgY /= len(nearby)
            newVelocity = [self.speed * item for item in UnitVector([self.x,self.y],[AvgX,AvgY])]
            print(newVelocity)
            self.x += newVelocity[0]
            self.y += newVelocity[1]

    def align(self, Flock, perceptionRadius=25):
        total = 0
        steering = numpy.zeros(2)
        for boid in Flock:
            if (boid != self) and (distanceFormula(self.x,self.y,boid.x,boid.y) <= (perceptionRadius)):
                steering += boid.velocity
                total += 1
        if total > 0:
            steering /= total
            steering = UnitVector([0,0],steering)*self.maxSpeed
            steering -= self.velocity
            steering = numpy.interp(steering, (-15, 15), (-1*maxForce, 1*maxForce))
        return steering     

    def Flock(self, boids):
        alignment = self.align(boids)
        self.acceleration = alignment

    def edges(self):
        if self.x < 0:
            self.x = 900
        elif self.x > 900:
            self.x = 0
        if self.y < 0:
            self.y = 600
        elif self.y > 600:
            self.y = 0

    def update(self):
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.velocity += self.acceleration
        # print(self.acceleration)
        self.acceleration *= 0
        # print(self.acceleration)
        # if self.velocity[0] > self.speed:
        #     self.velocity[0] = self.speed
        # if self.velocity[1] > self.speed:
        #     self.velocity[1] = self.speed


#create boids
Boids = []
for i in range(number_of_boids):
    Boids.append(boid(ScreenSize))


GameLoop = True
while GameLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameLoop = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:
                GameLoop = False

    
    


    #set screen to white
    screen.fill(White)
    #drawing code

    #display the boids
    for boid in Boids:
        boid.edges()
        boid.Flock(Boids)
        boid.update()
        boid.display()
    pygame.display.flip()
    # set fps to 60
    clock.tick(60)
pygame.quit()