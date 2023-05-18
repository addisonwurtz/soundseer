from audiobar import AudioBar
import numpy as np


class FrequencyBand:

    def __init__(self, lower_bound, upper_bound, song_frequencies, base_color, min_height, max_height, screen_w,
                 screen_h, num_bars=20):
        self.lower_bound, self.upper_bound = lower_bound, upper_bound
        self.num_bars = num_bars
        self.song_frequencies = song_frequencies
        self.base_color = base_color
        self.min_height = min_height
        self.max_height = max_height
        self.width = screen_w


        self.frequency_ranges = self.get_frequency_range()
        self.frequency_index_ratio = self.get_frequency_index_ratio()

        self.bars = []
        self.get_bars(screen_h)

    # Separate frequency band into equally spaced bars
    def get_frequency_range(self):
        step = (self.upper_bound - self.lower_bound) // self.num_bars
        return np.arange(self.lower_bound, self.upper_bound, step)

    def get_frequency_index_ratio(self):
        return len(self.song_frequencies) / self.song_frequencies[len(self.song_frequencies) - 1]

    # Get heights for each frequency bar
    def get_bars(self, screen_h):
        r = len(self.frequency_ranges)
        bar_width = self.width / r
        x = (self.width - bar_width * r) / 2
        for c in self.frequency_ranges:
            self.bars.append(
                AudioBar(x, screen_h, c, self.base_color, min_height=self.min_height, max_height=self.max_height,
                         width=bar_width))
            x += bar_width

