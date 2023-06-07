import argparse

import librosa
import numpy as np
import pygame
from audiobar import AudioBar
from frequencyband import FrequencyBand

parser = argparse.ArgumentParser(prog='BouncingBars',
                                 description='Music visualizer that animates the changing amplitudes of configurable '
                                             'frequency bands to chosen sound file.')
parser.add_argument(
    "filename",
    help="Name of audio file to visualize (mp3)"
)

args = parser.parse_args()

def get_decibel(target_time, freq, frequencies_index_ratio):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]


# TODO: add command line args for filename (and other knobs??)
#filename = "Songs/LanaDelRey-DietMountainDew(OfficialInstrumental).mp3"
# filename = "Songs/MKDomDolla-RhymeDust.mp3"
#filename = "Songs/Moby-'Porcelain'.mp3"

time_series, sample_rate = librosa.load(args.filename)  # getting information from the file

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

frequencies = librosa.core.fft_frequencies(n_fft=2048 * 4)  # getting an array of frequencies

# split into frequency bands
bass_frequencies, mid_frequencies, treble_frequencies = np.split(frequencies, [300, 4000])

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

time_index_ratio = len(times)/times[len(times) - 1]



pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w/1.5)
screen_h = int(infoObject.current_h/1.5)

bass_band = FrequencyBand(lower_bound=0,
                          upper_bound=300,
                          song_frequencies=bass_frequencies,
                          base_color=(255, 0, 0),
                          min_height=0,
                          max_height= 0.5 * screen_h,
                          screen_w=screen_w,
                          screen_h=screen_h)

mid_band = FrequencyBand(lower_bound=300,
                         upper_bound=4000,
                         song_frequencies=mid_frequencies,
                         base_color=(0, 255, 0),
                         min_height=screen_h * 0.25,
                         max_height=screen_h * 0.9,
                         screen_w=screen_w,
                         screen_h=screen_h)

treble_band = FrequencyBand(lower_bound=4000,
                            upper_bound=8000,
                            song_frequencies=treble_frequencies,
                            base_color=(0, 0, 255),
                            min_height=screen_h * 0.5,
                            max_height=screen_h,
                            screen_w=screen_w,
                            screen_h=screen_h)

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])

t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(args.filename)
pygame.mixer.music.play(0)

# Run until the user asks to quit
running = True
while running:

    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))
    # screen.fill((0, 0, 0))

    for bass, mid, treble in zip(bass_band.bars, mid_band.bars, treble_band.bars):
        bass.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, bass.freq, bass_band.frequency_index_ratio))
        mid.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, mid.freq, mid_band.frequency_index_ratio))
        treble.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, treble.freq, treble_band.frequency_index_ratio))
        treble.render(screen)
        mid.render(screen)
        bass.render(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
