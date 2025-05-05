import pygame
import random


class Bullet:
    def __init__(self, x, y):
        self.width = 5
        self.height = 10
        self.x = x
        self.y = y
        self.speed = 7
        self.color = (255, 255, 0)

    def move(self):
        self.y -= self.speed

    def collides_with(self, enemy):
        return (
            self.x < enemy.x + enemy.width and
            self.x + self.width > enemy.x and
            self.y < enemy.y + enemy.height and
            self.y + self.height > enemy.y
        )

    def draw(self, screen):
        # Draw a yellow glowing bullet
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, (255, 255, 100), (self.x - 2, self.y - 4, self.width + 4, self.height + 8), 1)


class PowerUp:
    TYPES = ['rapid', 'shield', 'life']
    COLORS = {'rapid': (0, 200, 255), 'shield': (255, 255, 0), 'life': (0, 255, 0)}

    def __init__(self, x, y):
        self.type = random.choice(self.TYPES)
        self.x = x
        self.y = y
        self.radius = 15
        self.color = self.COLORS[self.type]
        self.active = True
        self.speed = 2

    def move(self):
        self.y += self.speed
        if self.y > 600:
            self.active = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        pygame.draw.circle(screen, (255, 255, 255), (self.x, self.y), self.radius, 2)
        font = pygame.font.SysFont(None, 24)
        text = font.render(self.type[0].upper(), True, (0, 0, 0))
        screen.blit(text, (self.x - 7, self.y - 10))


class Explosion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 1
        self.max_radius = 30
        self.active = True
        self.frames = 0

    def update(self):
        if self.radius < self.max_radius:
            self.radius += 4
            self.frames += 1
        else:
            self.active = False

    def draw(self, screen):
        if self.active:
            for i in range(6):
                angle = i * 60 + self.frames * 10
                dx = int(self.radius * 1.2 * pygame.math.Vector2(1, 0).rotate(angle).x)
                dy = int(self.radius * 1.2 * pygame.math.Vector2(1, 0).rotate(angle).y)
                pygame.draw.circle(screen, (255, 200, 50), (self.x + dx, self.y + dy), 6, 0)
            pygame.draw.circle(screen, (255, 100, 0), (self.x, self.y), self.radius, 2)