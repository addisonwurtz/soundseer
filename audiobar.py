import pygame


def clamp(min_value, max_value, value):
    """Clamps rectangle height so animation stays pretty"""
    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioBar:
    """Represents a single frequency bucket, expressed as a rectangle that moved up and down based on the prevelance
    of those frequencies at a given time"""

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0, border_radius=25):
        """Initializes each rectangle to its default height and color. Sets height and decibel reactivity bounds."""

        self.x, self.y, self.freq = x, y, freq

        self.color = pygame.Color(color)

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.border_radius = border_radius

        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):
        """Updates height of rectangle based on current decibel"""

        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        speed = (desired_height - self.height)/0.1

        self.height += speed * dt

        self.height = clamp(self.min_height, self.max_height, self.height)

    def render(self, screen):
        """re-render rectangle with updated height"""

        pygame.draw.rect(screen, self.color, (self.x, self.y - self.height, self.width, self.height),
                         border_top_right_radius=self.border_radius, border_top_left_radius=self.border_radius)
