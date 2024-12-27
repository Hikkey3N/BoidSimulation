import pygame
import random
import math

WIDTH, HEIGHT = 800, 600
FPS = 60

class Boid:
    def __init__(self, x, y):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.acceleration = pygame.Vector2(0, 0)
        self.max_speed = 4
        self.max_force = 0.1

    def edges(self):
        """Make boids wrap around the screen edges."""
        if self.position.x > WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        elif self.position.y < 0:
            self.position.y = HEIGHT

    def apply_force(self, force):
        """Apply a force to the boid."""
        self.acceleration += force

    def seek(self, target):
        """Steer towards the target."""
        desired = target - self.position
        desired = desired.normalize() * self.max_speed
        steer = desired - self.velocity
        steer = steer.normalize() * self.max_force
        return steer

    def update(self):
        """Update the boid's position and velocity."""
        self.velocity += self.acceleration
        if self.velocity.length() > self.max_speed:
            self.velocity = self.velocity.normalize() * self.max_speed
        self.position += self.velocity
        self.acceleration *= 0  # Reset acceleration

    def flock(self, boids):
        """Apply all three behaviors (separation, alignment, cohesion)."""
        sep = self.separate(boids)
        ali = self.align(boids)
        coh = self.cohere(boids)

        # Apply forces
        self.apply_force(sep)
        self.apply_force(ali)
        self.apply_force(coh)

    def separate(self, boids):
        """Separation behavior: Steer to avoid crowding local boids."""
        desired_separation = 25
        steer = pygame.Vector2(0, 0)
        count = 0
        for boid in boids:
            distance = self.position.distance_to(boid.position)
            if distance > 0 and distance < desired_separation:
                diff = self.position - boid.position
                diff = diff.normalize() / distance  # Weight by distance
                steer += diff
                count += 1
        if count > 0:
            steer /= count
        if steer.length() > 0:
            steer = steer.normalize() * self.max_speed
            steer -= self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
        return steer

    def align(self, boids):
        """Alignment behavior: Steer to align with local boids."""
        neighbor_dist = 50
        steer = pygame.Vector2(0, 0)
        count = 0
        for boid in boids:
            if self.position.distance_to(boid.position) < neighbor_dist:
                steer += boid.velocity
                count += 1
        if count > 0:
            steer /= count
            steer = steer.normalize() * self.max_speed
            steer -= self.velocity
            if steer.length() > self.max_force:
                steer = steer.normalize() * self.max_force
        return steer

    def cohere(self, boids):
        """Cohesion behavior: Steer to move towards local boids' center."""
        neighbor_dist = 50
        steer = pygame.Vector2(0, 0)
        count = 0
        for boid in boids:
            if self.position.distance_to(boid.position) < neighbor_dist:
                steer += boid.position
                count += 1
        if count > 0:
            steer /= count  # Find the average position of the neighbors
            steer -= self.position  # Steer towards the center
            if steer.length() > 0:  # Only normalize if the vector is not zero
                steer = steer.normalize() * self.max_speed
                steer -= self.velocity
                if steer.length() > self.max_force:
                    steer = steer.normalize() * self.max_force
        return steer


    def draw(self, screen):
        """Draw the boid."""
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), 5)