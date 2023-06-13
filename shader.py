import librosa
import numpy as np
import arcade
from arcade.experimental import Shadertoy

UPDATE_RATE = 1 / 60


# Derive an application window from Arcade's parent Window class
class MyGame(arcade.Window):

    def __init__(self, filename, bpm, beats):
        # Call the parent constructor
        super().__init__(width=1800, height=1000)

        self.filename = filename
        self.bpm = bpm
        self.beats = iter(beats)
        self.next_beat = next(self.beats)
        self.update_rate = UPDATE_RATE
        self.set_update_rate(UPDATE_RATE)
        self.scale = 0.02

        # Load a file and create a shader from it
        shader_file_path = "circle_1.glsl"

        with open(shader_file_path) as file:
            shader_source = file.read()

        self.shadertoy = Shadertoy(size=self.get_size(),
                                   main_source=shader_source)

        self.song = arcade.Sound(filename, streaming=True)
        self.player = self.song.play()
        self.time = 0

    def on_update(self, delta_time: float):
        self.time += delta_time

    def on_draw(self):

        if self.next_beat - UPDATE_RATE < self.song.get_stream_position(self.player):

            self.scale = 0.05
            if self.song.get_stream_position(self.player) > self.next_beat + 5 * self.update_rate:
                self.next_beat = next(self.beats)
        else:
            self.scale = 0.02

        # Set uniform data to send to the GLSL shader
        # self.shadertoy.program['pos'] = self.mouse["x"], self.mouse["y"]
        self.shadertoy.program['color'] = arcade.get_three_float_color(arcade.color.AMBER)
        self.shadertoy.program['scale'] = self.scale

        # Run the GLSL code
        self.shadertoy.render()


if __name__ == "__main__":
    filename = "Songs/DietMountainDewInstrumental.mp3"

    time_series, sample_rate = librosa.load(filename)
    bpm, beats = librosa.beat.beat_track(y=time_series, sr=sample_rate, units='time')

    MyGame(filename, bpm, beats)
    arcade.run()
