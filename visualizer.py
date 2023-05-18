import librosa
import numpy as np
import pygame
from audiobar import AudioBar


def get_freq_index_ratio(freqs):
    return len(freqs) / freqs[len(freqs) - 1]


def get_decibel(target_time, freq, frequencies_index_ratio):
    return spectrogram[int(freq * frequencies_index_ratio)][int(target_time * time_index_ratio)]


def get_bars(bars, frequencies):
    r = len(frequencies)
    print(r)
    width = screen_w/r
    x = (screen_w - width*r)/2
    for c in frequencies:
        if c < 300:
            bars.append(AudioBar(x, 450, c, (255, 0, 0), max_height=300, width=width))
        elif c < 4000:
            bars.append(AudioBar(x,250, c, (0, 255, 0), max_height=300, width=width))
        else:
            bars.append(AudioBar(x, 50, c, (0, 0, 255), max_height=300, width=width))
        x += width


# TODO: add command line args for filename (and other knobs??)
filename = "Songs/LanaDelRey-DietMountainDew(OfficialInstrumental).mp3"

time_series, sample_rate = librosa.load(filename)  # getting information from the file

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

freqs = librosa.core.fft_frequencies(n_fft=2048 * 4)  # getting an array of frequencies

# split into frequency bands
# bass_frequencies, mid_frequencies, treble_frequencies = np.split(freqs, [(np.where(freqs <= 300)),
#                                                                         (np.where(freqs <= 4000))])
bass_frequencies, mid_frequencies, treble_frequencies = np.split(freqs, [300, 4000])

bass_frequency_index_ratio = get_freq_index_ratio(bass_frequencies)
mid_frequency_index_ratio = get_freq_index_ratio(mid_frequencies)
treble_frequency_index_ratio = get_freq_index_ratio(treble_frequencies)

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

time_index_ratio = len(times)/times[len(times) - 1]



pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w/1.5)
screen_h = int(infoObject.current_w/2.5)

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])


bass_bars = []
mid_bars = []
treble_bars = []


# frequencies = np.arange(100, 8000, 100)
bass_frequencies = np.arange(100, 300, 10)
mid_frequencies = np.arange(300, 4000, 185)
treble_frequencies = np.arange(4000, 8000, 200)


get_bars(bass_bars, bass_frequencies)
get_bars(mid_bars, mid_frequencies)
get_bars(treble_bars, treble_frequencies)

t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(filename)
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

    for bass, mid, treble in zip(bass_bars, mid_bars, treble_bars):
        bass.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, bass.freq, bass_frequency_index_ratio))
        mid.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, mid.freq, mid_frequency_index_ratio))
        treble.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, treble.freq, treble_frequency_index_ratio))
        treble.render(screen)
        mid.render(screen)
        bass.render(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
