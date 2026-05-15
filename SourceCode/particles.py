import random
import pygame

class Particle:
    def __init__(self, pos, color, max_radius, lifetime, velocity=None):
        self.x, self.y = pos
        self.color = list(color)
        self.max_radius = max_radius
        self.lifetime = lifetime
        self.age = 0
        self.radius = 0
        
        # Initial velocity
        if velocity:
            self.vx, self.vy = velocity
        else:
            self.vx = random.uniform(-150, 150)
            self.vy = random.uniform(-150, 150)
            
        self.drag = 0.95  # Air resistance / Drag

    def update(self, dt):
        self.age += dt
        if self.age >= self.lifetime:
            return False
            
        # Movement with drag
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx *= self.drag
        self.vy *= self.drag
        
        # Radius grows then shrinks slightly
        progress = self.age / self.lifetime
        if progress < 0.2:
            self.radius = self.max_radius * (progress / 0.2)
        else:
            self.radius = self.max_radius * (1 - (progress - 0.2) / 0.8)
            
        return True

    def draw(self, surface):
        # Draw directly to surface for performance (no alpha surface creation per frame)
        r_int = int(max(1, self.radius))
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), r_int)

class ParticleManager:
    def __init__(self):
        self.particles = []

    def emit(self, pos, color=(255, 200, 50), max_radius=15, lifetime=0.6, count=10):
        for _ in range(count):
            p = Particle(pos, color, max_radius, lifetime)
            self.particles.append(p)

    def update(self, dt):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
