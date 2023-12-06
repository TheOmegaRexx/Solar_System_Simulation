import pygame
import math

pygame.init()

# Set up window dimensions
WIDTH, HEIGHT = 1920, 1080
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
COLOUR = (0, 0, 0)
pygame.display.set_caption("Solar System")

# Define a class for planets
class Planet:
    # Astronomical Unit Distance from the Earth to the Sun in Meters
    AU = 149.6e6 * 1000
    # Gravitational Constant
    G = 6.67428e-11
    # 1AU = 100 Pixels
    SCALE = 250 / AU
    # Represents 1 Day
    TIMESTEP = 3600 * 24

    def __init__(self, x, y, radius, colour, mass):
        # Initialize planet properties
        self.x = x
        self.y = y
        self.radius = radius
        self.colour = colour
        self.mass = mass  # Mass in KG

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, win):
        # Draw the planet on the window
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x, y))

            pygame.draw.lines(win, self.colour, False, updated_points, 2)
        pygame.draw.circle(win, self.colour, (x, y), self.radius)

    def attraction(self, other):
        # Calculate the force of attraction between planets
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        # Check if other object is the Sun
        if other.sun:
            self.distance_to_sun = distance

        # Calculate the force of attraction
        force = self.G * self.mass * other.mass / distance**2
        # Break the Force into the x and y components by calculating the angle
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        # Update the position of the planet based on gravitational forces
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Acceleration = Force / Mass equation
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

# Main function
def main():
    run = True
    clock = pygame.time.Clock()

    # Create Sun and planets
    sun = Planet(0, 0, 30, (255, 255, 0), 1.98892 * 10**30)
    sun.sun = True

    earth = Planet(-1 * Planet.AU, 0, 16, (100, 149, 237), 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, (188, 39, 50), 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, (80, 78, 81), 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, (255, 255, 255), 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    jupiter = Planet(5.203 * Planet.AU, 0, 20, (255, 165, 0), 1.898 * 10**27)
    jupiter.y_vel = -13.06 * 1000

    saturn = Planet(9.537 * Planet.AU, 0, 18, (210, 180, 140), 5.683 * 10**26)
    saturn.y_vel = -9.68 * 1000

    uranus = Planet(19.191 * Planet.AU, 0, 15, (135, 206, 250), 8.681 * 10**25)
    uranus.y_vel = -6.8 * 1000

    neptune = Planet(30.05 * Planet.AU, 0, 14, (0, 0, 128), 1.024 * 10**26)
    neptune.y_vel = -5.43 * 1000

    planets = [sun, earth, mars, mercury, venus, jupiter, saturn, uranus, neptune]



    while run:
        clock.tick(60)
        WIN.fill(COLOUR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Update and draw planets
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

# Run the main function
if __name__ == '__main__':
    main()
