import pygame
import random
import math
import time

# Initialize pygame
pygame.init()

# Screen settings
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Firework Simulation")

# Colors
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (255, 255, 255)]
GRAVITY = 0.3  # Gravity pulling particles downward

class Rocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.dy = -random.uniform(8, 12)  # Speed going up
        self.color = random.choice(COLORS)
        self.exploded = False

    def update(self):
        if not self.exploded:
            self.y += 3 * self.dy  # Move up
            self.dy += GRAVITY  # Apply gravity
            if self.dy >= 0:  # When it starts falling, explode
                self.exploded = True
                return Firework(self.x, self.y)
        return None

    def draw(self, screen):
        if not self.exploded:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)

class Firework:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.particles = []
        self.create_particles()
        self.flash = 5  # Initial flash duration

    def create_particles(self):
        for _ in range(random.randint(50,100)):  # 50 particles per firework
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            dx = math.cos(angle) * speed
            dy = math.sin(angle) * speed
            color = random.choice(COLORS)
            self.particles.append([self.x, self.y, dx, dy, color, 100])  # (x, y, dx, dy, color, lifespan)

    def update(self):
        if self.flash > 0:
            self.flash -= 1  # Reduce flash effect
        for particle in self.particles:
            particle[0] += particle[2]  # Update x position
            particle[1] += particle[3]  # Update y position
            particle[3] += GRAVITY  # Apply gravity to y velocity
            particle[5] -= 2  # Decrease lifespan
        self.particles = [p for p in self.particles if p[5] > 0]

    def draw(self, screen):
        if self.flash > 0:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 10)  # Flash effect
        for particle in self.particles:
            pygame.draw.circle(screen, particle[4], (int(particle[0]), int(particle[1])), max(1, particle[5] // 20))

# Main loop
running = True
rockets = []
fireworks = []
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))  # Clear screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    if random.random() < 0.05:  # Randomly launch a rocket
        rockets.append(Rocket(random.randint(100, WIDTH - 100), HEIGHT))

    for rocket in rockets[:]:
        new_firework = rocket.update()
        if new_firework:
            fireworks.append(new_firework)
            rockets.remove(rocket)
        else:
            rocket.draw(screen)

    for firework in fireworks:
        firework.update()
        firework.draw(screen)

    fireworks = [fw for fw in fireworks if fw.particles]  # Remove finished fireworks
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
