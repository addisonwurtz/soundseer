import librosa.util
import numpy
import math
import arcade

# These constants control the particulars about the radar
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Soundseer"
UPDATE_RATE = 0.016666
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIANS_PER_FRAME = 0.02
SWEEP_LENGTH = 250


class Radar:
    def __init__(self, update_rate, bpm, beats, times, pulse):
        self.angle = 0
        self.radians_per_frame = bpm * update_rate * (numpy.pi / 120)
        print("radians / frame: " + str(self.radians_per_frame))

        self.times = iter(times)
        self.next_time = next(self.times)
        self.pulse = iter(pulse)
        self.next_pulse = next(self.pulse)

    def update(self):
        # Move the angle of the sweep.
        self.angle += self.radians_per_frame

    def draw(self, player, song):
        """ Use this function to draw everything to the screen. """

        # Calculate the end point of our radar sweep. Using math.
        x = (SWEEP_LENGTH + 100 * self.next_pulse) * math.sin(self.angle) + CENTER_X
        y = (SWEEP_LENGTH + 100 * self.next_pulse) * math.cos(self.angle) + CENTER_Y

        # Start the render. This must happen before any drawing
        # commands. We do NOT need a stop render command.
        arcade.start_render()



        # Draw the outline of the radar
        if self.next_time - UPDATE_RATE < song.get_stream_position(player):
            if self.next_pulse > 0.05:
                arcade.draw_circle_outline(CENTER_X,
                                           CENTER_Y,
                                            SWEEP_LENGTH + 100 * self.next_pulse,
                                           (100 + self.next_pulse * 100, 10, 255 - self.next_pulse * 80, 140 * self.next_pulse + 100),
                                           border_width=600 + 100 * self.next_pulse,
                                           num_segments=60)
            else:
                arcade.draw_circle_outline(CENTER_X,
                                           CENTER_Y,
                                           SWEEP_LENGTH,
                                           arcade.color.ELECTRIC_ULTRAMARINE,
                                           border_width=10,
                                           num_segments=60)
            if song.get_stream_position(player) > self.next_time + 5 * UPDATE_RATE:
                self.next_time = next(self.times)
                self.next_pulse = next(self.pulse)
        else:
            arcade.draw_circle_outline(CENTER_X,
                                       CENTER_Y,
                                       SWEEP_LENGTH,
                                       arcade.color.ELECTRIC_ULTRAMARINE,
                                       border_width=10,
                                       num_segments=60)

        # Draw the radar line
        if self.angle % numpy.pi < 1:
            arcade.draw_line(CENTER_X, CENTER_Y, x, y, arcade.color.BARBIE_PINK, 6)
        elif self.angle % numpy.pi < 2:
            arcade.draw_line(CENTER_X, CENTER_Y, x, y, arcade.color.FLUORESCENT_YELLOW, 8)
        else:
            arcade.draw_line(CENTER_X, CENTER_Y, x, y, arcade.color.AMBER, 4)