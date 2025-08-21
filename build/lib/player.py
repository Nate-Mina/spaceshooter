import pygame
import os

class Player:
    def __init__(self, screen_width, screen_height):
        self.width = 50
        self.height = 30
        self.x = screen_width // 2 - self.width // 2
        self.y = screen_height - 50
        self.speed = 5
        self.color = (0, 255, 0)
        self.sprite = None
        sprite_path = os.path.join('assets', 'player.png')
        if os.path.exists(sprite_path):
            self.sprite = pygame.image.load(sprite_path).convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.width, self.height))

    def move_left(self):
        if self.x > 0:
            self.x -= self.speed

    def move_right(self):
        if self.x < 800 - self.width:  # Assuming screen width is 800
            self.x += self.speed

    def move_up(self):
        if self.y > 0:
            self.y -= self.speed

    def move_down(self):
        if self.y < 600 - self.height:  # Assuming screen height is 600
            self.y += self.speed

    def draw(self, screen):
        if self.sprite:
            screen.blit(self.sprite, (self.x, self.y))
        else:
            # Draw a green triangle for the player spaceship
            point1 = (self.x + self.width // 2, self.y)
            point2 = (self.x, self.y + self.height)
            point3 = (self.x + self.width, self.y + self.height)
            pygame.draw.polygon(screen, self.color, [point1, point2, point3])