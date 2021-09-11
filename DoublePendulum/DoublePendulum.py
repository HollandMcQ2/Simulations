import pygame, math

Black = (0,0,0)
White = (255,255,255)
Blue = (0,0,255)
clock = pygame.time.Clock()

size = (900,600)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Double Pendulum")


origin = [int(size[0]/2),100]
r1 = 100
r2 = 100
m1 = 10
m2 = 10
g = 1

a1 = math.pi/2
a2 = math.pi/8
a1_v = 0
a2_v = 0
a1_a = 0
a2_a = 0





# creates tracer sprites to draw on the screen to follow the path
class Tracer(pygame.sprite.Sprite):
	def __init__(self,x,y,Color,size=2):
		super().__init__()
		self.image = pygame.Surface([size,size])
		self.image.fill(Color)
		self.rect = self.image.get_rect()

		self.rect.x = x
		self.rect.y = y

all_tracers = pygame.sprite.Group()


CarryOn = True

while CarryOn:

	x1 = (math.sin(a1)*r1) + origin[0]
	y1 = (math.cos(a1)*r1) + origin[1]

	x2 = x1 + (math.sin(a2)*r2)
	y2 = y1 + (math.cos(a2)*r2)

	tracer = Tracer(x2,y2,Black)
	tracer2 = Tracer(x1,y1,Blue)
	all_tracers.add(tracer,tracer2)

	a1_v += a1_a
	a2_v += a2_a
	a1 += a1_v
	a2 += a2_v


	num1 = ((-1*g)*((2*m1)+m2)*math.sin(a1))
	num2 = (m2*g*math.sin(a1-(2*a2)))
	num3 = (((2*math.sin(a1-a2))*m2)*((((a2_v)**2)*r2) + (((a1_v)**2)*r1*math.cos(a1-a2))))
	den1 = (r1*((2*m1) + m2 - (m2*math.cos((2*a1) - (2*a2)))))
	a1_a = (num1 - num2 -num3) / (den1)

	num1 = (2*math.sin(a1-a2))
	num2 = (a1_v*a1_v*r1*(m1+m2))
	num3 = (g*(m1+m2)*math.cos(a1))
	num4 = (a2_v*a2_v*r2*m2*math.cos(a1-a2))
	den1 = (r2*(2*m1 + m2 - (m2*math.cos(2*a1 - 2*a2))))
	a2_a = (num1 * (num2 + num3 + num4)) / (den1)

	# # dampening
	# a1_v *= .999
	# a2_v *= .999

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			CarryOn = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_x:
				CarryOn = False
				
				
	
	
	screen.fill(White)
	pygame.draw.circle(screen, Black, [origin[0], origin[1]], 10) # circle @ origin
	pygame.draw.line(screen, Black, [origin[0], origin[1]], [int(x1), int(y1)], 2) # line from origin to first mass
	pygame.draw.circle(screen, Black, [int(x1),int(y1)],m1) # first mass
	pygame.draw.line(screen, Black, [int(x1),int(y1)], [int(x2), int(y2)], 2)
	pygame.draw.circle(screen,Black,[int(x2),int(y2)],m2) # second mass
	all_tracers.draw(screen)
	pygame.display.flip()
	
	clock.tick(60)
	
pygame.quit()
	
	
	
	