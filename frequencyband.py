import pygame

from audiobar import AudioBar
import numpy as np


class FrequencyBand:
    """Class representing a frequency band that manages the bars (frequency buckets) that move with the music"""

    def __init__(self, lower_bound, upper_bound, song_frequencies, base_color, min_height, max_height, screen_w,
                 screen_h, num_bars):
        """Upper and lower bounds for the frequency band"""
        self.lower_bound, self.upper_bound = lower_bound, upper_bound
        """Number of bars in the frequency band"""
        self.num_bars = num_bars
        self.song_frequencies = song_frequencies
        """Color of the bars in the frequency band"""
        self.base_color = pygame.Color(list(map(int, base_color.split(","))))

        """Height of bars. Necessary to avoid excessive overlap between frequency bands """
        self.min_height = min_height
        self.max_height = max_height
        self.width = screen_w

        """List of frequency 'buckets' """
        self.frequency_ranges = self.get_frequency_range()
        self.frequency_index_ratio = self.get_frequency_index_ratio()
        self.bars = []
        self.get_bars(screen_h)

    def get_frequency_range(self):
        """Separate frequency band into equally spaced bars
        returns range of frequency buckets that will be used to represent the bars"""
        step = (self.upper_bound - self.lower_bound) // self.num_bars
        return np.arange(self.lower_bound, self.upper_bound, step)

    def get_frequency_index_ratio(self):
        return len(self.song_frequencies) / self.song_frequencies[len(self.song_frequencies) - 1]

    def get_bars(self, screen_h):
        """Get heights of each frequency bar.
        returns list of pygame rectangle representing each of the frequency buckets"""
        r = len(self.frequency_ranges)
        bar_width = self.width / r
        x = (self.width - bar_width * r) / 2
        for c in self.frequency_ranges:
            self.bars.append(
                AudioBar(x, screen_h, c, self.base_color, min_height=self.min_height, max_height=self.max_height,
                         width=bar_width))
            x += bar_width

