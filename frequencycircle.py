from audiobar import AudioBar
import numpy as np


class FrequencyCircle:

    def __init__(self, lower_bound, upper_bound, song_frequencies, base_color, circle_x, circle_y, min_radius=100,
                 max_radius=300, num_bars=20):
        self.lower_bound, self.upper_bound = lower_bound, upper_bound
        self.song_frequencies = song_frequencies
        self.base_color = base_color

        self.circle_x = circle_x
        self.circle_y = circle_y

        self.min_radius = min_radius
        self.max_radius = max_radius
        self.num_bars = num_bars

        self.frequency_ranges = self.get_frequency_range()
        self.frequency_index_ratio = self.get_frequency_index_ratio()

        self.bars = []
        self.get_bars()

    # Separate frequency band into equally spaced bars
    def get_frequency_range(self):
        step = (self.upper_bound - self.lower_bound) // self.num_bars
        return np.arange(self.lower_bound, self.upper_bound, step)

    def get_frequency_index_ratio(self):
        return len(self.song_frequencies) / self.song_frequencies[len(self.song_frequencies) - 1]

    # Get heights for each frequency bar
    def get_bars(self):
        r = len(self.frequency_ranges)
        bar_width = (2 * np.pi * self.min_radius) / self.num_bars
        coordinates = self.get_points_on_circle()
        angles = np.arange(0, 360, 360 / self.num_bars)
        print(angles)

        for freq, coordinate, angle in zip(self.frequency_ranges, coordinates, angles):
            self.bars.append(
                AudioBar(coordinate[0], coordinate[1], freq, self.base_color, angle=angle,
                         min_height=10,
                         max_height=self.max_radius,
                         width=bar_width))
            # x += bar_width

    def get_points_on_circle(self):
        return [
            (
                self.circle_x + (np.cos(2 * np.pi / self.num_bars * x) * self.min_radius),  # x
                self.circle_y + (np.sin(2 * np.pi / self.num_bars * x) * self.min_radius),  # y
                (np.cos((2 * np.pi / self.num_bars * x))) # angle

            ) for x in range(0, self.num_bars + 1)]
