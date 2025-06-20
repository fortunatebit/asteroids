import pygame
from constants import *
from bullet import Bullet
from circleshape import CircleShape

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (135, 135, 135), self.triangle())

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-abs(dt))
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-abs(dt))
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        self.cooldown_timer -= dt

    def move(self, dt):
        # Check if, when moving, the player crosses any screen borders. If they do, loop them around to the opposite side
        if self.position.x - self.radius < 0:
            self.position = pygame.Vector2(SCREEN_WIDTH - self.radius, self.position.y)

        if self.position.x + self.radius > SCREEN_WIDTH:
            self.position = pygame.Vector2(0 + self.radius, self.position.y)

        if self.position.y - self.radius < 0:
            self.position = pygame.Vector2(self.position.x, SCREEN_HEIGHT - self.radius)

        if self.position.y + self.radius > SCREEN_HEIGHT:
            self.position = pygame.Vector2(self.position.x, 0 + self.radius)

        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.cooldown_timer > 0:
            return
        velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        bullet = Bullet(self.position.x, self.position.y, velocity)
        self.cooldown_timer = PLAYER_SHOOT_COOLDOWN