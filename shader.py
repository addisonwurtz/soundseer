import librosa
import arcade
from arcade.experimental import Shadertoy
import argparse

"""seconds per frame"""
UPDATE_RATE = 1 / 60

parser = argparse.ArgumentParser(prog='BeatRadar',
                                 description='Music visualizer that detects and animates the beat of an audio file.')
parser.add_argument(
    "filename",
    help="Name of audio file to visualize (mp3)"
)


class MyGame(arcade.Window):
    """Game window maintains animation and game loop"""
    def __init__(self, filename, bpm, beats):
        super().__init__(width=1800, height=1000)

        """Name of audio file"""
        self.filename = filename
        """beats per minutes, from librosa estimate"""
        self.bpm = bpm
        """array of beats detected by librosa tools"""
        self.beats = iter(beats)
        """next beat as tracked by iterator"""
        self.next_beat = next(self.beats)
        self.update_rate = UPDATE_RATE
        self.set_update_rate(UPDATE_RATE)
        self.scale = 0.02

        """The name of the shader file"""
        shader_file_path = "circle_1.glsl"

        with open(shader_file_path) as file:
            shader_source = file.read()

        """create shader object in game window"""
        self.shadertoy = Shadertoy(size=self.get_size(),
                                   main_source=shader_source)

        """load sound file"""
        self.song = arcade.Sound(filename, streaming=True)
        """play song and passing player object for future time synchronization"""
        self.player = self.song.play()
        self.time = 0

    def on_update(self, delta_time: float):
        self.time += delta_time

    def on_draw(self):
        """redraw shader based on beats in song"""

        """if within one update before next beat"""
        if self.next_beat - UPDATE_RATE < self.song.get_stream_position(self.player):

            self.scale = 0.05
            if self.song.get_stream_position(self.player) > self.next_beat + 5 * self.update_rate:
                self.next_beat = next(self.beats)
        else:
            self.scale = 0.02

        """Set uniform data to send to the GLSL shader"""
        self.shadertoy.program['color'] = arcade.get_three_float_color(arcade.color.AMBER)
        self.shadertoy.program['scale'] = self.scale

        # Run the GLSL code
        self.shadertoy.render()


if __name__ == "__main__":
    args = parser.parse_args()

    time_series, sample_rate = librosa.load(args.filename)
    bpm, beats = librosa.beat.beat_track(y=time_series, sr=sample_rate, units='time')

    MyGame(args.filename, bpm, beats)
    arcade.run()
