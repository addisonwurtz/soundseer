import arcade
import math
import tkinter

import librosa.beat
import numpy

from radar import Radar

root = tkinter.Tk()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Soundseer"
UPDATE_RATE = 1 / 60

BASS_CUTOFF = 300
TREBLE_CUTOFF = 4000

# These constants control the particulars about the radar
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIANS_PER_FRAME = 0.02
SWEEP_LENGTH = 250

soundfile = "Songs/MKDomDolla-RhymeDust.mp3"
# soundfile = "Songs/155BPM.mp3"


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title, radar):
        super().__init__(width, height, title, fullscreen=False, vsync=True)

        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)

        self.update_rate = UPDATE_RATE
        self.set_update_rate(UPDATE_RATE)

        # Create our rectangle
        self.radar = radar

        # Set background color
        arcade.set_background_color(arcade.color.LICORICE)

        song = arcade.Sound(soundfile, streaming=True)
        song.play()
        self.time = -2 * self.update_rate

    def on_update(self, delta_time):
        # Move the rectangle
        self.radar.update(self.time)
        self.time += delta_time

    def on_draw(self):
        """ Render the screen. """

        # Clear screen
        self.clear()
        # Draw the rectangle
        self.radar.draw(self.time)

        # Get viewport dimensions
        left, screen_width, bottom, screen_height = self.get_viewport()

        text_size = 12
        # Draw text on the screen so the user has an idea of what is happening
        arcade.draw_text("Press F to toggle between full screen and windowed mode, unstretched.",
                         screen_width // 2, 10,
                         arcade.color.WHITE, text_size, anchor_x="center")
        arcade.draw_text("Press S to toggle between full screen and windowed mode, stretched.",
                         screen_width // 2, 30,
                         arcade.color.WHITE, text_size, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        if key == arcade.key.F:
            # User hits f. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Get the window coordinates. Match viewport to window coordinates
            # so there is a one-to-one mapping.
            width, height = self.get_size()
            self.set_viewport(0, width, 0, height)

        if key == arcade.key.S:
            # User hits s. Flip between full and not full screen.
            self.set_fullscreen(not self.fullscreen)

            # Instead of a one-to-one mapping, stretch/squash window to match the
            # constants. This does NOT respect aspect ratio. You'd need to
            # do a bit of math for that.
            self.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)


def main():
    """ Main function """
    time_series, sample_rate = librosa.load(soundfile)

    bpm, beats = librosa.beat.beat_track(y=time_series, sr=sample_rate, units='time')
    print("bpm: " + str(bpm))
    print(beats)

    radar = Radar(UPDATE_RATE, bpm, beats)
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, radar)

    arcade.run()


if __name__ == "__main__":
    main()
