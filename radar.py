import arcade
import math
import tkinter

root = tkinter.Tk()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Soundseer"

BASS_CUTOFF = 300
TREBLE_CUTOFF = 4000

# These constants control the particulars about the radar
CENTER_X = SCREEN_WIDTH // 2
CENTER_Y = SCREEN_HEIGHT // 2
RADIANS_PER_FRAME = 0.02
SWEEP_LENGTH = 250

soundfile="/Songs/DietMountainDewInstrumental.mp3"

class Radar:
    def __init__(self):
        self.angle = 0


    def update(self):

        # Move the angle of the sweep.
        self.angle += RADIANS_PER_FRAME

    def draw(self):
        """ Use this function to draw everything to the screen. """

        # Calculate the end point of our radar sweep. Using math.
        x = SWEEP_LENGTH * math.sin(self.angle) + CENTER_X
        y = SWEEP_LENGTH * math.cos(self.angle) + CENTER_Y

        # Start the render. This must happen before any drawing
        # commands. We do NOT need an stop render command.
        arcade.start_render()

        # Draw the radar line
        arcade.draw_line(CENTER_X, CENTER_Y, x, y, arcade.color.OLIVE, 4)

        # Draw the outline of the radar
        arcade.draw_circle_outline(CENTER_X,
                                   CENTER_Y,
                                   SWEEP_LENGTH,
                                   arcade.color.DARK_GREEN,
                                   border_width=10,
                                   num_segments=60)


class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height, title):
        super().__init__(width, height, title, fullscreen=False)

        width, height = self.get_size()
        self.set_viewport(0, width, 0, height)
        arcade.set_background_color(arcade.color.AMAZON)
        self.example_image = arcade.load_texture(":resources:images/tiles/boxCrate_double.png")

        # Create our rectangle
        self.radar = Radar()

        # Set background color
        arcade.set_background_color(arcade.color.BLACK)

        song = arcade.Sound(soundfile, streaming=True)
        song.play()

    def on_update(self, delta_time):
        # Move the rectangle
        self.radar.update()

    def on_draw(self):
        """ Render the screen. """

        # Clear screen
        self.clear()
        # Draw the rectangle
        self.radar.draw()

        # Get viewport dimensions
        left, screen_width, bottom, screen_height = self.get_viewport()

        text_size = 18
        # Draw text on the screen so the user has an idea of what is happening
        arcade.draw_text("Press F to toggle between full screen and windowed mode, unstretched.",
                         screen_width // 2, screen_height // 2 - 20,
                         arcade.color.WHITE, text_size, anchor_x="center")
        arcade.draw_text("Press S to toggle between full screen and windowed mode, stretched.",
                         screen_width // 2, screen_height // 2 + 20,
                         arcade.color.WHITE, text_size, anchor_x="center")

        # Draw loop
        #for x in range(64, 800, 128):

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
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()


if __name__ == "__main__":
    main()