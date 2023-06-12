import numpy
import math
import arcade

# These constants control the particulars about the radar
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Soundseer"
UPDATE_RATE = 0.016666666666666666
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIANS_PER_FRAME = 0.02
SWEEP_LENGTH = 250


class Radar:
    def __init__(self, update_rate, bpm, beats):
        self.angle = 0
        self.radians_per_frame = bpm * update_rate * (numpy.pi / 60)
        print("radians / frame: " + str(self.radians_per_frame))
        self.beats = iter(beats)
        self.next_beat = next(self.beats)

    def update(self, time):
        # Move the angle of the sweep.
        self.angle += self.radians_per_frame

    def draw(self, time):
        """ Use this function to draw everything to the screen. """

        # Calculate the end point of our radar sweep. Using math.
        x = SWEEP_LENGTH * math.sin(self.angle) + CENTER_X
        y = SWEEP_LENGTH * math.cos(self.angle) + CENTER_Y

        # Start the render. This must happen before any drawing
        # commands. We do NOT need a stop render command.
        arcade.start_render()

        # Draw the radar line
        if self.angle % numpy.pi < 1:
            arcade.draw_line(CENTER_X, CENTER_Y, x, y, arcade.color.BARBIE_PINK, 10)
        else:
            arcade.draw_line(CENTER_X, CENTER_Y, x, y, arcade.color.AMBER, 4)

        # Draw the outline of the radar
        beat_time = round(self.next_beat, 5)
        buffer = 0.04
        time = round(time, 5)
        print("beat time: " + str(beat_time))
        print("game time: " + str(time))
        print()
        if beat_time - buffer < time:
            print("On beat")
            arcade.draw_circle_outline(CENTER_X,
                                       CENTER_Y,
                                       SWEEP_LENGTH,
                                       arcade.color.ELECTRIC_ULTRAMARINE,
                                       border_width=40,
                                       num_segments=60)
            if time > beat_time + 2 * buffer:
                self.next_beat = next(self.beats)
        else:
            arcade.draw_circle_outline(CENTER_X,
                                       CENTER_Y,
                                       SWEEP_LENGTH,
                                       arcade.color.ELECTRIC_ULTRAMARINE,
                                       border_width=10,
                                       num_segments=60)
